import os
import re
import time
import logging

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import pymongo
from pymongo.errors import PyMongoError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Set up Swagger UI
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Ad Picker API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve swagger.json or other static files from ./static/."""
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# Read Mongo credentials / DB name from environment variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_DB   = os.getenv("MONGO_DB")

# Build or read the Mongo connection URI
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    default_hosts = (
        "<YOUR_MONGODB_FQDN_1>:27017,"
        "<YOUR_MONGODB_FQDN_2>:27017,"
        "<YOUR_MONGODB_FQDN_3>:27017"
    )
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{default_hosts}/{MONGO_DB}?replicaSet=<YOUR_MONGODB_REPLICA_SET>"

# Mask the password in logs
masked_uri = re.sub(r"//([^:]+):([^@]+)@", r"//\1:****@", MONGO_URI)
logger.info("[AdPicker] Will connect to MongoDB at: %s", masked_uri)

# Retry connecting to Mongo until it succeeds
mongo_client = None
while True:
    try:
        mongo_client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        mongo_client.admin.command("ping")  # basic connectivity check
        logger.info("[AdPicker] Successfully connected to MongoDB!")
        break
    except PyMongoError:
        logger.exception("[AdPicker] Could not connect to MongoDB. Retrying in 5s...")
        time.sleep(5)

# Access the DB and collections
db = mongo_client[MONGO_DB]
ads_coll         = db["ads"]          # user docs + "default"
last_events_coll = db["last_events"]  # stores { _id: userIdStr, event: "..." }

@app.route('/ad', methods=['GET'])
def pick_ad():
    """
    GET /ad?user_id=...
      1) Check 'last_events' for user_id's event. If missing => fallback user='default' + event='page_view'.
      2) Look up the ad doc in 'ads' using final user_id (or 'default'). If missing => fallback to 'default'.
      3) Return the sub-field for the event (or 'page_view') as JSON.
    """
    user_id_query = (request.args.get('user_id') or "").strip()
    if not user_id_query:
        return jsonify({"error": "Missing user_id"}), 400

    # Step 1: Look up last event
    try:
        last_doc = last_events_coll.find_one({"_id": user_id_query})
    except PyMongoError:
        logger.exception("[AdPicker] DB error reading last_events.")
        return jsonify({"error": "DB error reading last_events"}), 503

    if not last_doc:
        logger.info(
            "[AdPicker] No last_events doc found for user_id=%r. "
            "Falling back to 'default' + 'page_view'.",
            user_id_query
        )
        final_user_id = "default"
        event_str = "page_view"
    else:
        final_user_id = user_id_query
        event_str = last_doc.get("event", "page_view")

    # Step 2: Look up the user doc in 'ads'
    try:
        user_doc = ads_coll.find_one({"_id": final_user_id})
    except PyMongoError:
        logger.exception("[AdPicker] DB error retrieving user doc.")
        return jsonify({"error": "Database error retrieving user doc"}), 503

    if not user_doc:
        # Fallback to ads[_id="default"]
        try:
            default_doc = ads_coll.find_one({"_id": "default"})
            if not default_doc:
                logger.error("[AdPicker] Missing 'default' doc in DB. Returning 503.")
                return jsonify({
                    "error": f"No ads doc for user='{final_user_id}', and no 'default' doc",
                    "detail": "Database missing required 'default' doc"
                }), 503
            user_doc = default_doc
            logger.info("[AdPicker] No ads doc for user='%s'; using 'default'.", final_user_id)
            final_user_id = "default"
        except PyMongoError:
            logger.exception("[AdPicker] DB error retrieving 'default' doc!")
            return jsonify({"error": "Database error retrieving 'default' doc"}), 503

    # Step 3: Pull the sub-field for the event or fallback to 'page_view'
    action_data = user_doc.get(event_str) or user_doc.get("page_view")
    if not action_data:
        logger.error(
            "[AdPicker] user_doc missing event='%s' and 'page_view'. user_id_str=%r",
            event_str, final_user_id
        )
        return jsonify({
            "error": f"No data for event='{event_str}' or 'page_view' in ads doc",
            "detail": f"user_id='{final_user_id}'"
        }), 503

    # Construct the final JSON
    result = {
        "user_id": user_id_query,  # original ID from the query
        "event": event_str,
        "ad":    action_data.get("ad", "???"),
        "image": action_data.get("image", "https://example.com/default.jpg")
    }

    logger.info(
        "[AdPicker] final_user='%s', requested_user='%s', event='%s', selected ad='%s'",
        final_user_id, user_id_query, event_str, result["ad"]
    )
    return jsonify(result)

@app.route('/')
def root_index():
    """Simple health check + link to /docs."""
    base_url = request.host_url.rstrip('/')
    docs_link = f"{base_url}/docs"
    html = (
        "<html><head><title>Ad-Picker</title></head><body>"
        "<p>Ad-Picker is running. Check out the "
        f"<a href='{docs_link}'>Swagger UI</a> for API docs.</p>"
        "</body></html>"
    )
    return html

if __name__ == '__main__':
    logger.info("Starting local Flask dev server on port 8080.")
    app.run(host='0.0.0.0', port=8080, debug=False)
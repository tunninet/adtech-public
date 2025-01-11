#!/usr/bin/env python3

import os
import pymongo

# 1) Load credentials from environment variables set by the K8s Secret
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_DB   = os.getenv("MONGO_DB")

# 2) If MONGO_URI is explicitly set, it overrides the rest
#    Otherwise, build a default multi-seed replica set URI (but do NOT print the full password).
MONGO_URI = os.getenv(
    "MONGO_URI",
    f"mongodb://{MONGO_USER}:{MONGO_PASS}@"
    "<YOUR_MONGODB_FQDN_1>:27017,"
    "<YOUR_MONGODB_FQDN_2>:27017,"
    "<YOUR_MONGODB_FQDN_3>:27017/"
    f"{MONGO_DB}?replicaSet=<YOUR_MONGODB_REPLICA_SET>"
)

# Mask the password for logging
masked_pass = "*****" if MONGO_PASS else ""
masked_uri = MONGO_URI.replace(MONGO_PASS, masked_pass)

print("[seed_db] Will connect to MongoDB using something like:\n  ", masked_uri)

# Optionally: parse out hosts to log only the cluster addresses:
# hosts_example = "<YOUR_MONGODB_REPLICA_SET>-0,<YOUR_MONGODB_REPLICA_SET>-1,<YOUR_MONGODB_REPLICA_SET>-2"
# or skip logging altogether if you prefer absolute minimal logs.

# 3) Connect with PyMongo
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

ads_collection = db["ads"]

print("[seed_db] Clearing out old docs from 'ads' collection...")
ads_collection.delete_many({})

# 4) Full data for user IDs 1..10 + "default" doc
#    Each doc has "_id": <string>, plus "page_view", "click", "purchase".
full_data = {
    "1": {
        "page_view": {
            "ad": "Ad 1: Explore new gadgets!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad1-page_view.jpg"
        },
        "click": {
            "ad": "Ad 1: Limited-time offer on gadgets!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad1-click.jpg"
        },
        "purchase": {
            "ad": "Ad 1: Thank you for purchasing!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad1-purchase.jpg"
        }
    },
    "2": {
        "page_view": {
            "ad": "Ad 2: Check out our laptops!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad2-page_view.jpg"
        },
        "click": {
            "ad": "Ad 2: Laptop discount, click now!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad2-click.jpg"
        },
        "purchase": {
            "ad": "Ad 2: You bought a laptop!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad2-purchase.jpg"
        }
    },
    "3": {
        "page_view": {
            "ad": "Ad 3: Discover our books collection!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad3-page_view.jpg"
        },
        "click": {
            "ad": "Ad 3: Buy 1 get 1 free on books!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad3-click.jpg"
        },
        "purchase": {
            "ad": "Ad 3: Enjoy your new book!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad3-purchase.jpg"
        }
    },
    "4": {
        "page_view": {
            "ad": "Ad 4: Latest fashion trends!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad4-page_view.jpg"
        },
        "click": {
            "ad": "Ad 4: Fashion sale, click now!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad4-click.jpg"
        },
        "purchase": {
            "ad": "Ad 4: Thanks for shopping!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad4-purchase.jpg"
        }
    },
    "5": {
        "page_view": {
            "ad": "Ad 5: Explore new software!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad5-page_view.jpg"
        },
        "click": {
            "ad": "Ad 5: Software discounts, click here!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad5-click.jpg"
        },
        "purchase": {
            "ad": "Ad 5: Thanks for your purchase!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad5-purchase.jpg"
        }
    },
    "6": {
        "page_view": {
            "ad": "Ad 6: Discover new movies!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad6-page_view.jpg"
        },
        "click": {
            "ad": "Ad 6: Movie night discounts!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad6-click.jpg"
        },
        "purchase": {
            "ad": "Ad 6: Enjoy your movie!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad6-purchase.jpg"
        }
    },
    "7": {
        "page_view": {
            "ad": "Ad 7: Check out our furniture!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad7-page_view.jpg"
        },
        "click": {
            "ad": "Ad 7: Furniture sale, click now!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad7-click.jpg"
        },
        "purchase": {
            "ad": "Ad 7: Thanks for buying!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad7-purchase.jpg"
        }
    },
    "8": {
        "page_view": {
            "ad": "Ad 8: Browse our music collection!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad8-page_view.jpg"
        },
        "click": {
            "ad": "Ad 8: Music deals, click here!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad8-click.jpg"
        },
        "purchase": {
            "ad": "Ad 8: Enjoy your new music!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad8-purchase.jpg"
        }
    },
    "9": {
        "page_view": {
            "ad": "Ad 9: Explore our gaming offers!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad9-page_view.jpg"
        },
        "click": {
            "ad": "Ad 9: Gaming discounts, click now!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad9-click.jpg"
        },
        "purchase": {
            "ad": "Ad 9: Thanks for purchasing a game!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad9-purchase.jpg"
        }
    },
    "10": {
        "page_view": {
            "ad": "Ad 10: Discover new deals!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad10-page_view.jpg"
        },
        "click": {
            "ad": "Ad 10: Special discounts available!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad10-click.jpg"
        },
        "purchase": {
            "ad": "Ad 10: Enjoy your new product!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/ad10-purchase.jpg"
        }
    },
    "default": {
        "page_view": {
            "ad": "Default Ad: Visit our website!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/default-page_view.jpg"
        },
        "click": {
            "ad": "Default Ad: Click here for more!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/default-click.jpg"
        },
        "purchase": {
            "ad": "Default Ad: Thank you for purchasing!",
            "image": "<YOUR_S3_SERVER>/<YOUR_S3_BUCKET>/default-purchase.jpg"
        }
    }
}

print("[seed_db] Inserting docs for user IDs 1..10 plus 'default' doc into 'ads' collection...")
for user_id, actions_dict in full_data.items():
    doc = {"_id": user_id}
    doc.update(actions_dict)
    ads_collection.insert_one(doc)

print("[seed_db] Done seeding 'ads' collection with user IDs 1..10 plus 'default'.")
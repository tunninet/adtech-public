# Ad Picker (Mongo-based)

This service uses Flask + MongoDB. It fetches the user’s last event from `last_events` and the ad configuration from `ads` in the same database (`adtech`).

## Endpoints

- **GET** `/ad?user_id=...` - Returns JSON with `"ad"`, `"image"`, `"user_id"`, and `"event"` fields.

## Files

- `app.py` - The main Flask application code
- `static/swagger.json` - Swagger UI spec
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker build recipe
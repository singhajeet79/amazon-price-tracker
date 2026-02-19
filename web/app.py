from flask import Flask, request, jsonify
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tracker.service import (
    track_product,
    get_current_price,
    run_price_checks,
)
from tracker.scraper import ScrapingError
from tracker.storage import init_db

app = Flask(__name__)

# Ensure DB initialized on startup
init_db()


@app.route("/")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/price", methods=["POST"])
def api_price():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url'"}), 400

    try:
        result = get_current_price(data["url"])
        return jsonify(result)
    except ScrapingError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/track", methods=["POST"])
def api_track():
    data = request.get_json()

    required = ["url", "target_price", "channel", "contact"]
    if not data or not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = track_product(
            url=data["url"],
            target_price=float(data["target_price"]),
            channel=data["channel"],
            contact=data["contact"],
        )
        return jsonify(result)
    except ScrapingError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/run-checks", methods=["POST"])
def api_run_checks():
    run_price_checks()
    return jsonify({"status": "checks completed"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

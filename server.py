from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from distance import calculate_distance
from config import WAREHOUSE_LAT, WAREHOUSE_LON, MAX_DISTANCE_KM
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)
CORS(app)

# geopy locator
geolocator = Nominatim(user_agent="pincode_checker")


# homepage
@app.route("/")
def home():
    return render_template("index.html")


# manual pincode check
@app.route("/check-pincode", methods=["POST"])
def check_pincode():
    try:
        data = request.json
        pincode = data.get("pincode")

        if not pincode:
            return jsonify({"status": "invalid_pincode"}), 400

        location = geolocator.geocode(f"{pincode}, India", addressdetails=True)

        if location is None:
            return jsonify({"status": "not_found"})

        lat = location.latitude
        lon = location.longitude

        address = location.raw.get("address", {})

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or "Unknown"
        )

        state = address.get("state", "Unknown")

        distance = calculate_distance(
            WAREHOUSE_LAT,
            WAREHOUSE_LON,
            lat,
            lon
        )

        status = "available" if distance <= MAX_DISTANCE_KM else "not_available"

        return jsonify({
            "status": status,
            "distance": round(distance, 2),
            "city": city,
            "state": state
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# auto GPS check
@app.route("/auto-check", methods=["POST"])
def auto_check():
    try:
        data = request.json

        user_lat = data.get("lat")
        user_lon = data.get("lon")

        distance = calculate_distance(
            WAREHOUSE_LAT,
            WAREHOUSE_LON,
            user_lat,
            user_lon
        )

        status = "available" if distance <= MAX_DISTANCE_KM else "not_available"

        return jsonify({
            "status": status,
            "distance": round(distance, 2)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# 🔥 IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
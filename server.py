from flask import Flask, request, jsonify, render_template
from distance import calculate_distance
from config import WAREHOUSE_LAT, WAREHOUSE_LON, MAX_DISTANCE_KM
from geopy.geocoders import Nominatim

app = Flask(__name__)

# geopy locator
geolocator = Nominatim(user_agent="pincode_checker")


# homepage
@app.route("/")
def home():
    return render_template("index.html")


# manual pincode check
@app.route("/check-pincode", methods=["POST"])
def check_pincode():

    data = request.json
    pincode = data["pincode"]

    # fetch location using geopy
    location = geolocator.geocode(f"{pincode}, India", addressdetails=True)

    if location is None:
        return jsonify({"status": "not_found"})

    lat = location.latitude
    lon = location.longitude

    # address details
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

    if distance <= MAX_DISTANCE_KM:
        status = "available"
    else:
        status = "not_available"

    return jsonify({
        "status": status,
        "distance": round(distance, 2),
        "city": city,
        "state": state
    })


# auto GPS check
@app.route("/auto-check", methods=["POST"])
def auto_check():

    data = request.json
    user_lat = data["lat"]
    user_lon = data["lon"]

    distance = calculate_distance(
        WAREHOUSE_LAT,
        WAREHOUSE_LON,
        user_lat,
        user_lon
    )

    if distance <= MAX_DISTANCE_KM:
        status = "available"
    else:
        status = "not_available"

    return jsonify({
        "status": status,
        "distance": round(distance, 2)
    })


if __name__ == "__main__":
    app.run(debug=True)
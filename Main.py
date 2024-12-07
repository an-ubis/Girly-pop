pip install flask

2. Create the app.py (Flask Server):

from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import json

app = Flask(__name__)

# In-memory database of contacts (replace with real database in production)
emergency_contacts = {}

# Geolocator for getting user address from coordinates
geolocator = Nominatim(user_agent="emergency_contact_app")

@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    if name and phone:
        emergency_contacts[name] = phone
        return jsonify({"message": "Contact added successfully!"}), 200
    return jsonify({"message": "Invalid data!"}), 400

@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    return jsonify(emergency_contacts), 200

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    location = data.get("location")  # Location is expected as "latitude,longitude"
    if location:
        latitude, longitude = map(float, location.split(','))
        location_info = geolocator.reverse((latitude, longitude), language='en')
        message = f"Emergency! I'm at {location_info}. Please help!"
        
        # In a real app, you would send this message to each contact via SMS or email.
        for name, phone in emergency_contacts.items():
            print(f"Sending message to {name} ({phone}): {message}")  # Placeholder for real sending

        return jsonify({"message": "Location sent to contacts!"}), 200
    return jsonify({"message": "Location not provided!"}), 400

if __name__ == "__main__":
    app.run(debug=True)

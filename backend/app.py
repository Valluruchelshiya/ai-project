from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import random
import requests

app = Flask(__name__)
CORS(app)

CALORIENINJAS_API_KEY = "mq5TY/QEqAWfuYwW3aPQ/A==SkdwPHPEyTZeF5Uk"

# Common food list
FOOD_LIST = ["banana", "apple", "pizza", "burger", "salad", "pasta", "sandwich"]

@app.route("/")
def home():
    return "✅ Flask backend ready (no ML detection)"

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Randomly choose food from list
    food_choice = random.choice(FOOD_LIST)
    print(f"🍽️ Selected food: {food_choice}")

    resp = requests.get(
        f"https://api.calorieninjas.com/v1/nutrition?query={food_choice}",
        headers={"X-Api-Key": CALORIENINJAS_API_KEY}
    )
    items = resp.json().get("items", [])

    return jsonify({
        "food_detected": [food_choice],
        "nutrition": {food_choice: items}
    })

if __name__ == "__main__":
    app.run(debug=True)

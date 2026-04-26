from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)
CORS(app)


API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"

@app.route("/recipes", methods=["GET"])
def get_recipes():
    ingredients = request.args.get("ingredients","")

    if not ingredients:
        return jsonify({"Error": "No ingredients provided."}), 400
    if not API_KEY:
        return jsonify({"Error": "Missing Spoonacular API key."}), 500

    params = {
        "ingredients": ingredients,
        "number": 10,   # --- Recipes to return
        "ranking": 1,   # --- Maximizing used ingredients
        "ignorePantry": True,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
# ---- Making Changes on 04/25/26 -----
        # recipes = response.json()
        # return jsonify(recipes)
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

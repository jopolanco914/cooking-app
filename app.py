from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)
CORS(app)
load_dotenv()


API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

@app.route("/recipes", methods=["GET"])
def get_recipes():
    ingredients = request.args.get("ingredients", "")
    diet = request.args.get("diet", "")
    intolerances = request.args.get("intolerances", "")
    max_carbs = request.args.get("maxCarbs", "")
    min_protein = request.args.get("minProtein", "")

    if not ingredients:
        return jsonify({"Error": "No ingredients provided."}), 400
    if not API_KEY:
        return jsonify({"Error": "Missing Spoonacular API key."}), 500
    # ----- Changes made to Params 4/25/26 ----
    # to delete: ranking, ignorePantry
    # to add: fillIngredients
    params = {
        "includeIngredients": ingredients,
        "number": 10,   # --- Recipes to return
        "addRecipeInformation": True,
        "fillIngredients": True,
        "apiKey": API_KEY
    }

    if diet:
        params["diet"] = diet

    if intolerances:
        params["intolerances"] = intolerances

    if max_carbs:
        params["maxCarbs"] = max_carbs

    if min_protein:
        params["minProtein"] = min_protein


    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data =  response.json()
# ---- Making Changes on 04/25/26 -----
        # recipes = response.json()
        # return jsonify(recipes)
        return jsonify(data.get("results", []))

    except requests.exceptions.RequestException as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

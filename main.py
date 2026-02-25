from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from collections import defaultdict


app = FastAPI()

# ---- Example of Database ----

RECIPES = [
    {
        "id":1,
        "name": "Chicken Fried Rice",
        "ingredients": ["Chicken Thighs", "Soy Sauce", "Sugar", "Aromatic",
                        "Aromatics", "Rice", "Vegetables"]
    },
    {
        "id":2,
        "name":"Omelette",
        "ingredients": ["Eggs", "Butter", "Salt and Pepper", "Cheese", "Onions", "Spinach",
                        "Bell Peppers"]

    },
    {
        "id":3,
        "name": "Grilled Cheese Sandwich",
        "ingredients": ["Bread", "Cheese", "Butter"]
    }
]

class IngredientInput(BaseModel):
    ingredients: List[str]


def normalize(ingredients: List[str]) -> set:
    return set(i.strip().lower() for i in ingredients)

def analyze_recipe(recipe: Dict, user_ingredients: set):
    recipe_ingredients = normalize(recipe["ingredients"])

    matches = recipe_ingredients & user_ingredients
    missing = recipe_ingredients - user_ingredients

    return {
        "recipe": recipe["id"],
        "name": recipe["name"],
        "matches":list(matches),
        "missing": list(missing),
        "match_count": len(matches),
        "missing_count": len(missing)
    }


@app.post("/suggest")
def suggest_recipes(input: IngredientInput):
    user_ingredients = normalize(input.ingredients)

    complete_recipes = []
    partial_recipes = []
    grocery_suggestions = defaultdict(int)

    for recipe in RECIPES:
        result =  analyze_recipe(recipe, user_ingredients)

        if result["missing_count"] == 0:
            complete_recipes.append(recipe)
        elif result["missing_count"] <= 2:
            partial_reciples.append(recipe)

        # ---- Keeping Track of missing ingredients ----

            for item in result["missing"]:
                grocery_suggestions[item] += 1


    # ---- Sorting partial recipes by fewest missing ingredients ----
    partial_recipes.sort(key=lambda x: x["missing_count"])

    return {
        "Complete Recipes": complete_recipes,
        "Almost Complete Recipes": partial_recipes,
        "Suggested Recipes": sorted(
            grocery_suggestions.items(),
            key=lambda x: x[1],
            reverse=True
        )
    }





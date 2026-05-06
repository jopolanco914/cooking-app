import sys

import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLineEdit, QListWidget, QTextEdit, QScrollArea,
                             QFrame, QMessageBox, QSplitter)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import csv
import re
from collections import defaultdict


# ---- Adding Worker Thread that calls Flask/Spoonacular in the background then sends results back to UI ----


class RecipeWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        try:
            response = requests.get(
                "http://127.0.0.1:5000/recipes",
                params=self.params,
                timeout=10
            )

            if response.status_code != 200:
                self.error.emit(f"API Error: {response.text}")
                return

            recipes = response.json()
            self.finished.emit(recipes)

        except Exception as e:
            self.error.emit(str(e))

# ---- Class Implementing QThread made ---- DONE





class RecipeBookWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = "13k-recipes.csv"
        self.setGeometry(400, 200, 800, 600)
        self.setWindowTitle("Recipe Book")

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("📖 Recipe Book", self)
        title.setFont(QFont("Times New Roman", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: #ac5633; color: white; padding: 10px;")
        layout.addWidget(title)

        # Search section
        search_layout = QHBoxLayout()
        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText("Enter recipe name...")
        self.searchBox.setMinimumHeight(35)
        search_button = QPushButton("🔍 Search")
        search_button.clicked.connect(self.searchRecipe)
        search_button.setMinimumHeight(35)
        search_layout.addWidget(self.searchBox)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Splitter for recipe list and details
        splitter = QSplitter(Qt.Horizontal)

        # Recipe list
        self.recipeList = QListWidget()
        self.recipeList.itemClicked.connect(self.displayRecipeDetails)
        splitter.addWidget(self.recipeList)

        # Recipe details area
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)

        self.recipeTitle = QLabel()
        self.recipeTitle.setFont(QFont("Arial", 16, QFont.Bold))
        self.recipeTitle.setWordWrap(True)

        self.ingredientsText = QTextEdit()
        self.ingredientsText.setReadOnly(True)
        self.ingredientsText.setPlaceholderText("Ingredients will appear here...")

        self.instructionsText = QTextEdit()
        self.instructionsText.setReadOnly(True)
        self.instructionsText.setPlaceholderText("Instructions will appear here...")

        details_layout.addWidget(self.recipeTitle)
        details_layout.addWidget(QLabel("📝 Ingredients:"))
        details_layout.addWidget(self.ingredientsText)
        details_layout.addWidget(QLabel("👨‍🍳 Instructions:"))
        details_layout.addWidget(self.instructionsText)

        splitter.addWidget(details_widget)
        splitter.setSizes([300, 500])

        layout.addWidget(splitter)

        # Load all recipes
        self.loadAllRecipes()

    def loadAllRecipes(self):
        """Load all recipe titles into the list"""
        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.recipeList.addItem(row["Title"])
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"File {self.file_path} not found!")

    def searchRecipe(self):
        """Search for specific recipe"""
        search_term = self.searchBox.text().lower()
        if not search_term:
            self.loadAllRecipes()
            return

        self.recipeList.clear()
        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if search_term in row["Title"].lower():
                        self.recipeList.addItem(row["Title"])
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"File {self.file_path} not found!")

    def displayRecipeDetails(self, item):
        """Display full recipe details when clicked"""
        recipe_name = item.text()
        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Title"] == recipe_name:
                        self.recipeTitle.setText(row["Title"])

                        # Clean up ingredients
                        ingredients = row["Ingredients"].strip("[]")
                        ingredients_list = [i.strip().strip("'") for i in ingredients.split("', '")]
                        self.ingredientsText.setText("\n• " + "\n• ".join(ingredients_list))

                        # Clean up instructions
                        instructions = row["Instructions"].strip('"')
                        self.instructionsText.setText(instructions)
                        break
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load recipe: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ---- 4/26/26 -----
        # Implementing the history QPushButton to keep track of previous combinations
        self.searchHistory = []

        self.inputIngredients = []
        self.file_path = "13k-recipes.csv"
        self.recipes = self.loadRecipes()

        self.setWindowTitle("Barbecue Chicken - Recipe Finder")
        self.setGeometry(300, 200, 900, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Title section
        title = QLabel("🍗 Barbecue Chicken 🍗", self)
        title.setFont(QFont("Times New Roman", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: #b2ccab; padding: 20px; margin: 0px;")
        main_layout.addWidget(title)

        # Authors
        author = QLabel("Developers: Jose Polanco, Brian Nguyen, Vitalli Protsenko")
        author.setFont(QFont("Arial", 10))
        author.setAlignment(Qt.AlignCenter)
        author.setStyleSheet("margin-bottom: 20px;")
        main_layout.addWidget(author)

        # Button row
        button_layout = QHBoxLayout()

        self.recipeBookButton = QPushButton("📚 Recipe Book")
        self.recipeBookButton.clicked.connect(self.openRecipeBook)
        self.recipeBookButton.setMinimumHeight(80)
        self.recipeBookButton.setStyleSheet("background-color: #affae2; font-size: 16px; font-weight: bold;")

        self.findRecipeButton = QPushButton("🔍 Find Recipe")
        self.findRecipeButton.clicked.connect(self.findRecipe)
        self.findRecipeButton.setMinimumHeight(80)
        self.findRecipeButton.setStyleSheet("background-color: #affab4; font-size: 16px; font-weight: bold;")

        self.historyButton = QPushButton("📜 History")
        self.historyButton.clicked.connect(self.showHistory)
        self.historyButton.setMinimumHeight(80)
        self.historyButton.setStyleSheet("background-color: #fae8af; font-size: 16px; font-weight: bold;")

        button_layout.addWidget(self.recipeBookButton)
        button_layout.addWidget(self.findRecipeButton)
        button_layout.addWidget(self.historyButton)
        main_layout.addLayout(button_layout)

        # Diet preferences
        diet_frame = QFrame()
        diet_frame.setStyleSheet("background-color: #f0f0f0; padding: 10px; margin: 10px 0;")
        diet_layout = QHBoxLayout(diet_frame)

        self.proteinButton = QPushButton("💪 Protein Heavy")
        self.glutenFreeButton = QPushButton("🌾 Gluten Free")
        self.lowCarbsButton = QPushButton("🥗 Low Carbs")
        self.vegetarianButton = QPushButton("🥬 Vegetarian")


        for btn in [self.proteinButton, self.glutenFreeButton, self.lowCarbsButton, self.vegetarianButton]:
            btn.setCheckable(True)
            btn.setStyleSheet(
                "QPushButton { padding: 10px; font-size: 12px; } QPushButton:checked { background-color: #4CAF50; color: white; }")
            diet_layout.addWidget(btn)

        main_layout.addWidget(diet_frame)

        # ---- 4/26/26 -----
        # Combining the Spoonacular Recipes and 13K recipes to have more options
        self.useApiButton = QPushButton("🌐 Spoonacular API")
        self.useCsvButton = QPushButton("📁 Local Recipe File")

        self.useApiButton.setCheckable(True)
        self.useCsvButton.setCheckable(True)

        self.useApiButton.setChecked(True)
        self.useCsvButton.setChecked(True)

        for btn in [self.useApiButton, self.useCsvButton]:
            btn.setStyleSheet(
            "QPushButton { padding: 10px; font-size: 12px; } "
            "QPushButton:checked { background-color: #2196F3; color: white; }"
            )
            diet_layout.addWidget(btn)

        # ---- 4/26/26 ---- DONE







        # Ingredient input section
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #fff3e0; padding: 15px;")
        input_layout = QVBoxLayout(input_frame)

        input_label = QLabel("✏️ Enter Your Ingredients:")
        input_label.setFont(QFont("Arial", 12, QFont.Bold))
        input_layout.addWidget(input_label)

        ingredient_input_layout = QHBoxLayout()
        self.ingredientInput = QLineEdit()
        self.ingredientInput.setPlaceholderText("Type an ingredient and press Enter or click Add...")
        self.ingredientInput.returnPressed.connect(self.addIngredient)

        add_button = QPushButton("➕ Add")
        add_button.clicked.connect(self.addIngredient)

        ingredient_input_layout.addWidget(self.ingredientInput)
        ingredient_input_layout.addWidget(add_button)
        input_layout.addLayout(ingredient_input_layout)

        # Ingredient list display
        self.ingredientList = QListWidget()
        self.ingredientList.setMaximumHeight(100)
        input_layout.addWidget(self.ingredientList)

        clear_button = QPushButton("🗑️ Clear All")
        clear_button.clicked.connect(self.clearIngredients)
        input_layout.addWidget(clear_button)

        main_layout.addWidget(input_frame)

        # Results section
        results_label = QLabel("📊 Recipe Suggestions:")
        results_label.setFont(QFont("Arial", 14, QFont.Bold))
        results_label.setStyleSheet("margin-top: 15px;")
        main_layout.addWidget(results_label)

        # Results text area
        self.resultsText = QTextEdit()
        self.resultsText.setReadOnly(True)
        self.resultsText.setMinimumHeight(300)
        self.resultsText.setStyleSheet("font-family: Consolas; font-size: 11px;")
        main_layout.addWidget(self.resultsText)

        # ---- Adding Button to Find Recipes  (04/25/26) ----
        # Find recipe button at bottom
        self.findBigButton = QPushButton("🔍 FIND RECIPES WITH THESE INGREDIENTS 🔍")
        self.findBigButton.clicked.connect(self.findRecipe)
        self.findBigButton.setMinimumHeight(50)
        self.findBigButton.setStyleSheet("background-color: #ff9800; color: white; font-size: 14px; font-weight: bold;")
        main_layout.addWidget(self.findBigButton)



    # ---- (4/26/26) ----
    # Implementing the method that will allow us to look at the local recipes


    # ---- (5/5/26) ----
    # Making the search algorithm less specific so we can find more recipes in the CSV file
    # 1) Adding a normalize function
    # 2) Adding ingredient_match function
    # 3) editing the searchLocalRecipes
    # 4) filtering the ingredients in the CSV file

    def normalize2(self, text):
        text = text.lower().strip()

    # ---- Removing punctuation ----
        text = re.sub(r"[^a-zA-Z\s]","",text)

    # ---- Remove measurements ----
        measurement_words = [
        "cup", "cups", "tbsp", "tablespoon", "tablespoons",
        "tsp", "teaspoon", "teaspoons", "oz", "ounce", "ounces",
        "lb", "pound", "pounds", "gram", "grams", "kg", "ml", "liter",
        "liters"
        ]

    # ---- Remove descriptive words ----
        descriptor_words = [
        "fresh", "frozen", "dried", "boneless", "skinless", "large",
        "small", "medium", "extra", "virgin", "chopped", "diced", "minced",
        "sliced", "shredded", "grated", "crushed", "ground", "whole", "halved", "cubed",
        "cooked", "uncooked", "raw", "lean"
        ]

        remove_words = measurement_words + descriptor_words

        words = text.split()

        words = [w for w in words if w not in remove_words]

        text = " ".join(words)

    # ---- Ingredient family replacements ----
        replacements = {

            # ---- eggs ----
            "eggs":"egg",

           # ---- Family of onions ----
            "onions":"onion",
            "green onions":"onion",
            "red onions":"onion",
            "yellow onions":"onion",
            "white onions":"onion",
            "scallions":"onion",

           # ---- Family of garlic ----
            "garlic cloves":"garlic",
            "cloves garlic":"garlic",


           # ---- Family of tomatoes ----
            "tomatoes":"tomato",
            "roma tomatoes":"tomato",
            "cherry tomatoes":"tomato",


           # ---- Family of Potato ----
            "potatoes":"potato",
            "russet potatoes":"potato",

        #  ---- Family of Cheese ----
            "cheddar cheese":"cheese",
            "mozzarella cheese":"cheese",
            "parmesan cheese":"cheese",
            "swiss cheese":"cheese",


        # ---- Family of Beef ----
            "ground beef":"beef",
            "beef chuck":"beef",
            "steak":"beef",

        # ---- Family of Oils ----
            "olive oil":"oil",
            "vegetable oil":"oil",
            "canola oil":"oil",

        # ---- Family of Peppers ----
            "bell peppers":"pepper",
            "bell pepper":"pepper",
            "black pepper":"pepper",

        #  START ON RICE
            "white rice":"rice",
            "brown rice":"rice",

            # ---- Family of Milk ----
            "whole milk":"milk",
            "skim milk":"milk",

        # ---- Family of Pasta ----
            "spaghetti":"pasta",
            "penne":"pasta",
            "macaroni":"pasta"
        }

        return replacements.get(text, text)


    def ingredientMatch(self, user_item, recipe_item):
        user_item = self.normalize2(user_item)
        recipe_item = self.normalize2(recipe_item)

    #  ---- Exact Match ----
        if user_item == recipe_item:
            return True

    #  ---- Partial Match ----
        if user_item in recipe_item:
            return True

        if recipe_item in user_item:
            return True


        return False

    # ---- 5/5/26 -----
    # 1) Changing current algorithm for searchLocalRecipes

    def searchLocalRecipes(self):
        user_ingredients = [self.normalize2(i) for i in self.inputIngredients]
        local_results = []

        for recipe in self.recipes:
            recipe_ingredients = [self.normalize2(i) for i in recipe["ingredients"]]

            matches = []
            missing = []

            for recipe_item in recipe_ingredients:
                found = False

                for user_item in user_ingredients:
                    if self.ingredientMatch(user_item, recipe_item):
                        found = True
                        matches.append(recipe_item)
                        break

                if not found:
                    missing.append(recipe_item)

            if len(matches) > 0:
                match_score = round((len(matches) / len(recipe_ingredients)) * 100, 1)

                local_results.append({
                    "name": recipe["name"],
                    "matches": matches,
                    "missing": missing,
                    "match_score": match_score,
                    "match_count": len(matches),
                    "missing_count": len(missing)
                })

        local_results.sort(key=lambda x: x["match_score"], reverse=True)
        return local_results[:10]

    # ---- (5/5/26) ---- DONE

    def loadRecipes(self):
        """Load recipes from CSV"""
        recipes = []
        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for idx, row in enumerate(reader, start=1):
                    ingredients_str = row["Ingredients"].strip("[]")
                    ingredients_list = [i.strip().strip("'") for i in ingredients_str.split("', '")]
                    recipes.append({
                        "id": idx,
                        "name": row["Title"],
                        "ingredients": ingredients_list
                    })
        except FileNotFoundError:
            # Fallback recipes
            recipes = [
                {"id": 1, "name": "Chicken Fried Rice",
                 "ingredients": ["Chicken Thighs", "Soy Sauce", "Sugar", "Rice", "Vegetables"]},
                {"id": 2, "name": "Omelette", "ingredients": ["Eggs", "Butter", "Salt", "Cheese", "Onions"]},
                {"id": 3, "name": "Grilled Cheese Sandwich", "ingredients": ["Bread", "Cheese", "Butter"]}
            ]
        return recipes

    def addIngredient(self):
        """Add ingredient to the list"""
        ingredient = self.ingredientInput.text().strip()
        if ingredient:
            self.inputIngredients.append(ingredient)
            self.ingredientList.addItem(ingredient)
            self.ingredientInput.clear()

    def clearIngredients(self):
        """Clear all ingredients"""
        self.inputIngredients = []
        self.ingredientList.clear()
        self.resultsText.clear()

    def findRecipe(self):
        # ---- Changing to read from the Flask API ----
        # ---- (4/26/26) -----
        # Implementing the CSV file and the API recipes together

        """Find recipes based on ingredients"""
        if not self.inputIngredients:
            QMessageBox.warning(self, "No Ingredients", "Please add some ingredients first!")
            return

        if not self.useApiButton.isChecked() and not self.useCsvButton.isChecked():
            QMessageBox.warning(self, "No Source Selected", "Please select API, local file, or both.")
            return

        # ---- Flask API implementation ----
        ingredients_str = ",".join(self.inputIngredients)


        self.resultsText.clear()
        self.resultsText.append("⌛ Fetching recipes...")

        self.findRecipeButton.setEnabled(False)
        self.findBigButton.setEnabled(False)

        local_results = []

        if self.useCsvButton.isChecked():
            local_results = self.searchLocalRecipes()

        if self.useApiButton.isChecked():
            params = {
                "ingredients": ingredients_str
            }

            if self.vegetarianButton.isChecked():
                params["diet"] = "vegetarian"

            if self.glutenFreeButton.isChecked():
                params["intolerances"] = "gluten"

            if self.lowCarbsButton.isChecked():
                params["maxCarbs"] = "30"

            if self.proteinButton.isChecked():
                params["minProtein"] = "25"

            self.worker = RecipeWorker(params)
            self.worker.finished.connect(
                lambda recipes: self.displayCombinedResults(recipes, local_results, ingredients_str)
            )
            self.worker.error.connect(self.displayApiError)


            # ---- 04/26/26 ----- CHANGE
            # ---- Added this hear because I want to add the history before the API starts
            if ingredients_str not in self.searchHistory:
                self.searchHistory.append(ingredients_str)

            # ---- 04/26/26 ---- DONE

            self.worker.start()
        else:
            self.displayCombinedResults([], local_results, ingredients_str)



    # ---- 5/5/26 ----
    # Edited the last line
    def displayCombinedResults(self, api_recipes, local_results, ingredients_str):
        self.resultsText.clear()
        self.resultsText.append("=" * 60)
        self.resultsText.append(f"📦 INGREDIENTS: {ingredients_str}")
        self.resultsText.append("=" * 60)

        if self.useApiButton.isChecked():
            self.resultsText.append("\n 🌐 SPOONACULAR API RESULTS")

            if not api_recipes:
                self.resultsText.append("❌ No API recipes found.\n")
            else:
                for recipe in api_recipes:
                    self.resultsText.append(f"\n 🍽 {recipe.get('title', 'No Title')}")
                    self.resultsText.append(f"✅ Used Ingredients: {recipe.get('usedIngredientCount', 0)}")
                    self.resultsText.append(f"❌ Missing Ingredients: {recipe.get('missedIngredientCount', 0)}")

                    missed = recipe.get("missedIngredients", [])
                    if missed:
                        self.resultsText.append("🛒 Ingredients to buy:")
                        for item in missed:
                            self.resultsText.append(f"     *{item.get('name', 'Unknown ingredient')}")
                    else:
                        self.resultsText.append("🎉 You have all the ingredients!")

        # else:
        #     for recipe in api_recipes:
        #         self.resultsText.append(f"\n 🍽 {recipe.get('title', 'No Title')}")
        #         self.resultsText.append(f"✅ Used Ingredients: {recipe.get('usedIngredientCount', 0)}")
        #         self.resultsText.append(f"❌ Missing Ingredients: {recipe.get('missedIngredientCount', 0)}")
        #
        #         missed = recipe.get("missedIngredients", [])
        #         if missed:
        #             self.resultsText.append("🛒 Ingredients to buy:")
        #             for item in missed:
        #                 self.resultsText.append(f"     *{item.get('name', 'Unknown ingredient')}")
        #         else:
        #             self.resultsText.append("🎉 You have all the ingredients!")

        if self.useCsvButton.isChecked():
            self.resultsText.append("\n📁 LOCAL RECIPE FILE RESULTS:\n")

            if not local_results:
                self.resultsText.append("❌ No local recipes found.\n")
            else:
                for recipe in local_results:
                    self.resultsText.append(f"\n📖 {recipe['name']}")
                    self.resultsText.append(f"🔥 Match Score: {recipe['match_score']}%")
                    self.resultsText.append(f"✅ You have: {', '.join(recipe['matches'][:5])}")
                    self.resultsText.append(f"❌ Need: {', '.join(recipe['missing'][:10])}")

        self.findRecipeButton.setEnabled(True)
        self.findBigButton.setEnabled(True)





    def displayApiResults(self, recipes, ingredients_str):
        self.resultsText.clear()
        self.resultsText.append("=" * 60)
        self.resultsText.append(f"📦 INGREDIENTS: {ingredients_str}")
        self.resultsText.append("=" * 60)


        if not recipes:
            self.resultsText.append("\n ❌ No recipes found. \n")
            self.findRecipeButton.setEnabled(True)
            self.findBigButton.setEnabled(True)
            return
        else:
            for recipe in recipes:
                self.resultsText.append(f"\n 🍽 {recipe.get('title', 'No Title')}")
                self.resultsText.append(f" ✅ Used Ingredients: {recipe.get('usedIngredientCount', 0)}")
                self.resultsText.append(f" ❌ Missing Ingredients: {recipe.get('missedIngredientCount', 0)}")

                missed = recipe.get("missedIngredients", [])

                if missed:
                    self.resultsText.append("🛒 Ingredients to buy: ")
                    for item in missed:
                        self.resultsText.append(f"     * {item.get('name', 'Unknown ingredient')}")
                else:
                    self.resultsText.append("🎉 You have all the ingredients!")


        # ---- Added bottom two lines to enable buttons after response ----
        # ---- 4/25/26 ----
        self.findRecipeButton.setEnabled(True)
        self.findBigButton.setEnabled(True)

    def displayApiError(self, error_message):
        # ---- Added bottom two lines to enable buttons after response ----
        # ---- 4/25/26 ----
        self.findRecipeButton.setEnabled(True)
        self.findBigButton.setEnabled(True)

        QMessageBox.warning(self, "Error", f"Failed to fetch recipes: \n{error_message}")

    # ---- Changes made to connect flask and Interface with QThread library ----




    def openRecipeBook(self):
        """Open the recipe book window"""
        self.recipe_book_window = RecipeBookWindow()
        self.recipe_book_window.show()

    def showHistory(self):
        """Show recipe search history"""
        # ---- 4/26/26 -----
        # Implementing the history QPushButton to keep track of previous combinations
        if not self.searchHistory:
            QMessageBox.information(self, "History", "No ingredient in search history yet.")
            return

        history_text = "Previous ingredient searches \n\n"

        for index, item in enumerate(self.searchHistory, start=1):
            history_text += f"{index}. {item}\n"

        QMessageBox.information(self, "History", history_text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
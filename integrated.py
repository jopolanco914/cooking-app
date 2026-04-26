import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLineEdit, QListWidget, QTextEdit, QScrollArea,
                             QFrame, QMessageBox, QSplitter)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import csv
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

        """Find recipes based on ingredients"""
        if not self.inputIngredients:
            QMessageBox.warning(self, "No Ingredients", "Please add some ingredients first!")
            return


        # ---- Flask API implementation ----
        ingredients_str = ",".join(self.inputIngredients)

        # ---- Change 4/25/26 ----
        # Added params {} set
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

        self.resultsText.clear()
        self.resultsText.append("⌛ Fetching recipes...")


        # ---- Changed BigButton 4/25/26 -----
        self.findRecipeButton.setEnabled(False)
        self.findBigButton.setEnabled(False)

        self.worker = RecipeWorker(params)
        self.worker.finished.connect(lambda recipes: self.displayApiResults(recipes, ingredients_str))
        self.worker.error.connect(self.displayApiError)
        self.worker.start()


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
        QMessageBox.information(self, "History", "Feature coming soon!\nWill track your recipe searches.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
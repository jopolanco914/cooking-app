import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import csv
import os


# ---- TO-DO -----
# 1.Finish setting up the second page
# 2. Create a button to read the names of all recipes
# 3. Copy the data twice and clean up the numbers in ingredients to only read the ingredients
# 4. Then in the second copy be able to show how much of each ingredient they actually need
# 5. Then print the instructions


# ---- Doing RN -----
# 1. Checking if the file path can be instantiated within the RecipeWindow class





class RecipeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ---- Creating File Path ----
        self.file_path = "13k-recipes.csv"

        self.setGeometry(700, 700, 300, 300)
        self.setWindowTitle("Recipe Book")





    #  ---- Specific Recipe ----
        self.wantedRecipe = []

    #  ---- Titles ----
        self.recipesTitle = QLabel("Recipe Book", self)
        self.recipesTitle.setStyleSheet("background-color: #ac5633;"
                                        "font-family: Times New Roman; "
                                        "font-weight: bold;"
                                        "font-size: 30px;")

        self.seeFullMenu = QLabel("Full Recipes", self)
        self.seeFullMenu.setStyleSheet("font-size: 15px;")


    #     ---- Input Box ----
        self.searchBox = QLineEdit(self)
        self.searchBox.setPlaceholderText("----Enter Recipe Name----")


    # ---- Push Buttons ----
        self.submit = QPushButton("Search", self)






    # ---- Layout Setup ----
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0,0 ,100 ,0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)


        self.initUI()





    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(self.layout)



        # ---- Adding Functionality to Submit button ----
        self.submit.clicked.connect(self.searchRecipe)



        self.layout.addWidget(self.recipesTitle)
        self.layout.addWidget(self.searchBox)
        self.layout.addWidget(self.submit)

        self.layout.addWidget(self.seeFullMenu)









    # ---- Function to Display Recipes (Hella Long) ----
    def displayRecipes(self):
        with open(self.file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                print(row["Title"])

    def searchRecipe(self):
        recipeName = self.searchBox.text()

        with open(self.file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["Title"].lower() == recipeName.lower():

                    title = row["Title"]
                    ingredients = row["Ingredients"]
                    instructions = row[("Instructions")]

                    formatted_text = (f" Title: {title} \n"
                                      f" Ingredients: {ingredients} \n"
                                      f" Instructions: {instructions} \n")

        print(formatted_text)


def main():
    app = QApplication(sys.argv)
    window = RecipeWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
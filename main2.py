import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QPushButton, QCheckBox, QRadioButton, QButtonGroup, QLineEdit)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):



    def __init__(self):
        super().__init__()

        # ---- List of ingredients ----
        self.inputIngredients = []

        # ---- Declaring all my widgets ----



        # ---- Ingredient Intake ----
        self.layout = QVBoxLayout()
        self.ingredients = QLineEdit(self)
        self.submitButton = QPushButton("Submit", self)
        self.displayLabel = QLabel("Ingredients will appear here")


        # ---- Push Buttons ----
        self.recipeBookButton = QPushButton("Recipes Book", self)
        self.findRecipeButton = QPushButton("Find Recipe", self)
        self.historyButton = QPushButton("History", self)

        # ---- Check Boxes ----
        # self.goatDebateBox = QCheckBox("Is LeBron the GOAT", self)

        # ---- Radio Buttons ----
        self.proteinButton = QRadioButton("Protein Heavy", self)
        self.glutenFreeButton = QRadioButton("Gluten Free", self)
        self.lowCarbsButton = QRadioButton("Low Carbohydrates", self)
        self.vegetarianButton = QRadioButton("Vegetarian", self)


        # ---- Button Group 1 (Type of Meal) ----
        self.dietButtons = QButtonGroup(self)



        # ---- Actual Window ----
        self.setWindowTitle("Barbecue Chicken")
        self.setGeometry(800, 600, 700, 700)
        self.setWindowIcon(QIcon("C:/Users/jpola/OneDrive/Pictures/bdf9ce38c8874272f8afcbb8326fe190.jpg"))


        # ---- Title ---
        title = QLabel("Barbecue Chicken", self)
        title.setFont(QFont("Times New Roman", 20))
        title.setGeometry(0, 0, 700, 100)
        title.setStyleSheet("background-color: #b2ccab;"
                            "text-decoration: underline;")
        title.setAlignment(Qt.AlignCenter)

        # ---- Authors ----
        author = QLabel("Developers: Jose Polanco, Vitalli Protsenko, Bryan Nguyen ", self)
        author.setFont(QFont("Times New Roman", 10))
        author.setGeometry(0, 30, 700, 100)
        author.setAlignment(Qt.AlignCenter)

        #Finish setting up the interface ---- -3/21/26
        self.initUI()

    def initUI(self):
        # ---- Moving QPixmap object here -----
        # pictureSpace = QLabel(self)
        # picture = QPixmap("C:/Users/jpola/OneDrive/Pictures/OPness.jpg")
        # pictureSpace.setPixmap(picture)
        # pictureSpace.setGeometry(15, 100, 50, 50)
        # pictureSpace.setScaledContents(True)


        #  ---- Customizing "Recipe Book" Button ----
        self.recipeBookButton.clicked.connect(self.button1clicked)
        self.recipeBookButton.setGeometry(10, 100, 100, 100)
        self.recipeBookButton.setStyleSheet("background-color: #affae2;")

        #  ---- Customizing "Find Recipe" Button ----
        self.findRecipeButton.clicked.connect(self.button2clicked)
        self.findRecipeButton.setGeometry(180, 100, 100, 100)
        self.findRecipeButton.setStyleSheet("background-color: #affab4;")


        # ---- Customizing "History" Button ----
        self.historyButton.clicked.connect(self.button3clicked)
        self.historyButton.setGeometry(350, 100, 100, 100)
        self.historyButton.setStyleSheet("background-color: #fae8af;")

        # ---- Setting the QCheckBox ---- object
        # self.goatDebateBox.setGeometry(10, 200, 400, 100)
        # self.goatDebateBox.setStyleSheet("font-style: italic;"
        #                                  "font-family: Times New Roman;")
        # self.goatDebateBox.setChecked(False)
        # self.goatDebateBox.stateChanged.connect(self.checkBox)


        # ---- Setting up Radio Buttons ----
        self.proteinButton.setGeometry(10, 250, 150, 100)
        self.glutenFreeButton.setGeometry(10, 300, 150, 100)
        self.lowCarbsButton.setGeometry(10, 350, 170, 100)
        self.vegetarianButton.setGeometry(10, 400, 150, 100)

        self.setStyleSheet("QRadioButton{"
                           "font-size: 15px;"
                           "}")

        self.dietButtons.addButton(self.proteinButton)
        self.dietButtons.addButton(self.glutenFreeButton)
        self.dietButtons.addButton(self.lowCarbsButton)
        self.dietButtons.addButton(self.vegetarianButton)


        self.proteinButton.toggled.connect(self.radio_button_changed)
        self.glutenFreeButton.toggled.connect(self.radio_button_changed)
        self.lowCarbsButton.toggled.connect(self.radio_button_changed)
        self.vegetarianButton.toggled.connect(self.radio_button_changed)


    # ---- Setting up Ingredients intake ----
    # Fixes TO-DO:
    # 1. Make the list interactable so people can scroll down and see their list
    # 2. Fix the UI so it I dont manually set the geometry of all the widgets
    #     - this will allow the program to handle the layout itself
        # ---- Chat Fix ----
        mainLayout = QVBoxLayout()

        # ---- Pushes everything down ----
        mainLayout.addStretch()

        # ---- Create a horizontal layout to push right ----
        bottomRow = QHBoxLayout()
        bottomRow.addStretch()
        bottomRow.addLayout(self.layout)




        mainLayout.addLayout(bottomRow)

        central_widget = QWidget()
        central_widget.setLayout(mainLayout)
        self.setCentralWidget(central_widget)
        central_widget.layout()

        #
        # self.ingredients.setGeometry(200, 225, 150, 50)
        # self.submitButton.setGeometry(350, 225, 100, 50)
        # self.displayLabel.setGeometry(400, 250, 200, 200)

        self.layout.addWidget(self.ingredients)
        self.layout.addWidget(self.submitButton)
        self.layout.addWidget(self.displayLabel)


        self.ingredients.setPlaceholderText("Enter Ingredient")
        self.submitButton.setStyleSheet("font-family: Times New Roman;"
                                        "border: 3px dotted green;")




        self.submitButton.clicked.connect(self.getIngredients)




    # ---- Check Box Functions (Event) ----
    def checkBox(self, state):
        if state == Qt.Checked:
            print("You are not GAY")
        else:
            print("You ARE GAY")

    # ---- Push Button Functions (Events) ----
    def button1clicked(self):
        print("You pressed Recipe Book")
        self.recipeBookButton.setText("Recipe Book Clicked")
        self.recipeBookButton.setGeometry(10, 100, 150, 100)

    def button2clicked(self):
        print("You pressed Find Recipe")
        self.findRecipeButton.setText("Find Recipe Clicked")
        self.findRecipeButton.setGeometry(180, 100, 150, 100)

    def button3clicked(self):
        print("You pressed History")
        self.historyButton.setText("History Clicked")
        self.historyButton.setGeometry(350,100, 150, 100)

    #  ---- Radio Button Functions (Events) ----
    # Fixes TO-DO:
    def radio_button_changed(self):
        button = self.sender()
        if button.isChecked():
            print(f"{button.text()} was pressed")

    # ---- Ingredients Intake Function ----
    def getIngredients(self):
       text = self.ingredients.text()

       if text:
           self.inputIngredients.append(text)

           self.displayLabel.setText(", ".join(self.inputIngredients))

           self.ingredients.clear()

       print(self.inputIngredients)





def main2():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main2()



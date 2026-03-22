import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QPushButton, QCheckBox)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.recipeBookButton = QPushButton("Recipes Book", self)
        self.findRecipeButton = QPushButton("Find Recipe", self)
        self.historyButton = QPushButton("History", self)
        self.goatDebateBox = QCheckBox("Is LeBron the GOAT", self)
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
        self.goatDebateBox.setGeometry(10, 200, 400, 100)
        self.goatDebateBox.setStyleSheet("font-style: italic;"
                                         "font-family: Times New Roman;")
        self.goatDebateBox.setChecked(False)
        self.goatDebateBox.stateChanged.connect(self.checkBox)






    def checkBox(self, state):
        if state == Qt.Checked:
            print("You are not GAY")
        else:
            print("You ARE GAY")

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









def main2():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main2()



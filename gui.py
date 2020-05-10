import sys, os

from functools import partial

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

from be.latin_square import *

ERROR_MSG = "ERROR"

class LatinSquareUI(QMainWindow):
    """LatinSquare's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("Latin Square Validator")
        self.setFixedSize(800, 800)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.pushButton = QtWidgets.QPushButton(self._centralWidget)
        self.player = 1

        # Create the display and the buttons
        self._createLabels()
        self._takeinputs()
        self._createButtons()
        self._createBottomButtons()
        self._createResultLabels()

    def on_box_click(self, label, input):
        print(f"label {label} input {input}")
        row = label // self.n
        column = label % self.n
        print(f"row {row} column {column}")
        print(f"before assignment {self.userInput}")
        self.userInput[row][column] = input
        print(f"after assignment {self.userInput}")

    @pyqtSlot()
    def on_submit_click(self):
        submit = True
        for x in self.userInput:
            if None in x:
                submit = False
        if submit:
            print(self.userInput)
            result = lat_square_sat(self.userInput)
            print('PyQt5 button click submit')
            print("Result from BE {}".format(result))

            if result:
                resultString = "Player {}\nWINS".format(self.player)
            else:
                resultString = "Player 1\nWINS" if self.player == 2 else "Player 2\nWINS"

            self.resultLabel.setText(resultString)
            self.resultLabel.setStyleSheet("color: green;" "font: bold 36px;")

    @pyqtSlot()
    def on_reset_click(self):
        print('PyQt5 button click reset')
        os.execl(sys.executable, sys.executable, *sys.argv)

    def _createResultLabels(self):
        # Rules Label
        self.resultLabel = QtWidgets.QLabel(self._centralWidget)
        self.resultLabel.setGeometry(QtCore.QRect(625, 675, 200, 100))
        self.resultLabel.setText("")

    def _createBottomButtons(self):
        submitButton = QPushButton('Submit', self)
        submitButton.setToolTip('Submit your Latin Square')
        submitButton.move(350,710)
        submitButton.clicked.connect(self.on_submit_click)

        resetButton = QPushButton('Reset', self)
        resetButton.setToolTip('Reset your Latin Square')
        resetButton.move(350,750)
        resetButton.clicked.connect(self.on_reset_click)

    def _createLabels(self):
        # Upper Notice Label
        self.noticeLabel = QtWidgets.QLabel(self._centralWidget)
        self.noticeLabel.setGeometry(QtCore.QRect(20,20, 400, 50))

        # Keeping the text of label empty initially.
        self.noticeLabel.setText("")

        # Rules Label
        self.ruleLabel = QtWidgets.QLabel(self._centralWidget)
        self.ruleLabel.setGeometry(QtCore.QRect(20, 640, 700, 100))
        self.ruleLabel.setText("Rules:\n1. You are only allowed to put the same Pokemon once in each Row or Column\n2. You must fill all boxes")

    def _takeinputs(self):
        # self.n is an int how many n chosen by user
        self.n, done1 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter your Latin Square n: (max 9)', max=9)
        if done1:
            self.noticeLabel.setText(f'Latin Square Succesfully Initialized with\nSize: {self.n}')
            self.userInput = [[None] * self.n for i in range(self.n)]
            self.pushButton.hide()

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {}
        for n in range(self.n**2):
            buttons[n] = (0,0) if n==0 else (n // self.n, n % self.n)
            # print('{} : ({},{})'.format(n, n // self.n, n % self.n))

        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton("")
            self.buttons[btnText].setFixedSize(60, 60)
            # self.buttons[btnText].setIconSize()
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)


# Create a Controller class to connect the GUI and the model
class LatinSquareCtrl:
    """LatinSquare's Controller."""

    def __init__(self, view):
        """Controller initializer."""
        self._view = view
        self._counter = 1
        self._pushedBtn = []
        # Connect signals and slots
        self._connectSignals()

    def _changeIcon(self, btn, btnText):
        """Change image of button."""
        if btnText not in self._pushedBtn:
            btn.setIcon(QIcon(QPixmap("assets/{}.png".format(self._counter))))
            btn.setIconSize(QtCore.QSize(50,50))

            self._view.on_box_click(btnText, self._counter)

            if self._counter == self._view.n:
                self._counter = 1
            else:
                self._counter += 1

            self._view.player = 1 if self._view.player == 2 else 2

            self._pushedBtn.append(btnText)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            btn.clicked.connect(partial(self._changeIcon, btn, btnText))


# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    pycalc = QApplication(sys.argv)

    # Show the LatinSquare's GUI
    view = LatinSquareUI()
    view.show()

    # Create instances of the model and the controller
    LatinSquareCtrl(view=view)
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()

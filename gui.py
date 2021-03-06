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

class CustomDialog(QtWidgets.QDialog):

    def __init__(self, isWin):
        super().__init__()

        self.setWindowTitle("GAME OVER!")

        # QBtn = QtWidgets.QPushButton("Close")

        self.buttonBox = QtWidgets.QPushButton("Close")
        self.buttonBox.clicked.connect(lambda : self.close())

        self.resultText = QtWidgets.QLabel("DRAW!" if isWin else "GAME OVER!")
        self.resultText.setStyleSheet("font: bold 36px;")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.resultText)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

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
        # self._createResultLabels()

    def disconnect_buttons(self):
        for btnText, btn in self.buttons.items():
            btn.clicked.disconnect()

    def on_box_click(self, label, input):

        row = label // self.n
        column = label % self.n
        self.userInput[row][column] = input

        done = True
        for x in self.userInput:
            if 0 in x:
                done = False

        QtWidgets.qApp.processEvents()
        # Adding submission per click
        result = lat_square_sat(self.userInput)
        if not result:
            resultString = "Player 1 WINS" if self.player == 2 else "Player 2 WINS"
            self.titleLabel.setText("Congratulations!")
            self.titleLabel.setStyleSheet("color: green;" "font: bold 32px;")
            self.subTitleLabel.setText(resultString)
            self.subTitleLabel.setStyleSheet("color: red;" "font: bold 24px;")
            QtWidgets.qApp.processEvents()
            self.disconnect_buttons()
            dlg = CustomDialog(False)
            if dlg.exec_():
                on_reset_click()
                print("Success!")
            else:
                print("Result")

        if done:
            resultString = "DRAW!"
            self.titleLabel.setText("Congratulations!")
            self.titleLabel.setStyleSheet("color: green;" "font: bold 32px;")
            self.subTitleLabel.setText(resultString)
            self.subTitleLabel.setStyleSheet("color: red;" "font: bold 24px;")
            QtWidgets.qApp.processEvents()
            self.disconnect_buttons()
            dlg = CustomDialog(True)
            if dlg.exec_():
                on_reset_click()
                print("Success!")
            else:
                print("Result")

    # @pyqtSlot()
    # def on_submit_click(self):
    #     submit = True
    #     for x in self.userInput:
    #         if None in x:
    #             submit = False
    #     if submit:
    #         print(self.userInput)
    #         result = lat_square_sat(self.userInput)
    #         print('PyQt5 button click submit')
    #         print("Result from BE {}".format(result))
    #         resultString = "YOU \nWIN" if result else "YOU \nLOSE:("
    #         self.resultLabel.setText(resultString)
    #         self.resultLabel.setStyleSheet("color: green;" "font: bold 36px;" if result else "color: red;" "font: bold 36px;")

    @pyqtSlot()
    def on_reset_click(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    # def _createResultLabels(self):
    #     # Rules Label
    #     self.resultLabel = QtWidgets.QLabel(self._centralWidget)
    #     self.resultLabel.setGeometry(QtCore.QRect(600, 675, 200, 100))
    #     self.resultLabel.setText("")

    def _createBottomButtons(self):
        # submitButton = QPushButton('Submit', self)
        # submitButton.setToolTip('Submit your Latin Square')
        # submitButton.move(350,710)
        # submitButton.clicked.connect(self.on_submit_click)

        resetButton = QPushButton('Reset', self)
        resetButton.setToolTip('Reset your Latin Square')
        resetButton.move(350,730)
        resetButton.clicked.connect(self.on_reset_click)

    def _createLabels(self):

        self.titleLabel = QtWidgets.QLabel(self._centralWidget)
        self.titleLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setGeometry(QtCore.QRect(200, 80, 400, 50))
        self.titleLabel.setText("Current Player:")
        self.titleLabel.setStyleSheet("color: green;" "font: bold 32px;")

        self.subTitleLabel = QtWidgets.QLabel(self._centralWidget)
        self.subTitleLabel.setGeometry(QtCore.QRect(200, 110, 400, 50))
        self.subTitleLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.subTitleLabel.setAlignment(Qt.AlignCenter)
        self.subTitleLabel.setText(f"Player {self.player}")
        self.subTitleLabel.setStyleSheet("color: red;" "font: bold 24px;")

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
        self.n, done1 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter your Latin Square n: (even only, max 8)', max=8, min=2)
        if done1 and self.n % 2 == 0 and self.n != 0:
            self.noticeLabel.setText(f'Latin Square Succesfully Initialized with\nSize: {self.n}')
            self.userInput = [[0] * self.n for i in range(self.n)]
            self.pushButton.hide()
        elif self.n % 2 != 0:
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            sys.exit()

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {}
        for n in range(self.n**2):
            buttons[n] = (0,0) if n==0 else (n // self.n, n % self.n)

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
            QtWidgets.qApp.processEvents()

            self._view.on_box_click(btnText, self._counter)
            QtWidgets.qApp.processEvents()

            if self._counter == self._view.n:
                self._counter = 1
            else:
                self._counter += 1

            self._view.player = 2 if self._view.player == 1 else 1
            self._view.subTitleLabel.setText(f"Player {self._view.player}")
            self._view.subTitleLabel.setStyleSheet("color: red;" "font: bold 24px;")

            self._pushedBtn.append(btnText)
            QtWidgets.qApp.processEvents()

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

import sys

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

# from be.latin_square import *

ERROR_MSG = "ERROR"

# Create a subclass of QMainWindow to setup the calculator's GUI
class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("PyCalc")
        self.setFixedSize(600, 600)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.pushButton = QtWidgets.QPushButton(self._centralWidget)

        # Create the display and the buttons
        self._createLabels()
        self._takeinputs()
        self._createButtons()
        self._createBottomButtons()
        self._createResultLabels()

    @pyqtSlot()
    def on_submit_click(self):
        # result = lat_square_sat([[1,2,3],[3,1,2],[2,3,1]])
        result = True
        print('PyQt5 button click submit')
        print("Result from BE {}".format(result))
        resultString = "YOU \nWIN" if result else "YOU \nLOSE:("
        self.resultLabel.setText(resultString)

    @pyqtSlot()
    def on_reset_click(self):
        print('PyQt5 button click reset')
        self.resultLabel.setText("")
        # TODO: Add reset

    def _createResultLabels(self):
        # Rules Label
        self.resultLabel = QtWidgets.QLabel(self._centralWidget)
        self.resultLabel.setGeometry(QtCore.QRect(475, 475, 200, 100))
        self.resultLabel.setStyleSheet("color: red;" "font: bold 36px;")
        self.resultLabel.setText("")

    def _createBottomButtons(self):
        submitButton = QPushButton('Submit', self)
        submitButton.setToolTip('Submit your Latin Square')
        submitButton.move(250,500)
        submitButton.clicked.connect(self.on_submit_click)

        resetButton = QPushButton('Reset', self)
        resetButton.setToolTip('Reset your Latin Square')
        resetButton.move(250,540)
        resetButton.clicked.connect(self.on_reset_click)

    def _createLabels(self):
        # Upper Notice Label
        self.noticeLabel = QtWidgets.QLabel(self._centralWidget)
        self.noticeLabel.setGeometry(QtCore.QRect(20, 20, 400, 50))
        # Keeping the text of label empty initially.
        self.noticeLabel.setText("")

        # Rules Label
        self.ruleLabel = QtWidgets.QLabel(self._centralWidget)
        self.ruleLabel.setGeometry(QtCore.QRect(20, 400, 500, 100))
        self.ruleLabel.setText("Rules:\n1. You are only allowed to put the same Pokemon once in each Row or Column\n2. You must fill all boxes")

    def _takeinputs(self):
        # self.n is an int how many n chosen by user
        self.n, done1 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Enter your Latin Square n: (max 9)', max=9)
        if done1:
             self.noticeLabel.setText('Latin Square Succesfully Initialized with\nSize: ' + str(self.n))
             self.pushButton.hide()

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {
            "1": (0, 0),
            "2": (0, 1),
            "3": (0, 2),
            "4": (1, 0),
            "5": (1, 1),
            "6": (1, 2),
            "7": (2, 0),
            "8": (2, 1),
            "9": (2, 2),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton("")
            self.buttons[btnText].setFixedSize(60, 60)
            # self.buttons[btnText].setIconSize()
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)


# Create a Controller class to connect the GUI and the model
class PyCalcCtrl:
    """PyCalc's Controller."""

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
            if self._counter == 1:
                btn.setIcon(QIcon(QPixmap("assets/1-turtwig.png")))
            elif self._counter == 2:
                btn.setIcon(QIcon(QPixmap("assets/2-charmander.png")))
            elif self._counter == 3:
                btn.setIcon(QIcon(QPixmap("assets/3-mudkip.png")))

            if self._counter == 3:
                self._counter = 1
            else:
                self._counter += 1

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
    # Show the calculator's GUI
    view = PyCalcUi()
    view.show()
    # Create instances of the model and the controller
    PyCalcCtrl(view=view)
    # Execute calculator's main loop
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()

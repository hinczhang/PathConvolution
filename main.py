# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ui.MainWindowPro import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    application = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    program = Ui_MainWindow()
    program.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(application.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

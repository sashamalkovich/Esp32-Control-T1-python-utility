from CONTROL_T1_main import mywindow
from PyQt5 import QtWidgets
import sys




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())

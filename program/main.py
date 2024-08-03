from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
import sys
from final_gui import MyGui

app = QApplication(sys.argv)

window = MyGui()

window.show()
app.exec()
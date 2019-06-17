# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class MplWidget(QWidget):
    # Code of MplWidget copied from: https://yapayzekalabs.blogspot.com/2018/11/pyqt5-gui-qt-designer-matplotlib.html
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.setLayout(vertical_layout)
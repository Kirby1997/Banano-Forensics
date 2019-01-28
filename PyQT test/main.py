# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

import networkx as nx

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("interface.ui",self)

        self.setWindowTitle("Banano Forensics")

        self.standardViewBtn.clicked.connect(self.standardGraph)

        self.hierarchyViewBtn.clicked.connect(self.hierarchyGraph)

        self.tracerViewBtn.clicked.connect(self.updateGraph)

        self.exampleBtn.clicked.connect(self.example)

        self.addToolBar(NavigationToolbar(self.mpl_widget.canvas, self))


    def example(self):
        self.mpl_widget.canvas.axes.clear()
        self.mpl_widget.figure.clf()
        self.mpl_widget.canvas.axes = self.mpl_widget.canvas.figure.add_subplot(111)
        x = [i for i in range(100)]
        y = [i ** 0.5 for i in x]
        self.mpl_widget.canvas.axes.plot(x, y, 'r.-')
        self.mpl_widget.canvas.axes.set_title('Square Root Plot')
        self.mpl_widget.canvas.draw_idle()

    def standardGraph(self):
        self.mpl_widget.figure.clf()
        #self.mpl_widget.canvas.axes.clear()
        B = nx.Graph()
        B.add_nodes_from([1, 2, 3, 4], bipartite=0)
        B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

        X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
        Y = set(B) - X

        X = sorted(X, reverse=True)
        Y = sorted(Y, reverse=True)

        pos = dict()
        pos.update((n, (1, i)) for i, n in enumerate(X))  # put nodes from X at x=1
        pos.update((n, (2, i)) for i, n in enumerate(Y))  # put nodes from Y at x=2
        nx.draw(B, pos=pos, with_labels=True)

        #self.mpl_widget.canvas.axes.set_title('standard')
        #self.mpl_widget.canvas.axes.plot()
        self.mpl_widget.canvas.draw_idle()

    def hierarchyGraph(self):
        self.mpl_widget.canvas.axes.clear()
        self.mpl_widget.figure.clf()
        #self.MplWidget.canvas.axes.set_axis_off()
        G = nx.MultiGraph()
        G.add_edge('a', 'b', weight=0)
        G.add_edge('b', 'c', weight=10)
        G.add_edge('b', 'd', weight=10)
        G.add_edge('b', 'e', weight=10)
        G.add_edge('c', 'g', weight=20)
        G.add_edge('c', 'h', weight=20)
        G.add_edge('c', 'i', weight=20)
        G.add_edge('d', 'j', weight=30)
        G.add_edge('d', 'k', weight=30)
        G.add_edge('d', 'l', weight=30)
        G.add_edge('e', 'm', weight=40)
        G.add_edge('e', 'n', weight=40)
        G.add_edge('e', 'o', weight=40)

        zero = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 0]
        ten = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] < 10]
        twenty = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 20]
        thirty = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 30]
        forty = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 40]

        pos = nx.spring_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=700)

        nx.draw_networkx_edges(G, pos, width=6)
        nx.draw_networkx_edges(G, pos, width=6, alpha=0.5, edge_color='b', style='dashed')

        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        # nx.draw(G)
        #plt.axis('off')
        self.mpl_widget.canvas.axes.plot(G)
        self.mpl_widget.canvas.axes.set_title('Hierarchy')
        self.mpl_widget.canvas.draw()

    def updateGraph(self):
        self.mpl_widget.canvas.axes = self.mpl_widget.canvas.figure.add_subplot(111)
        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)

        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.mpl_widget.canvas.axes.clear()

        self.mpl_widget.canvas.axes.plot(t, cosinus_signal)
        self.mpl_widget.canvas.axes.plot(t, sinus_signal)
        self.mpl_widget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')

        self.mpl_widget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.mpl_widget.canvas.draw()

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
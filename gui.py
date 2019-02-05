# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

import networkx as nx

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
from collections import defaultdict
     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("interface.ui",self)

        self.setWindowTitle("Banano Forensics")

        self.standardViewBtn.clicked.connect(self.standardGraph)

        self.hierarchyViewBtn.clicked.connect(self.hierarchyGraph)

        self.tracerViewBtn.clicked.connect(self.updateGraph)

        self.exampleBtn.clicked.connect(self.example)
        
        self.familyBtn.clicked.connect(self.familyGraph)

        self.addToolBar(NavigationToolbar(self.mpl_widget.canvas, self))
        
        self.setAddressBtn.clicked.connect(self.addItem)


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
        
    def familyGraph(self):

        self.mpl_widget.figure.clf()
        #g=nx.read_edgelist('edge_list.txt',create_using=nx.Graph(),nodetype=str)
        
        nodes = defaultdict(list)
        nodes = {'ban_1tc93no6sebhpbh69b877wy3hhhxriqoj5cneq3qbfg9skw63o9wbezrjmka': ['ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_3uiszoq1fca35hjigdbr7p7muo6pfih78s5cubj9e5jbqq5tgz159s7oi8j4', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_3faucb1o9ifundznqw6xn1xkybztz4zfbn4fw95ujfy48ds1ebayzycfsspk', 'ban_3temho9bnim1acqzwwa673yeggeudzo6y857y4t38pmu6jx79amtku8szp3s', 'ban_1dec111t9fpoqspq7gm7w4zw88su5dgs4j1rqttds91ezyyigz7988saftuw', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_1xqyrgt37p6hi3bezgdtxkgq5t8g3eat1bea4uiwrj7rkb61ztxx6yukrz1j', 'ban_1gyrzi4onyafm1ihtzcw5u1gua6pcajymkdmmctfq7bfskjuzqisdsswptt8', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_1u166355pzbk5548zfswf59fxseu9w8y6zk9jomqrrhihh3bu9a8yfygwqbj', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_3ijte5usq7hyawytcuamochcgft6duwjjxnoyfknwnbrsnp1yymqa4me7xne', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_17ejzfncch4463673zqq9kr4kxn5sornnedtbdtzi98kncazt456bw8a5kta', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_3faucb1o9ifundznqw6xn1xkybztz4zfbn4fw95ujfy48ds1ebayzycfsspk', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_3he11oi45zcfe3i65wogyikf1569mu1jcf9kj4o7jojpebmmkbhrpf38qrqx', 'ban_1no3g6ho99zjfgujgkyqmmedi4k9u46yxwnf8bchxs4sof1yg334u8yrt4h5', 'ban_1no4g7k51giqnhscpqm153hamoe956958yrr79sggzgy8wriiemx7owh89ka', 'ban_1tcudnsjjcyposgpwe18dppccknd67yazou58jc3ggpmu9ihepba4o1d9jap', 'ban_3z6nsdpos63dobu5znwhqaxh8a7xzgy99p8uwqx1ymkptyzj5gwjjz4fra7x', 'ban_3z6nsdpos63dobu5znwhqaxh8a7xzgy99p8uwqx1ymkptyzj5gwjjz4fra7x', 'ban_3matchhw9ksc9xfqdhedfn34n8kw6woxr36gnyoop7jc14j7unw9uknhjk8h', 'ban_3ezfbygw1gcmbt7ficnddfwwe1g7unbgfbcoy979wy4agmr4pkdiiamic7ew', 'ban_3z6nsdpos63dobu5znwhqaxh8a7xzgy99p8uwqx1ymkptyzj5gwjjz4fra7x', 'ban_3runnerrxm74165sfmystpktzsyp7eurixwpk59tejnn8xamn8zog18abrda', 'ban_39qa19wke55s46cejgmgcmjfpgp6hrc86sjsi76upxhxtjafoxs7j8kcfod8', 'ban_39qa19wke55s46cejgmgcmjfpgp6hrc86sjsi76upxhxtjafoxs7j8kcfod8', 'ban_3mdoqczk99phi6hhpi4wmuzya5d3gf7djts95aps7p7wtn7t76ohibwkjxzi', 'ban_1dbw7scnhqr9y4h1fgp91jucrhfdedjfuiupjdcc711u4hcdtta6fnnmmbi9', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_39qa19wke55s46cejgmgcmjfpgp6hrc86sjsi76upxhxtjafoxs7j8kcfod8', 'ban_39qa19wke55s46cejgmgcmjfpgp6hrc86sjsi76upxhxtjafoxs7j8kcfod8', 'ban_39qa19wke55s46cejgmgcmjfpgp6hrc86sjsi76upxhxtjafoxs7j8kcfod8', 'ban_3matchhw9ksc9xfqdhedfn34n8kw6woxr36gnyoop7jc14j7unw9uknhjk8h', 'ban_3matchhw9ksc9xfqdhedfn34n8kw6woxr36gnyoop7jc14j7unw9uknhjk8h', 'ban_3matchhw9ksc9xfqdhedfn34n8kw6woxr36gnyoop7jc14j7unw9uknhjk8h', 'ban_3runnerrxm74165sfmystpktzsyp7eurixwpk59tejnn8xamn8zog18abrda', 'ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy', 'ban_3twitegseiodhntduw76t3gsoqsn1ooo4dhpc5p6r5bqx8phbufdr876odh3']}
        g = nx.from_dict_of_lists(nodes)
        nx.write_gexf(g, 'hmm.gexf')

        sp=nx.spring_layout(g)

        nx.draw_networkx(g,pos=sp,with_labels=True,node_size=35,font_size=7)
        #self.mpl_widget.canvas.axes.plot(g)
        self.mpl_widget.canvas.draw_idle()
        print(nx.info(g))
        
        
    def addItem(self):
        value = self.setAddressTxt.text()
        self.setAddressTxt.clear()
        self.listWidget.addItem(value)

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
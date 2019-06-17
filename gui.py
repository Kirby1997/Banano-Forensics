# ------------------------------------------------------
# ---------------------- gui.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUi
import PyQt5
from PyQt5 import QtCore
from enum import Enum
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import networkx as nx
import json
import asyncio
import aiohttp
import scipy # Not directly used but NetworkX tries to use it when running out of memory


# Code to deal with high resolution monitors copied from: https://coad.ca/2017/05/15/one-way-to-deal-with-high-dpi-4k-screens-in-python/
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# For storing runtime variables instead of using globals
class Storage:
    knownaddresses = []
    tipbotaccs = []
    banbetaccs = []
    known_labels = {}
    defaultaddr = ""
    host = ""


async def find_reps(nodes):

    """Go through all the nodes, make an RPC call to the node and request the representative of the account"""
    tasks = []
    for address in nodes:
        tasks.append(get_rep(address))
    ret = []
    while len(tasks):
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            result = task.result()
            if result is not None:
                ret.append(task.result())

    for pair in ret:
        node = pair[0]
        rep = pair[1]

        if rep == "ban_1tipbotgges3ss8pso6xf76gsyqnb69uwcxcyhouym67z7ofefy1jz7kepoy":
            Storage.tipbotaccs.append(node)

        elif rep == "ban_1banbet1hxxe9aeu11oqss9sxwe814jo9ym8c98653j1chq4k4yaxjsacnhc":
            Storage.banbetaccs.append(node)

        pass


async def json_get(payload):
    try:
        connector = aiohttp.TCPConnector(limit=60)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(Storage.host, json=payload, timeout=100) as resp:
                json_resp = await resp.json(content_type=None)
                return json_resp
    except BaseException:
        return None


async def get_rep(address):

    payload = {"action": "account_representative", "account": address}
    resp_json = await json_get(payload)
    try:
        rep = resp_json['representative']
    except:
        rep = 'No rep'
    return address, rep


class PlotType(Enum):
    ALL = 1
    SEND = 2
    RECEIVE = 3


def set_defaults():

    """Set a default host and address and put them into a config file"""
    config = list()
    config.append({
        "host": "http://206.189.120.80:7072",
        "default address": "ban_1tc93no6sebhpbh69b877wy3hhhxriqoj5cneq3qbfg9skw63o9wbezrjmka"
    })
    Storage.host = "http://206.189.120.80:7072"
    Storage.defaultaddr = "ban_1tc93no6sebhpbh69b877wy3hhhxriqoj5cneq3qbfg9skw63o9wbezrjmka"
    with open("config.cfg", "w") as output:
        json.dump(config, output)


def load_config():

    """Import settings from config file in case of use of own node"""
    try:
        with open("config.cfg", "r") as file:
            try:
                config = json.load(file)
                for attribute in config:
                    Storage.host = attribute["host"]
                    Storage.defaultaddr = attribute["default address"]
            except:
                set_defaults()

    except IOError:
        print("config.cfg not found. Creating file and setting to defaults")
        set_defaults()


async def get_next_addresses(node_address, trans, plottype):

    """Create list of descendants for node."""
    address_list = []
    # Do lookup to get next generation
    payload = {"action": "account_history",
               "account": node_address,
               "count": trans}

    history_json = await json_get(payload)

    if plottype == PlotType.ALL:
        for account in history_json['history']:
            address_list.append(account['account'])
    elif plottype == PlotType.SEND:
        for account in history_json['history']:
            if account['type'] == "send":
                address_list.append(account['account'])
    elif plottype == PlotType.RECEIVE:
        for account in history_json['history']:
            if account['type'] == "receive":
                address_list.append(account['account'])
    return address_list


async def calculate_pairs(addresses, trans, plottype):

    """Create list of descendants for each node."""

    tasks = []
    for address in addresses:
        payload = {"action": "account_history",
                   "account": address,
                   "count": trans}
        tasks.append(json_get(payload))
    ret = []
    while len(tasks):
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            result = task.result()
            if result is not None:
                ret.append(task.result())
    lock = asyncio.Lock()

    next_addresses = []
    potential_pairs = {}
    address_list = []
    for history_json in ret:
        if plottype == PlotType.ALL:
            for account in history_json['history']:
                address_list.append(account['account'])
        elif plottype == PlotType.SEND:
            for account in history_json['history']:
                if account['type'] == "send":
                    address_list.append(account['account'])
        elif plottype == PlotType.RECEIVE:
            for account in history_json['history']:
                if account['type'] == "receive":
                    address_list.append(account['account'])
        new_connections = []
        for potential_address in address_list:
            if potential_address not in potential_pairs.keys():
                new_connections.append(potential_address)
        account = history_json['account']
        await lock.acquire()
        try:
            potential_pairs[account] = new_connections
            next_addresses = next_addresses + new_connections
            address_list = []
        finally:
            lock.release()

    return potential_pairs, next_addresses


class MatplotlibWidget(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        loadUi("interface.ui", self)

        self.setWindowTitle("Banano Forensics")

        self.receiveViewBtn.clicked.connect(self.receive_graph)
        self.sentViewBtn.clicked.connect(self.sent_graph)
        self.banGraphBtn.clicked.connect(self.full_graph)

        self.setNoTransBtn.clicked.connect(self.set_max_trans)
        self.setAddressBtn.clicked.connect(self.set_address)
        self.setDepthBtn.clicked.connect(self.set_max_generations)

        self.addressListBtn.clicked.connect(self.load_addresses)

        self.addToolBar(NavigationToolbar(self.mpl_widget.canvas, self))

        self.addressValue.setText(Storage.defaultaddr)
        self.transValue.setText("2")  # 2 as default value
        self.depthValue.setText("2")  # 2 as default value

        self.FontSizeSlider.valueChanged.connect(self.update_slider_label)
        self.FontSizeSlider.setValue(5)
        self.FontSizeLbl.setText("Font size = " + str(self.FontSizeSlider.value()))

    def receive_graph(self):
        self.statusBar().showMessage('Plotting receive graph in progress...')
        plottype = PlotType.RECEIVE
        self.plot_graph(plottype)
        self.statusBar().showMessage('Plotted receive graph')

    def sent_graph(self):
        self.statusBar().showMessage('Plotting send graph in progress...')
        plottype = PlotType.SEND
        self.plot_graph(plottype)
        self.statusBar().showMessage('Plotted send graph')

    def full_graph(self):
        self.statusBar().showMessage('Plotting full graph in progress...')
        plottype = PlotType.ALL
        self.plot_graph(plottype)
        self.statusBar().showMessage('Plotted full graph')

    def plot_graph(self, plottype):
        """Plot the graph into the matplotlib widget"""
        knownaddresses = Storage.knownaddresses
        known_labels = Storage.known_labels
        self.mpl_widget.figure.clf()
        self.mpl_widget.canvas.axes = self.mpl_widget.canvas.figure.add_subplot(111)
        self.mpl_widget.canvas.axes.axis('off')
        address = self.get_address()
        max_gens = self.get_max_generations()
        trans = self.get_max_trans()

        completed_nodes = {address: []}
        addresses_in_progress = list()

        # To start we have no completed nodes and have one
        # address to work on
        addresses_in_progress.append(address)
        for generation in range(int(max_gens)):
            try:
                calculated_pairs = asyncio.run(calculate_pairs(addresses_in_progress, trans, plottype))
                completed_nodes = {**completed_nodes, **calculated_pairs[0]}
                next_addresses = calculated_pairs[1]
                addresses_in_progress = next_addresses
            except:
                print("Network too big to generate more nodes")
                pass

        print("COMPLETED NODES")

        g = nx.from_dict_of_lists(completed_nodes)
        nx.write_gexf(g, "{}.gexf".format(address))
        print("Saved Gephi graph as {}.gexf".format(address))
        sp = nx.spring_layout(g, iterations=100, scale=1)

        show_labels = self.get_show_labels()
        labels = {}

        for node in known_labels:
            try:
                if node in g.nodes():
                    labels[node] = known_labels[node]
            except:
                print("No known addresses to look for")
        fontsize = self.FontSizeSlider.value()
        nx.draw_networkx(g, pos=sp, with_labels=show_labels, font_size=fontsize, node_size=10, node_color="r")
        try:
            # use Asyncio to get all the representatives of nodes and append them to lists
            asyncio.run(find_reps(g.nodes()))
            nx.draw_networkx(g, pos=sp, with_labels=False, nodelist=Storage.tipbotaccs, node_size=10, node_color='y')
            nx.draw_networkx(g, pos=sp, with_labels=False, nodelist=Storage.banbetaccs, node_size=10, node_color='c')
        except:
            print("Sockets limit reached")
        if knownaddresses != 1:
            pair = 0
            while pair < len(knownaddresses):

                if g.has_node(knownaddresses[pair][0]):
                    nx.draw_networkx(g, pos=sp, with_labels=False, nodelist=[knownaddresses[pair][0]], node_size=12, node_color='b',
                                     font_color='b')
                    nx.draw_networkx_labels(g, sp, labels, font_size=fontsize, font_color='b')
                    print(nx.shortest_path(g, address, knownaddresses[pair][0]))
                pair += 1
        nx.draw_networkx(g, pos=sp, with_labels=False, nodelist=[address], node_size=10, node_color='g')
        self.mpl_widget.canvas.draw_idle()
        print("Number of nodes: " + str(len(g)))
        Storage.tipbotaccs.clear()
        Storage.banbetaccs.clear()

    def update_slider_label(self):
        value = self.FontSizeSlider.value()
        self.FontSizeLbl.setText("Font Size = " + str(value))

    def set_address(self):
        value = self.setAddressTxt.text()
        if value == "":
            address = "ban_1tc93no6sebhpbh69b877wy3hhhxriqoj5cneq3qbfg9skw63o9wbezrjmka"
            self.addressValue.setText(address)
        else:
            address = value
            self.addressValue.setText(address)

    def get_address(self):
        address = self.addressValue.text()
        return address

    def set_max_trans(self):
        max_trans = self.noTransBox.text()
        self.transValue.setText(max_trans)


    def get_max_trans(self):
        trans = self.transValue.text()
        return trans

    def set_max_generations(self):
        depth = self.depthBox.text()
        self.depthValue.setText(depth)

    def get_max_generations(self):
        depth = self.depthValue.text()
        return depth

    def get_show_labels(self):
        labels = self.labelsToggle.isChecked()
        return labels

    def load_addresses(self):
        print("Loading known addresses")
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0]:
            file = open(filename[0], 'r')
            linenum = 0
            for line in file:
                linenum += linenum
                keypair = line.strip()
                keypair = keypair.split(":")
                Storage.knownaddresses.append(keypair)
                try:
                    Storage.known_labels[keypair[0]] = keypair[1]
                    self.addressListBox.append(keypair[0] + " - " + keypair[1])
                except:
                    print("inconsistency at line {} containing \"{}\" ".format(linenum, line))
                    print("Formatting should be address:label")
        print("Loaded file")


def main():
    load_config()
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()


main()

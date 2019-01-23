%matplotlib inline
import matplotlib.pyplot as plt
import networkx as nx

G=nx.MultiGraph()
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

nx.draw_networkx_edges(G, pos, edgelist=elarge,
                       width=6)
nx.draw_networkx_edges(G, pos, edgelist=esmall,
                       width=6, alpha=0.5, edge_color='b', style='dashed')



nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
#nx.draw(G)
plt.axis('off')
plt.show()

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes

def get_graph(nodes):

    G = nx.Graph()
    G.add_nodes_from(np.arange(0, nodes, 1))

    # Create random positions in the graph. Distance will be calculated from positions
    # Note: Dwave and other solvers require a complete graph
    for i in range(nodes):
        G.nodes[i]['pos'] = (np.random.uniform(0, 10), np.random.uniform(0, 10))

    elist = set()
    for i in range(nodes):
        for t in range(i + 1,nodes):
            y1=G.nodes[i]['pos'][1]
            x1=G.nodes[i]['pos'][0]
            y2=G.nodes[t]['pos'][1]
            x2=G.nodes[t]['pos'][0]
            dist = np.sqrt(((x2-x1)**2)+((y2-y1)**2))
            _tuple = (i, t, dist)
            elist.add(_tuple)

    # tuple is (i,j,weight) where (i,j) is the edge
    G.add_weighted_edges_from(elist)

    return G

def get_cost_matrix(G, nodes):
    w = np.zeros([nodes,nodes])
    for i in range(nodes):
        for j in range(nodes):
            temp = G.get_edge_data(i,j,default=0)
            if temp != 0:
                w[i,j] = temp['weight']
    return w

def calculate_cost(cost_matrix, solution):
    cost = 0
    for i in range(len(solution)):
        a = i % len(solution)
        b = (i + 1) % len(solution)
        cost += cost_matrix[solution[a]][solution[b]]

    return cost

def draw_tsp_solution(G, order, solver, end_time):

    colors = ['r' for node in G.nodes()]

    default_axes = plt.axes(frameon=True)

    G2 = G.copy()
    G2.remove_edges_from(list(G.edges))
    n = len(order)
    for i in range(n-1):
        j = (i + 1) % n
        G2.add_edge(order[i], order[j])

    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx(G2, node_color=colors, node_size=600, alpha=.8, ax=default_axes, pos=pos)
    plt.title(solver)
    # Print png or show in screen
    #plt.savefig(solver + '_' + str(end_time) + '.png')
    #plt.clf()
    plt.show()

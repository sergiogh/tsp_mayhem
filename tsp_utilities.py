
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes

def get_graph(nodes):

    G = nx.Graph()
    G.add_nodes_from(np.arange(0, nodes, 1))

    # Create random edges.
    # Note: Dwave and other solvers require a complete graph
    elist = set()
    for i in range(nodes):
        for t in range(i + 1,nodes):
            _tuple = (i, t, np.random.rand() * 10)
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
    pos = nx.spring_layout(G)
    default_axes = plt.axes(frameon=True)

    G2 = G.copy()
    G2.remove_edges_from(list(G.edges))
    n = len(order)
    for i in range(n-1):
        j = (i + 1) % n
        G2.add_edge(order[i], order[j])


    nx.draw_networkx(G2, node_color=colors, node_size=600, alpha=.8, ax=default_axes, pos=pos)
    plt.title(solver)
    # Print png or show in screen
    #plt.savefig(solver + '_' + str(end_time) + '.png')
    #plt.clf()
    plt.show()

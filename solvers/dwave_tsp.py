
import dwave_networkx as dnx
import dimod

class Dwave_tsp:

    def calculate(self, G, cost_matrix, starting_node):

        route = []
        for i in list(G):
            route.append(i)

        return route

        sapi_token = ''
        dwave_url = 'https://cloud.dwavesys.com/sapi'

        #nx.draw_networkx(G, node_color=colors, node_size=400, alpha=.8, ax=default_axes, pos=pos)
        # Test with https://docs.ocean.dwavesys.com/en/latest/docs_dnx/reference/algorithms/tsp.html
        route = dnx.traveling_salesperson(G, dimod.ExactSolver(), start=starting_node)

        return route

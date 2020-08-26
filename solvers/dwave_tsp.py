import dwave_networkx as dnx
import networkx as nx
import dimod


class Dwave_tsp:
    def calculate(self, G, cost_matrix, starting_node):

        sapi_token = ""
        dwave_url = "https://cloud.dwavesys.com/sapi"

        dnx.traveling_salesperson(G, dimod.ExactSolver(), start=0)  # doctest: +SKIP

        # nx.draw_networkx(G, node_color=colors, node_size=400, alpha=.8, ax=default_axes, pos=pos)
        # Test with https://docs.ocean.dwavesys.com/en/latest/docs_dnx/reference/algorithms/tsp.html
        route = dnx.traveling_salesperson(G, dimod.ExactSolver(), start=starting_node)

        return route

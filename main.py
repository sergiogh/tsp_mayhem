import time
import importlib

from tsp_utilities import *

##############################################
## ADD HERE YOUR NEW SOLVERS CLASSES #########
##############################################
active_solvers = ["Bruteforce",
                  #"Dwave_tsp",
                  "TSP_genetico"]
##############################################
##############################################

def main():

    starting_node = 0
    nodes = 5

    G = get_graph(nodes)
    cost_matrix = get_cost_matrix(G, nodes)

    for solver_ in active_solvers:
        ClassName = getattr(importlib.import_module("solvers."+solver_.lower()), solver_)
        instance = ClassName()
        route = instance.calculate(G, cost_matrix, starting_node)
        print("Route for %s:" % solver_)
        print(route)
        print("Cost: %s" % calculate_cost(cost_matrix, route))
        draw_tsp_solution(G, route)


if __name__ == '__main__':
    main()


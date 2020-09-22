import time
import importlib

from tsp_utilities import *

##############################################
## ADD HERE YOUR NEW SOLVERS CLASSES #########
##############################################
active_solvers = ["Bruteforce",
                  "Dwave_tsp",
                  "TSP_genetico",
                  "Numpyeigensolver",
                  "Vqe"]

active_solvers = ["Admm", "Bruteforce"]

##############################################
##############################################

def main():


    nodes = 3
    starting_node = 0
    G = get_graph(nodes)
    cost_matrix = get_cost_matrix(G, nodes)

    for solver_ in active_solvers:

        ClassName = getattr(importlib.import_module("solvers."+solver_.lower()), solver_)
        instance = ClassName()
        print("Route for %s:" % solver_)
        start_time = time.time()
        route = instance.calculate(G, cost_matrix, starting_node)
        end_time = time.time()
        calculation_time = end_time - start_time
        print(route)
        print("%s Solution - Cost: %s - Calculation Time: %s" % (solver_, calculate_cost(cost_matrix, route), calculation_time))
        #draw_tsp_solution(G, route, solver_, end_time)


if __name__ == '__main__':
    main()

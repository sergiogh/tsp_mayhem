import numpy as np

import dwave_networkx as dnx

import dimod
from dwave.system import LeapHybridSampler


# Inspired on https://github.com/mstechly/quantum_tsp/blob/master/src/dwave_tsp_solver.py

class Dwave_hybrid:
    def calculate(self, G, cost_matrix, starting_node):

        sampler = LeapHybridSampler()
        result = dnx.traveling_salesman(G, sampler, start=0)

        return result

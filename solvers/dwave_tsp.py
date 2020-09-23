import numpy as np

import dwave_networkx as dnx
import networkx as nx
import dimod

from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import EmbeddingComposite   # Library to embed our problem onto the QPU physical graph

# Inspired on https://github.com/mstechly/quantum_tsp/blob/master/src/dwave_tsp_solver.py

class Dwave_tsp:
    def calculate(self, G, cost_matrix, starting_node):

        if(len(G.nodes) > 9):
            print("Dwave 2000Q systems can only embed up to 9 nodes on the lattice with current algorithm")
            return []

        #sapi_token = ""
        #dwave_url = "https://cloud.dwavesys.com/sapi"

        #bqm = dimod.BinaryQuadraticModel.from_networkx_graph(G, 'BINARY')
        Q = dnx.algorithms.traveling_salesman_qubo(G)
        bqm = dimod.BinaryQuadraticModel.from_qubo(Q)

        response = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_6')).sample(bqm, chain_strength=600)

        self.decode_solution(response, cost_matrix)
        print(self.solution)
        print(self.distribution)

        # nx.draw_networkx(G, node_color=colors, node_size=400, alpha=.8, ax=default_axes, pos=pos)
        # Test with https://docs.ocean.dwavesys.com/en/latest/docs_dnx/reference/algorithms/tsp.html
        #route = dnx.traveling_salesperson(G, dimod.ExactSolver(), start=starting_node)

        return self.solution


    def binary_state_to_points_order(self, binary_state):
        points_order = []
        number_of_points = int(np.sqrt(len(binary_state)))
        for p in range(number_of_points):
            for j in range(number_of_points):
                if binary_state[(number_of_points) * p + j] == 1:
                    points_order.append(j)
        return points_order

    def decode_solution(self, response, cost_matrix):
        n = len(cost_matrix)
        distribution = {}
        min_energy = response.record[0].energy

        for record in response.record:
            sample = record[0]
            solution_binary = [node for node in sample]
            solution = self.binary_state_to_points_order(solution_binary)
            distribution[tuple(solution)] = (record.energy, record.num_occurrences)
            if record.energy <= min_energy:
                self.solution = solution
        self.distribution = distribution

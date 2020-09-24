import numpy as np

import dwave_networkx as dnx
import networkx as nx
import dimod

from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import AutoEmbeddingComposite   # Library to embed our problem onto the QPU physical graph

# Inspired on https://github.com/mstechly/quantum_tsp/blob/master/src/dwave_tsp_solver.py

class Dwave:
    def calculate(self, G, cost_matrix, starting_node):

        if(len(G.nodes) > 9):
            print("Dwave 2000Q systems can only embed up to 9 nodes on the lattice with current algorithm")
            return []

        #sapi_token = ""
        #dwave_url = "https://cloud.dwavesys.com/sapi"

        #bqm = dimod.BinaryQuadraticModel.from_networkx_graph(G, 'BINARY')
        Q = dnx.algorithms.traveling_salesman_qubo(G)
        #bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
        bqm = dimod.BinaryQuadraticModel.from_networkx_graph(G, 'BINARY', edge_attribute_name='weight')

        #response = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_6')).sample(bqm, chain_strength=30)

        sampler = AutoEmbeddingComposite(DWaveSampler(solver='DW_2000Q_6'))
        route = dnx.traveling_salesperson(G, sampler, lagrange=90.0, weight='weight')

        #self.decode_solution(response, cost_matrix)
        #print(self.solution)
        #print(self.distribution)

        # nx.draw_networkx(G, node_color=colors, node_size=400, alpha=.8, ax=default_axes, pos=pos)
        # Test with https://docs.ocean.dwavesys.com/en/latest/docs_dnx/reference/algorithms/tsp.html
        #route_classic = dnx.traveling_salesperson(G, dimod.ExactSolver(), start=starting_node)
        #print("Exact classical solver:")
        #print(route_classic)
        #print("Full Q Annealer solver:")
        print(route)
        #return []
        return route

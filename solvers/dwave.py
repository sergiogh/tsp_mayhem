import numpy as np

import dwave_networkx as dnx
import networkx as nx
import dimod

from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import AutoEmbeddingComposite, EmbeddingComposite   # Library to embed our problem onto the QPU physical graph

# Inspired on https://github.com/mstechly/quantum_tsp/blob/master/src/dwave_tsp_solver.py
# ref: https://docs.ocean.dwavesys.com/en/latest/docs_dnx/reference/algorithms/tsp.html

class Dwave:
    def calculate(self, G, cost_matrix, starting_node):

        if(len(G.nodes) > 9):
            print("Dwave 2000Q systems can only embed up to 9 nodes on the lattice with current algorithm")
            return []


        # Different tests to make it happen!
        #Q = dnx.algorithms.traveling_salesman_qubo(G)
        #bqm = dimod.BinaryQuadraticModel.from_networkx_graph(G, 'BINARY', edge_attribute_name='weight')
        #response = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_6')).sample(bqm, chain_strength=300, num_reads=1000)
        #print(response)
        sampler = AutoEmbeddingComposite(DWaveSampler(solver='DW_2000Q_6'))
        #sampleset = dimod.SimulatedAnnealingSampler().sample_qubo(Q)
        result = dnx.traveling_salesperson(G, sampler, start = starting_node, lagrange=90.0, weight='weight')

        return result

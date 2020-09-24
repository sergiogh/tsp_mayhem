import numpy as np

import dwave_networkx as dnx
import networkx as nx
import dimod
import hybrid
from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import EmbeddingComposite   # Library to embed our problem onto the QPU physical graph

# Inspired on https://github.com/mstechly/quantum_tsp/blob/master/src/dwave_tsp_solver.py

class Dwave_hybrid:
    def calculate(self, G, cost_matrix, starting_node):

        if(len(G.nodes) > 9):
            print("Dwave 2000Q systems can only embed up to 9 nodes on the lattice with current algorithm")
            return []

        bqm = dimod.BinaryQuadraticModel.from_networkx_graph(G, 'BINARY', edge_attribute_name='weight')

        iteration = hybrid.Race(
            hybrid.InterruptableTabuSampler(),
            hybrid.EnergyImpactDecomposer(size=50, rolling=True, rolling_history=0.15)
            | hybrid.QPUSubproblemAutoEmbeddingSampler()
            | hybrid.SplatComposer()
        ) | hybrid.ArgMin() | hybrid.TrackMin(output=True)

        main = hybrid.Loop(iteration, max_iter=10, convergence=3)

        # run the workflow
        init_state = hybrid.State.from_sample(hybrid.min_sample(bqm), bqm)
        solution = main.run(init_state).result()

        # show results
        print("Solution: sample={.samples.first}".format(solution))



        return []
        #return route
        #return self.solution

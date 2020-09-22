import numpy as np

import dwave_networkx as dnx
import networkx as nx
import dimod

from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import EmbeddingComposite   # Library to embed our problem onto the QPU physical graph

# Inspired on https://github.com/mstechly/quantum_tsp/blob/master/src/dwave_tsp_solver.py

class Dwave_tsp:
    def calculate(self, G, cost_matrix, starting_node):

        max_distance = np.max(np.array(cost_matrix))
        scaled_distance_matrix = cost_matrix / max_distance
        self.distance_matrix = scaled_distance_matrix
        self.constraint_constant = 400
        self.cost_constant = 10
        self.chainstrength = 800
        self.numruns = 1000
        self.qubo_dict = {}
        #self.sapi_token = sapi_token
        #self.url = url
        self.add_cost_objective()
        print("===== COST OBJECTIVE ====")
        print(self.qubo_dict)
        self.add_time_constraints()
        print("===== TIME CONSTRAINTS ====")
        print(self.qubo_dict)
        self.add_position_constraints()
        print("===== POSITION CONSTRAINTS ====")
        print(self.qubo_dict)



        sapi_token = ""
        dwave_url = "https://cloud.dwavesys.com/sapi"

        #response = EmbeddingComposite(DWaveSampler(token=self.sapi_token, endpoint=self.url, solver='DW_2000Q_2_1')).sample_qubo(self.qubo_dict, chain_strength=self.chainstrength, num_reads=self.numruns)
        #response = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_6')).sample_qubo(self.qubo_dict, chain_strength=800, num_reads=1000)
        #print(response)
        #self.decode_solution(response, cost_matrix)
        #print(self.solution)
        #print(self.distribution)

        # nx.draw_networkx(G, node_color=colors, node_size=400, alpha=.8, ax=default_axes, pos=pos)
        # Test with https://docs.ocean.dwavesys.com/en/latest/docs_dnx/reference/algorithms/tsp.html
        #route = dnx.traveling_salesperson(G, dimod.ExactSolver(), start=starting_node)

        #return self.solution


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


    def add_cost_objective(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    qubit_a = t * n + i
                    qubit_b = (t + 1) % n * n + j
                    self.qubo_dict[(qubit_a, qubit_b)] = self.cost_constant * self.distance_matrix[i][j]

    def add_time_constraints(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                qubit_a = t * n + i
                if (qubit_a, qubit_a) not in self.qubo_dict.keys():
                    self.qubo_dict[(qubit_a, qubit_a)] = -self.constraint_constant
                else:
                    self.qubo_dict[(qubit_a, qubit_a)] += -self.constraint_constant
                for j in range(n):
                    qubit_b = t * n + j
                    if i!=j:
                        self.qubo_dict[(qubit_a, qubit_b)] = 2 * self.constraint_constant


    def add_position_constraints(self):
        n = len(self.distance_matrix)
        for i in range(n):
            for t1 in range(n):
                qubit_a = t1 * n + i
                if (qubit_a, qubit_a) not in self.qubo_dict.keys():
                    self.qubo_dict[(qubit_a, qubit_a)] = -self.constraint_constant
                else:
                    self.qubo_dict[(qubit_a, qubit_a)] += -self.constraint_constant
                for t2 in range(n):
                    qubit_b = t2 * n + i
                    if t1!=t2:
                        self.qubo_dict[(qubit_a, qubit_b)] = 2 * self.constraint_constant

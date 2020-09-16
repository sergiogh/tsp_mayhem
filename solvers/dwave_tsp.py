import dwave_networkx as dnx
import networkx as nx
import dimod

from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import EmbeddingComposite   # Library to embed our problem onto the QPU physical graph


from qiskit.optimization.problems import QuadraticProgram
from qiskit.optimization.applications.ising import tsp

# Inspired on https://github.com/mstechly/quantum_tsp/blob/master/src/dwave_tsp_solver.py

class Dwave_tsp:
    def calculate(self, G, cost_matrix, starting_node):

        sapi_token = ""
        dwave_url = "https://cloud.dwavesys.com/sapi"


        # Create nodes array for the TSP solver in Qiskit
        coords = []
        for node in G.nodes:
            coords.append(G.nodes[node]['pos'])

        tsp_instance = tsp.TspData(name = "TSP", dim = len(G.nodes), coord = coords, w = cost_matrix)
        qubitOp, offset = tsp.get_operator(tsp_instance)
        qp = QuadraticProgram()
        qp.from_ising(qubitOp, offset, linear=True)



        #response = EmbeddingComposite(DWaveSampler(token=self.sapi_token, endpoint=self.url, solver='DW_2000Q_2_1')).sample_qubo(self.qubo_dict, chain_strength=self.chainstrength, num_reads=self.numruns)
        response = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_5')).sample_qubo(qp, chain_strength=800, num_reads=1000)
        self.decode_solution(response, cost_matrix)
        print(self.solution)
        print(self.distribution)

        # nx.draw_networkx(G, node_color=colors, node_size=400, alpha=.8, ax=default_axes, pos=pos)
        # Test with https://docs.ocean.dwavesys.com/en/latest/docs_dnx/reference/algorithms/tsp.html
        #route = dnx.traveling_salesperson(G, dimod.ExactSolver(), start=starting_node)

        return route


    def binary_state_to_points_order(binary_state):
        points_order = []
        number_of_points = int(np.sqrt(len(binary_state)))
        for p in range(number_of_points):
            for j in range(number_of_points):
                if binary_state[(number_of_points) * p + j] == 1:
                    points_order.append(j)
        return points_order

    def decode_solution(response, cost_matrix):
        n = len(cost_matrix)
        distribution = {}
        min_energy = response.record[0].energy

        for record in response.record:
            sample = record[0]
            solution_binary = [node for node in sample]
            solution = binary_state_to_points_order(solution_binary)
            distribution[tuple(solution)] = (record.energy, record.num_occurrences)
            if record.energy <= min_energy:
                self.solution = solution
        self.distribution = distribution

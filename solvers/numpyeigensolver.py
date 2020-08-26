
from qiskit.aqua.algorithms import NumPyEigensolver
from qiskit.optimization.applications.ising import tsp
from qiskit.optimization.applications.ising.common import sample_most_likely

class Numpyeigensolver:

    def calculate(self, G, cost_matrix, starting_node = 0):

        # Create nodes array for the TSP solver in Qiskit
        G.nodes[0]['pos']
        coords = []
        for node in G.nodes:
            print(node)
            coords.append(G.nodes[0]['pos'])

        tsp_instance = tsp.TspData(name = "TSP", dim = len(G.nodes), coord = coords, w = cost_matrix)

        qubitOp, offset = tsp.get_operator(tsp_instance)


        ee = NumPyEigensolver(qubitOp, k=1)
        result = ee.run()


        x = sample_most_likely(result['eigenstates'][0])

        return tsp.get_tsp_solution(x)

import numpy as np
from qiskit import Aer
from qiskit.aqua import aqua_globals, QuantumInstance
from qiskit.aqua.components.optimizers import SPSA, COBYLA
from qiskit.aqua.algorithms import VQE, NumPyMinimumEigensolver
from qiskit.circuit.library import TwoLocal
from qiskit.optimization.applications.ising import tsp
from qiskit.optimization.applications.ising.common import sample_most_likely

class Vqe:

    def calculate(self, G, cost_matrix, starting_node = 0):

        # Create nodes array for the TSP solver in Qiskit
        coords = []
        for node in G.nodes:
            coords.append(G.nodes[node]['pos'])

        tsp_instance = tsp.TspData(name = "TSP", dim = len(G.nodes), coord = coords, w = cost_matrix)

        qubitOp, offset = tsp.get_operator(tsp_instance)

        #print(qubitOp.print_details())

        #backend = Aer.get_backend('statevector_simulator')
        backend = Aer.get_backend('qasm_simulator')
        quantum_instance = QuantumInstance(backend)

        #optimizer = SPSA(maxiter=400)
        optimizer = COBYLA(maxiter=300, rhobeg=3, tol=1.5)
        #ry = TwoLocal(qubitOp.num_qubits, 'ry', 'cz', reps=3, entanglement='linear')
        vqe = VQE(operator=qubitOp, optimizer=optimizer, quantum_instance=quantum_instance)

        result = vqe.run(quantum_instance)

        x = sample_most_likely(result.eigenstate)

        if(tsp.tsp_feasible(x)):
            z = tsp.get_tsp_solution(x)
            print('solution:', z)
            return z
        else:
            print('no solution:', x)
            return []


    def iterations(_eval_count, param_set, means, estimator_error):
        print(_eval_count)
        print(param_set)
        print(means)
        print(estimator_error)

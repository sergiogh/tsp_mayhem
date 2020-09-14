import numpy as np
from qiskit import Aer
from qiskit.aqua import aqua_globals, QuantumInstance
from qiskit.aqua.algorithms import QAOA, VQE, NumPyMinimumEigensolver
from qiskit.aqua.components.optimizers import SPSA, COBYLA
from qiskit.optimization.problems import QuadraticProgram
from qiskit.optimization.algorithms import MinimumEigenOptimizer, RecursiveMinimumEigenOptimizer
from qiskit.optimization.applications.ising import tsp
from qiskit.optimization.applications.ising.common import sample_most_likely


class OptimizedQAOA:

    def calculate(self, G, cost_matrix, starting_node = 0):

        # Create nodes array for the TSP solver in Qiskit
        coords = []
        for node in G.nodes:
            coords.append(G.nodes[node]['pos'])

        tsp_instance = tsp.TspData(name = "TSP", dim = len(G.nodes), coord = coords, w = cost_matrix)

        qubitOp, offset = tsp.get_operator(tsp_instance)


        backend = Aer.get_backend('qasm_simulator')
        quantum_instance = QuantumInstance(backend)

        optimizer = COBYLA(maxiter=300, rhobeg=3, tol=1.5)

        # Define Minimum Eigen Solvers
        minimum_eigen_solver = QAOA(quantum_instance = quantum_instance, optimizer=optimizer, operator=qubitOp)
        #minimum_eigen_solver = VQE(quantum_instance=quantum_instance, optimizer=optimizer, operator=qubitOp)
        exact_mes = NumPyMinimumEigensolver()

        # Create the optimizers so we can plug our Quadratic Program
        minimum_eigen_optimizer = MinimumEigenOptimizer(minimum_eigen_solver)
        #vqe = MinimumEigenOptimizer(vqe_mes)
        exact = MinimumEigenOptimizer(exact_mes)
        rqaoa = RecursiveMinimumEigenOptimizer(min_eigen_optimizer=minimum_eigen_optimizer,
                                               min_num_vars=1,
                                               min_num_vars_optimizer=exact)

        # Create QUBO based on qubitOp from the TSP
        qp = QuadraticProgram()
        qp.from_ising(qubitOp, offset, linear=True)

        result = rqaoa.solve(qp)

        if(tsp.tsp_feasible(result.x)):
            z = tsp.get_tsp_solution(result.x)
            print('solution:', z)
            return z
        else:
            print('no solution:', result.x)
            return []


    def iterations(_eval_count, param_set, means, estimator_error):
        print(_eval_count)
        print(param_set)
        print(means)
        print(estimator_error)

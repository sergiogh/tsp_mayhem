import numpy as np

from qiskit.aqua.algorithms import VQE, NumPyMinimumEigensolver
from qiskit.circuit.library import TwoLocal, RealAmplitudes
from qiskit.optimization.applications.ising import tsp

import pennylane as qml
from pennylane.operation import Tensor

class Pennylane:

    def calculate(self, G, cost_matrix, starting_node = 0):

        # Create nodes array for the TSP solver in Qiskit
        coords = []
        for node in G.nodes:
            coords.append(G.nodes[node]['pos'])

        tsp_instance = tsp.TspData(name = "TSP", dim = len(G.nodes), coord = coords, w = cost_matrix)
        qubitOp, offset = tsp.get_operator(tsp_instance)
        print("Qubits needed: ", qubitOp.num_qubits)
        qubitOp.to_dict()['paulis']

        dev = qml.device('default.qubit', wires=qubitOp.num_qubits)

        def circuit(params, wires):
            for i in wires:
                qml.Rot(*params[i], wires=i)
            qml.CNOT(wires=[2, 3])
            qml.CNOT(wires=[2, 0])
            qml.CNOT(wires=[3, 1])

        @qml.qnode(dev)
        def final_circ(params, num_qubits):
            circuit(params, range(num_qubits))
            return qml.probs(wires=range(num_qubits))

        # Prepare Hamiltonian in the shape Pennylane likes
        coeffs = []
        obs = []
        for i in qubitOp.to_dict()['paulis']:
            obs.append(i['label'])
            coeffs.append(i['coeff']['real'])

        final_obs = []
        for idx, observable in enumerate(obs):
            for sidx, s in enumerate(observable):
                if(sidx == 0): T = Tensor()
                if (s == 'I'):
                    T = Tensor(T, qml.Identity(sidx))
                elif (s == 'Z'):
                    T = Tensor(T, qml.PauliZ(sidx))
            final_obs.append(T)

        H = qml.Hamiltonian(coeffs, final_obs)

        cost_fn = qml.VQECost(circuit, H, dev)

        opt = qml.GradientDescentOptimizer(stepsize=0.4)
        # Initial parameters
        np.random.seed(0)
        params = np.random.normal(0, np.pi, (qubitOp.num_qubits, 3))

        max_iterations = 80
        conv_tol = 1e-06

        prev_energy = cost_fn(params)
        for n in range(max_iterations):
            params = opt.step(cost_fn, params)
            energy = cost_fn(params)
            conv = np.abs(energy - prev_energy)

            if n % 20 == 0:
                print('Iteration = {:},  Cost = {:.8f},  Convergente = {'
                      ':.8f} Ha'.format(n, energy, conv))
                print("Parameters:")
                print(params)

            if conv <= conv_tol:
                break

            prev_energy = energy

        print("===================")
        print('Final convergence parameter = {:.8f} Ha'.format(conv))
        print('Cost: ',energy)
        print('Final circuit parameters = \n', params)

        result = final_circ(params, qubitOp.num_qubits)

        print("Different states: ", len(result))
        print(min(result))
        idx = np.where(result == min(result))
        idx = '{0:09b}'.format(idx[0][0])
        print(idx)
        print("Cost: ", cost_fn(params))

        binary_result = list(map(int, idx))
        x = binary_state_to_points_order(list(binary_result))
        print(x)

        if(tsp.tsp_feasible(x)):
            z = tsp.get_tsp_solution(x)
            print('solution:', z)
            return z
        else:
            print('no solution:', x)
            return []

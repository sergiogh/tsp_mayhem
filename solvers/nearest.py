import numpy as np

class Nearest:

    def calculate(self, G, cost_matrix, starting_node):

        n = len(list(G))
        cost_matrix = self.check_matrix(cost_matrix)

        solution = [starting_node]

        while len(solution) != n:
            dist = np.inf
            for indx in range(n):
                if cost_matrix[solution[-1]][indx] < dist and indx not in solution:
                    nearest = indx
                    dist = cost_matrix[solution[-1]][indx]
            solution.append(nearest)

        return solution

    def check_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 0:
                    matrix[i][j] = np.inf
        return matrix

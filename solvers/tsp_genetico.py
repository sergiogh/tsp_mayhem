import numpy as np
from numpy.random import permutation

class TSP_genetico:

    def calculate(self, G, cost_matrix, starting_node):

        n = len(list(G))

        cost_matrix = self.check_matrix(cost_matrix)

        prob_mutation = 0.2
        epochs = 10
        samples = 100
        n_top = samples // 2

        #print(cost_matrix)
        for _ in range(epochs):

            population = self.generate_population(n, samples)


            select_top = self.select_population(population, n_top, cost_matrix)

            new_population = self.cross_population(select_top, samples)
            new_population = self.mutation(new_population, prob_mutation)

        cost_population = [self.cost_travel(person, cost_matrix) for person in new_population]

        route = new_population[np.argmin(cost_population)]

        # Put the start node at the beginning
        if route[0] != starting_node:
            # rotate to put the start in front
            idx = route.index(starting_node)
            route = route[idx:] + route[:idx]

        return route

    def cost_travel(self, travel, cost_matrix):

        n = len(travel)
        cost = 0
        previous = travel[0]
        for i in range(1,n):
            cost += cost_matrix[previous][travel[i]]
            previous = travel[i]

        cost += cost_matrix[travel[n - 1]][travel[0]]
        return cost

    def generate_population(self, n, samples):
        return [list(permutation(list(range(n)))) for _ in range(samples)]

    def select_population(self, population, n_top, cost_matrix):

        cost_population = [self.cost_travel(person, cost_matrix) for person in population]
        select_population = []
        while len(select_population) != n_top:
            select_population.append(population[np.argmin(cost_population)])
            cost_population[np.argmin(cost_population)] = np.inf

        return select_population

    def cross_population(self, parents, samples):
        new_population = []
        for _ in range(samples):
            index = list(np.random.choice(list(range(len(parents))), size=2, replace=False))
            two_parents = [parents[index[0]], parents[index[1]]]
            new_population.append(self.get_child(two_parents))
        return new_population

    def get_child(self, parents):
        n = len(parents[0])
        child = parents[0][:n // 2]
        for i in range(n):
            if not parents[1][i] in child:
                child.append(parents[1][i])
        return child

    def check_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 0:
                    matrix[i][j] = np.inf
        return matrix

    def mutation(self, population, prob):
        for person in population:
            if np.random.rand() < prob:
                person[:len(person) // 2] = permutation(person[:len(person) // 2])
        return population

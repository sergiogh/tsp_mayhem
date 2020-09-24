import random
import math


def acceptance_criteria(distance, new_distance, temp):
    if new_distance < distance:
        return 1.0
    return math.exp((distance - new_distance) / temp)


def get_distance(current_list, cost_matrix):
    distance = 0
    pre_j = 0
    for index in current_list:
        distance = distance + cost_matrix[index, pre_j]
        pre_j = index
    return distance


class Annealing:
    def calculate(self, G, cost_matrix, starting_node):

        n = len(list(G))
        temp = 100
        cooling_rate = 0.003

        current = [[i] for i in range(0, n)]
        random.shuffle(current)

        best = current

        while temp > 1:
            # random indexes must be different
            (random_index_1, random_index_2) = random.sample(range(1, n), 2)
            swapped = current.copy()
            swapped[random_index_1], swapped[random_index_2] = swapped[random_index_2], swapped[random_index_1]
            distance = get_distance(current, cost_matrix)
            new_distance = get_distance(swapped, cost_matrix)
            # annealing acceptance criteria
            if acceptance_criteria(distance, new_distance, temp) > random.random():
                current = swapped
                if get_distance(current, cost_matrix) < get_distance(best, cost_matrix):
                    best = current
            # decrease temp
            temp -= cooling_rate

        route = []
        for i in best:
            route.append(i[0])

        # Put the start node at the beginning
        if route[0] != starting_node:
            # rotate to put the start in front
            idx = route.index(starting_node)
            route = route[idx:] + route[:idx]

        return route

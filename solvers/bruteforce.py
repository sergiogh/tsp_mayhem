from itertools import permutations

class Bruteforce:

    def calculate(self, G, cost_matrix, starting_node):

        n = len(list(G))

        a = list(permutations(range(1,n)))
        last_best_distance = 1e10
        for i in a:
            distance = 0
            pre_j = 0
            for j in i:
                distance = distance + cost_matrix[j,pre_j]
                pre_j = j
            distance = distance + cost_matrix[pre_j,0]
            order = (0,) + i
            if distance < last_best_distance:
                best_order = order
                last_best_distance = distance
                print('order = ' + str(order) + ' Distance = ' + str(distance))
        return list(best_order)

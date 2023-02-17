import random
import numpy


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj_list = {v: [] for v in vertices}
        self.weights = {v: 1 for v in vertices}

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def neighbors(self, v):
        return self.adj_list[v]

    def weight(self, v):
        return self.weights[v]

    def set_weight(self, v, w):
        self.weights[v] = w

    def total_weight(self):
        return sum(self.weights[v] for v in self.vertices)

    def get_partition_cost(self, partition1, partition2):
        return sum(self.weight(u) for u in partition1) * (len(partition2) - len(partition1))

    def __len__(self):
        return len(self.vertices)


def fm_algorithm(graph, max_iterations=100):
    """
    Implementation of the Fiduccia-Mattheyses algorithm
    :param graph: Graph object
    :param max_iterations: number of iterations to run the algorithm. Default is 100
    :return:
    """
    partition1 = set(random.sample(graph.vertices, len(graph.vertices) // 2))
    partition2 = set(graph.vertices) - partition1

    # compute initial cut size

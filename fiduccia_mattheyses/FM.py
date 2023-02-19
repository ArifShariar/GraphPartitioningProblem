import random


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


def cut_size_between_partitions(graph, partition1, partition2):
    """
    Computes the cut size between two partitions
    :param graph: Graph object
    :param partition1: partition of vertices
    :param partition2: partition of vertices
    :return: cut size between the two partitions
    """
    cut_size = 0
    for v in partition1:
        for u in graph.neighbors(v):
            if u in partition2:
                cut_size += graph.weight(u)
    return cut_size


def compute_gain(graph, partition1, partition2, v):
    """
    Computes the gain of moving a vertex to the other partition
    :param graph: Graph object
    :param partition1: partition of vertices
    :param partition2: partition of vertices
    :param v: vertex to move
    :return: gain of moving the vertex to the other partition
    """
    return 2 * (cut_size_between_partitions(graph, partition1 - {v}, partition2 | {v}) -
                cut_size_between_partitions(graph, partition1, partition2))


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
    cut_size = cut_size_between_partitions(graph, partition1, partition2)

    # run the algorithm for max_iterations
    for i in range(max_iterations):
        # determine the best partition to move
        if len(partition1) < len(partition2):
            from_partition = partition1
            to_partition = partition2
        else:
            from_partition = partition2
            to_partition = partition1

        # compute the gains for all vertices in the best partition
        gains = {v: compute_gain(graph, from_partition, to_partition, v) for v in from_partition}

        # sort the vertices by gain for all vertices in the best partition
        sorted_vertices = sorted(gains, key=gains.get, reverse=True)
        number_of_vertices_to_move = len(sorted_vertices) // 2
        vertices_to_move = set(sorted_vertices[:number_of_vertices_to_move])
        from_partition.difference_update(vertices_to_move)
        to_partition.update(vertices_to_move)

        # compute the new cut size
        new_cut_size = cut_size_between_partitions(graph, partition1, partition2)

        # if the cut size did not improve, stop the algorithm
        if new_cut_size < cut_size:
            cut_size = new_cut_size
        else:
            from_partition.update(vertices_to_move)
            to_partition.difference_update(vertices_to_move)
            break

    print("Final cut size: " + str(cut_size))
    return partition1, partition2, cut_size


def load_data(file_path: str):
    """
    Loads data from a file
    :param file_path: path to the file
    :return: Graph object
    """
    vertex_list = []
    edges = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in list(lines):
            vertices = line.split()
            u = int(vertices[0])
            v = int(vertices[1])
            if u not in vertex_list:
                vertex_list.append(u)
            if v not in vertex_list:
                vertex_list.append(v)
            edges.append((u, v))

    _graph = Graph(vertex_list)
    for edge in edges:
        _graph.add_edge(edge[0], edge[1])
    return _graph


if __name__ == "__main__":
    graph = load_data("../data/data.txt")
    print(graph.__len__())
    print(graph.vertices)
    print(graph.adj_list)
    _partition1, _partition2_, _cut_size = fm_algorithm(graph)
    print("Final partition cost: " + str(_cut_size))
    print("Partition 1: " + str(_partition1))
    print("Partition 2: " + str(_partition2_))

import sys
sys.path.append('..')

from kernighan_lin.kernighan_lin import * 



graph = load_data("../data/data.txt")
print("Loaded graph with " + str(len(graph.vertices)) + " vertices and " + str(len(graph.edges)) + " edges.")

kl = KernighanLin(graph)
kl.partition()
print("Final partition cost: " + str(graph.get_partition_cost()))
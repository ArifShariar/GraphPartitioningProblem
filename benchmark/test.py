import sys
import time

sys.path.append('..')

from kernighan_lin.kernighan_lin import *

graph = load_data("../data/data16.txt")
print("Loaded graph with " + str(len(graph.vertices)) + " vertices and " + str(len(graph.edges)) + " edges.")

kl = KernighanLin(graph)
start = time.time()
kl.partition()
print("Time: " + str(time.time() - start))
print("Final partition cost: " + str(graph.get_partition_cost()))

from functions import *

graph = {
    'A': ['B', 'C', 'D', 'E'],
    'B': ['A', 'F', 'G'],
    'C': ['A', 'F', 'I'],
    'D': ['A', 'G', 'H'],
    'E': ['A', 'H', 'I'],
    'F': ['B', 'C'],
    'G': ['B', 'D'],
    'H': ['D', 'E'],
    'I': ['C', 'E']
}



print(initState(graph, 5))
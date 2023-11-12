from random import randint
from functions import *
from copy import deepcopy

car1 = (1, 'C')
car2 = (2, 'D')
car3 = (3, 'A')

cars = [car1, car2, car3]

graph = {
    'A': [car2],
    'B': [],
    'C': [],
    'D': [car3],
    'E': [],
    'F': [car1],
}

edges = {
    'AB': randint(1, 10),
    'AD': randint(1, 10),
    'BC': randint(1, 10),
    'BE': randint(1, 10),
    'CF': randint(1, 10),
    'DE': randint(1, 10),
    'EF': randint(1, 10),
}

addReverseEdges(edges)

q_table = {}

sums = q_learning(graph, edges, cars, q_table, 10)
print(sums)
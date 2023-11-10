from itertools import permutations, combinations_with_replacement
from random import randint

def getEdges(graph, node): #get all edges incidental to a given node
    edges = []
    main = graph[node]
    for m in main:
        edges.append(node + m)
    return edges

def genDist(length, sum_): #generate all summations of given length that add up to given sum
    seq = list(range(0, sum_ + 1))
    combos = set(combinations_with_replacement(seq, length))
    good_combos = []
    for c in combos:
        if sum(c) == sum_:
            good_combos.append(c)

    perms = []
    for c in good_combos:
        gen = list(permutations(c))
        for g in gen:
            perms.append(g)

    return list(set(perms))

def genEdgeDist(graph, state):
    nodes = list(graph.keys())
    edges = []
    for n in nodes:
        pass

def initState(graph, sum_=1):
    nodes = list(graph.keys())
    dist = genDist(len(nodes), sum_)
    i = randint(0, len(dist)-1)
    return dist[i]

def newState(graph, old_state, edge_dist):
    nodes = list(graph.keys())
    for e in edge_dist:
        pass
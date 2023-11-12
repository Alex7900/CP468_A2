from itertools import product
from random import random, randint
from copy import deepcopy

def addReverseEdges(edges):
    keys = list(edges.keys())
    for k in keys:
        edges.update({k[::-1]: edges[k]})

    return

def getPopNodes(graph):
    nodes = list(graph.keys())
    pop_nodes = []
    for n in nodes:
        if len(graph[n]) > 0:
            pop_nodes.append(n)
    return pop_nodes

def getPopEdges(pop_nodes, edges):
    edge_names = list(edges.keys())
    pop_edges = []
    for e in edge_names:
        if e[0] in pop_nodes:
            pop_edges.append(e)
    return pop_edges

def getCarIDs(cars):
    car_ids = []
    for c in cars:
        car_ids.append(c[0])
    return car_ids

def pruneActions(actions, graph):
    pruned_actions = []
    pop_nodes = getPopNodes(graph)
    for a in actions:
        node = a[0][0]
        car_id = a[1]
        cars = graph[node]
        for c in cars:
            if car_id == c[0]:
                pruned_actions.append(a)

    return pruned_actions

def genActions(graph, edges, cars):
    pop_nodes = getPopNodes(graph)
    pop_edges = getPopEdges(pop_nodes, edges)
    car_ids = getCarIDs(cars)

    actions = list(product(pop_edges, car_ids))
    pruned_actions = pruneActions(actions, graph)
    return pruned_actions

def findCar(graph, node, car_id):
    car = None
    cars = graph[node]
    for c in cars:
        if c[0] == car_id:
            car = c
            break
    return car

def updateGraph(action, graph):
    curr_node = action[0][0]
    next_node = action[0][1]
    car_id = action[1]
    car = findCar(graph, curr_node, car_id)
    graph[curr_node].remove(car)
    graph[next_node].append(car)
    return

def chooseAction(actions, q_table, iteration):
    epsilon = iteration/10 + 0.01
    value = random()
    action = None
    if len(q_table) > 0 and value <= epsilon:
        s, a = max(q_table, key=q_table.get)
        while a not in actions:
            s, a = max(q_table, key=q_table.get)
        action = a
    else:
        index = randint(0, len(actions)-1)
        action = actions[index]
    return action

def calculateGraphCongestion(graph):
    pop_nodes = getPopNodes(graph)
    ss = 0
    for n in pop_nodes:
        ss += len(graph[n]) **2
    return ss

def numCarsDone(graph):
    num = 0
    nodes = getPopNodes(graph)
    for n in nodes:
        cars = graph[n]
        remove = []
        for c in cars:
            if c[1] == n:
                num += 1
                remove.append(c)
        for r in remove:
            cars.remove(r)

    return num    

def calculateReward(graph1, graph2, action, edges):
    #new reward function: SSP1 - SSP2 - edge_weight
    congestion1 = calculateGraphCongestion(graph1)
    congestion2 = calculateGraphCongestion(graph2)
    edge = action[0]
    edge_weight = edges[edge]
    numCars = numCarsDone(graph2)
    reward = congestion1 - congestion2 - edge_weight + numCars
    return reward

def getMaxFutureReward(graph, actions, q_table):
    next_states = [(str(graph), i) for i in actions]
    max_reward = -1000
    for s in next_states:
        try:
            reward = q_table[s]
            if reward > max_reward:
                max_reward = reward
        except:
            pass
    
    if max_reward == -1000:
        max_reward = 0
    
    return max_reward

def updateQTable(q_table, graph1, action, actions, reward):
    s = str(graph1)
    a = action
    alpha = 0.1
    gamma = 0.9
    max_future_reward = getMaxFutureReward(graph1, actions, q_table)
    index = (s, a)
    
    try:
        q_table[index] = q_table[index] + alpha*((reward + gamma*max_future_reward) - q_table[index])
    except:
        q_table[index] = alpha*((reward + gamma*max_future_reward))

    return

def terminalState(graph):
    terminal = True
    pop_nodes = getPopNodes(graph)
    if len(pop_nodes) == 0:
        terminal = False
    return terminal
    
def q_learning(graph, edges, cars, q_table, iterations):
    sums_rewards = []
    for i in range(iterations):
        done = True
        sum = 0
        print("iteration:", i)
        while done:
            actions = genActions(graph, edges, cars)
            action = chooseAction(actions, q_table, i)
            graph1 = deepcopy(graph)
            updateGraph(action, graph)
            graph2 = deepcopy(graph)
            reward = calculateReward(graph1, graph2, action, edges)
            updateQTable(q_table, graph1, action, actions, reward)
            sum += reward
            done = terminalState(graph)

            print(graph)
            print(len(q_table))
            print()
            
        sums_rewards.append(sum)

    return sums_rewards
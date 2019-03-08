import numpy as np
import random

st = list(map(int, input().split()))
N = len(st)
tmp = [0] * N
tmp[0] = st
for i in range(1, len(st)):
    tmp[i] = list(map(int, input().split()))

a = np.array(tmp)


pheromone = np.ones((N, N), dtype=float)

time = 0
alpha, beta, P, Q = 1, 1, 0.01, 1
numAnts = 10
ants = np.ones((numAnts, N))


def InitAnts():
    for k in range(0, numAnts):
        start = np.random.randint(0, N)
        ants[k] = RandomWay(start, N)
    return ants


def RandomWay(start, N):
    way = np.arange(0, N, 1)
    for i in range(0, N):
        r = np.random.randint(i, N)
        tmp = way[r]
        way[r] = way[i]
        way[i] = tmp
    index = IndexOfElement(way, start)
    tmp = way[0]
    way[0] = way[index]
    way[index] = tmp
    return way


def IndexOfElement(way, start):
    for i in range(0, len(way)):
        if way[i] == start:
            return i


def Length(way):
    res = 0
    for i in range(0, len(way)-1):
        res += a[int(way[i])][int(way[i+1])]
    res += a[int(way[-1])][int(way[0])]
    return res


def BestWay():
    bestLength = Length(ants[0])
    bestLengthIndex = 0
    for k in range(0, len(ants)):
        length = Length(ants[k])
        if length < bestLength:
            bestLength = length
            bestLengthIndex = k
    bestWay = ants[bestLengthIndex]
    return bestWay

def InitPheromones():
    for i in range(0, N):
        for j in range(0, N):
            pheromone[i][j] = 0.01


def UpdateAnts():
    for k in range(0, numAnts):
        start = np.random.randint(0, N)
        newWay = CreateNewWay(k, start)
        ants[k] = newWay


def CreateNewWay(k, start):
    way = [0] * N
    visited = [0] * N
    way[0] = start
    visited[start] = 1
    for i in range(0, N-1):
        nextVertex = NextVertex(k, way[i], visited)
        way[i+1] = nextVertex
        visited[nextVertex] = 1
    return way


def NextVertex(k, fromVertex, visited):
    prob = Probability(k, fromVertex, visited)
    c = [0] * (len(prob)+1)
    for i in range(0, len(prob)):
        c[i+1] = c[i] + prob[i]
    x = random.uniform(0, 1)
    for i in range(0, len(c)-1):
        if x >= c[i] and x < c[i+1]:
            return i


def Probability(k, fromVertex, visited):
    p = [0] * N
    prob = [0] * N
    sum = 0.0
    for i in range(0, len(p)):
        if i == fromVertex:
            p[i] = 0
        elif visited[i] == 1:
            p[i] = 0
        else:
            p[i] = (pheromone[fromVertex][i] ** alpha) * (1/a[fromVertex][i] ** beta)
            if p[i] < 0.0001:
                p[i] = 0.0001
            elif p[i] > 100000:
                p[i] = 100000
        sum += p[i]
    for i in range(0, len(prob)):
        prob[i] = p[i] / sum
    return prob


def UpdatePheromone():
    for k in range(0, numAnts):
        PlusDeltaTay(ants[k])
    for i in range(0, N):
        for j in range(0, N):
            pheromone[i][j] *= (1-P)



def PlusDeltaTay(way):
    length = Length(way)
    delTay = Q / length
    for i in range(0, N-1):
        pheromone[int(way[i])][int(way[i+1])] += delTay
    pheromone[int(way[-1])][int(way[0])] += delTay


InitAnts()

bestWay = BestWay()
bestLength = Length(bestWay)

InitPheromones()

while time < 100:
    UpdateAnts()
    UpdatePheromone()

    currentBestWay = BestWay()
    currentBestLength = Length(currentBestWay)
    if currentBestLength < bestLength:
        bestLength = currentBestLength
        bestWay = currentBestWay
        #print(bestLength)
    time += 1

print(bestLength)
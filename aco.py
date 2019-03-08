import numpy as np
import random

# считывание матрицы смежности
st = list(map(int, input().split()))
N = len(st)
tmp = [0] * N
tmp[0] = st
for i in range(1, len(st)):
    tmp[i] = list(map(int, input().split()))

a = np.array(tmp)

# инициализации начальных параметров
pheromone = np.ones((N, N), dtype=float)
time = 0
alpha, beta, P, Q = 1, 1, 0.01, 1
numAnts = 10
ants = np.ones((numAnts, N))


# инициализация муравьев
def init_ants():
    for k in range(0, numAnts):
        start = np.random.randint(0, N)
        ants[k] = random_way(start, N)
    return ants


# инициализация феромонов
def init_pheromones():
    for i in range(0, N):
        for j in range(0, N):
            pheromone[i][j] = 0.01


# путь муравья выбирается случайнвм образом
def random_way(start, N):
    way = np.arange(0, N, 1)
    for i in range(0, N):
        r = np.random.randint(i, N)
        tmp = way[r]
        way[r] = way[i]
        way[i] = tmp
    # начальная вершина помещается на певрое место
    index = index_of_element(way, start)
    tmp = way[0]
    way[0] = way[index]
    way[index] = tmp
    return way


# получение индекса нцжного элемента
def index_of_element(way, start):
    for i in range(0, len(way)):
        if way[i] == start:
            return i


# расчет длины пути
def culc_length(way):
    res = 0
    for i in range(0, len(way)-1):
        res += a[int(way[i])][int(way[i+1])]
    res += a[int(way[-1])][int(way[0])]
    return res


# расчет лучшего пути
def culc_best_way():
    best_len = culc_length(ants[0])
    best_len_index = 0
    for k in range(0, len(ants)):
        length = culc_length(ants[k])
        if length < best_len:
            best_len = length
            best_len_index = k
    best_way = ants[best_len_index]
    return best_way


# обновление путей муравьев
def update_ants():
    for k in range(0, numAnts):
        start = np.random.randint(0, N)
        new_way = create_new_way(k, start)
        ants[k] = new_way


def create_new_way(k, start):
    way = [0] * N
    visited = [0] * N
    way[0] = start
    visited[start] = 1  # посещенные вершины муравьем
    for i in range(0, N-1):
        next_vertex = culc_next_vertex(k, way[i], visited)
        way[i+1] = next_vertex
        visited[next_vertex] = 1
    return way


def culc_next_vertex(k, from_vertex, visited):
    prob = probability(k, from_vertex, visited)
    c = [0] * (len(prob)+1)
    for i in range(0, len(prob)):  # метод рулетки
        c[i+1] = c[i] + prob[i]
    x = random.uniform(0, 1)
    for i in range(0, len(c)-1):
        if x >= c[i] and x < c[i+1]:
            return i


# вычисление вероятностей
def probability(k, from_vertex, visited):
    p = [0] * N
    prob = [0] * N
    sum = 0.0
    for i in range(0, len(p)):
        if i == from_vertex:
            p[i] = 0
        elif visited[i] == 1:
            p[i] = 0
        else:
            p[i] = (pheromone[from_vertex][i] ** alpha) * (1/a[from_vertex][i] ** beta)
            if p[i] < 0.0001:
                p[i] = 0.0001
            elif p[i] > 100000:
                p[i] = 100000
        sum += p[i]
    for i in range(0, len(prob)):
        prob[i] = p[i] / sum
    return prob


# обновление феромонов
def update_pheromone():
    for k in range(0, numAnts):
        plus_delta_tay(ants[k])  # усиление
    for i in range(0, N):
        for j in range(0, N):
            pheromone[i][j] *= (1-P)  # испарение


def plus_delta_tay(way):
    length = culc_length(way)
    del_tay = Q / length
    for i in range(0, N-1):
        pheromone[int(way[i])][int(way[i+1])] += del_tay
    pheromone[int(way[-1])][int(way[0])] += del_tay


init_ants()

best_way = culc_best_way()
best_length = culc_length(best_way)

init_pheromones()

while time < 100:
    update_ants()
    update_pheromone()

    current_best_way = culc_best_way()
    current_best_length = culc_length(current_best_way)
    if current_best_length < best_length:
        best_length = current_best_length
        best_way = current_best_way
    time += 1

print(best_length)

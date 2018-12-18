import copy
import random
import sys
from math import floor


PRECISE = 5
Q = 20
COLOR_CODES = list(range(236, 255))

CONFIG = {
    'a': float,
    'b': float,
    'p': float,
    'agents': int,

}


def sanitize_config(config):
    for key, sanitizer in CONFIG.items():
        if key in config:
            config[key] = sanitizer(config[key])

def _matrix_max(matrix):
    return max(max(row) for row in matrix)


def _print_matrix(matrix):
    matrix_max = _matrix_max(matrix)
    colores = len(COLOR_CODES)
    def __formatter(element):
        return '\033[38;5;%sm%8.5f' % (COLOR_CODES[floor((colores - 1) * element / matrix_max)], element, )
    print("\n".join(" ".join(map(__formatter, row)) for row in matrix))
    print("\033[39m")


def ant(graph, config=None):
    """Calculate.

    :params:
        graph - travel prices.
        a - ferment weight.
        b - heuristic coefficient.
        p - pheromones expiration.
    """
    size = len(graph)
    if config:
        sanitize_config(config)
    else:
        config = {}
    a = config.get('a', 0.85)
    b = config.get('b', round(1 - a, PRECISE))
    p = config.get('p', 0.5)
    agents = config.get('agents', 5)
    print("agents: %s" % (agents, ))

    def n(r, u):
        return round(1 / graph[r][u], PRECISE)

    smell = [[Q if col_ind != row_ind else 0 for col_ind in range(size)] for row_ind in range(size)]

    def expiration_rate(x):
        return round(x * (1 - p), PRECISE)

    def expire():
        nonlocal smell
        smell = [list(map(expiration_rate, row)) for row in smell]

    def update(path_pairs, costs):
        nonlocal smell
        pheromone_unit = Q / sum(costs)
        print("path:", path_pairs)
        print('was')
        _print_matrix(smell)
        for (f, t), cost in zip(path_pairs, costs):
            smell[f][t] = round(smell[f][t] * (1 - p) + Q / cost, PRECISE)
        print("become")
        _print_matrix(smell)

    def agent():
        current = random.randrange(0, size-1)
        banned = set((current, ))
        path = [current, ]
        # print('current: %s' % (current, ))

        def get_p(r):
            """Return changes.

            :params:
                r - from
                u - to

            :return:
                list of probabilities.
            """
            raw_chances = [round(smell[r][u] ** a * n(r, u) ** b, PRECISE) if u not in banned and r != u else 0 for u in range(size)]
            # print('raw_chances: ', raw_chances)
            summed = sum(raw_chances)
            # print('sum: ', summed)
            return [round(raw_chance / summed, PRECISE) for raw_chance in raw_chances]
            # print('chances: ', chances)

        while len(banned) != size:
            print("current: ", current)
            # get chances.
            chances = get_p(current)
            print("chances: ", chances)

            # get random node.
            index, agg_chance = 0, chances[0]
            target_chance = round(random.random(), PRECISE)
            print("target chance: ", target_chance)
            while agg_chance < target_chance:
                index += 1
                agg_chance += chances[index]
            # print(chances)
            # print('target chance: ', target_chance, ' index: ', index)
            current = index
            path.append(current)
            banned.add(current)
        # print('path: ', path)
        return path

    paths = []
    costs = []
    smells = []
    for agent_id in range(agents):
        # spawn agent
        path = agent()
        path_pairs = list(zip(path[-1:] + path[:-1], path))
        path_costs = [graph[f][t] for f, t in path_pairs]
        path_smells = [smell[f][t] for f, t in path_pairs]
        print("path: \n%s \ncosts: \n%s \nsmell: \n%s" % (path, path_costs, path_smells))
        cost = sum(path_costs)
        paths.append(path)
        costs.append(path_costs)
        smells.append(copy.copy(smell))
        # update pheromone.
        update(path_pairs, path_costs)

    for path, cost in zip(paths, costs):
        print("path: [ %s ] cost: %s" % (' > '.join(map(str, path)), sum(cost)))

    return paths[::-1], [sum(cost) for cost in costs][::-1], smell[::-1]


if __name__ == '__main__':
    graph = [
        [0, 2, 1, 3, 6],
        [1, 0, 1, 3, 5],
        [1, 5, 0, 2, 1],
        [4, 2, 6, 0, 2],
        [1, 2, 1, 4, 0],
    ]
    ant(graph)
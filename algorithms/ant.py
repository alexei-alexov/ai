import random


def ant(graph, a=None, b=None, p=None):
    """Calculate.

    :params:
        graph - travel prices.
        a - ferment weight.
        b - heuristic coefficient.
        p - pheromones expiration.
    """
    size = len(graph)
    if not a:
        a = 0.3
    if not b:
        b = 1 - a
    if not p:
        p = 0.2

    def n(r, u):
        return 1 / graph[(r,u)]

    smell = [[0]*size for _ in range(size)]

    def expiration_rate(x):
        return x * (1 - p)


    def expire():
        smell = [list(map(expiration_rate, row)) for row in smell]

    def agent():
        current = random.randrange(0, size-1)
        banned = set(current)

        def get_p(r):
            """Return changes.

            :params:
                r - from
                u - to

            :return:
                list of probabilities.
            """
            raw_chances = [0 if i in banned else smell[r][i] for i in range(size)]
            summed = sum(raw_chances)
            chances = [raw_chance / summed for raw_chance in raw_chances]
            smell[r, u] ** a * n(r, u) ** b

        while True:
            # exhaust pheromone.
            expire()

            # get chances.

            # get random node.

            # update pheromone.


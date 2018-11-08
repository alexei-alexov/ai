"""Short distance search."""
import random
from itertools import cycle
from functools import reduce


config_values = {
    'population': int,
    'penalty': int,
    'mutation': int,
    'rounds': int,
}


def evaluate_config(raw_data):
    for key, evaluator in config_values.items():
        if key in raw_data:
            raw_data[key] = evaluator(raw_data[key])


def search(graph, config=None):
    """Resolve TSP using genetic algorithm.

    Config:
    - population: number of units in population. (size of graph by default)
    - penalty: minimum amount to be chosen. (5 by default)
    - mutation: amount of units to be mutated after selection. (2 by default)
    - rounds: amount of rounds (select, mutate). (10 by default)
    """
    if not graph:
        return None
    config = config or {}
    population_size = config.get('population', len(graph))
    def get_unit():
        pop = list(range(len(graph)))
        random.shuffle(pop)
        return pop

    def get_costs(population):
        return [sum(graph[i][j] for i, j in zip(unit, cycle(unit[1:]+unit[:1])))
                    for unit in population]

    def print_pop(population, costs):
        print("Population and costs:\n%s" % (
            "\n".join("%s -> %s" % (pop, cost, ) for pop, cost in zip(population, costs)), ))

    def selection(population, costs):
        new_population = []
        worst_cost = max(costs) + config.get('penalty', 5)
        revers_costs = [worst_cost - cost for cost in costs]
        # print("R Costs: %s" % (revers_costs, ))
        chances = reduce(lambda acc, elem: acc + [acc[-1]+elem, ], revers_costs, [0, ])[1:]
        # print("chances: %s" % (chances, ))
        max_chance = max(chances)
        for _ in range(len(population)):
            chosen = random.randint(1, max_chance)
            # print("Chosen: %s" % (chosen, ))
            s, index = revers_costs[0], 0
            while chosen > s:
                index += 1; s += revers_costs[index]
                # print("Index: %s Sum: %s" % (index, s, ))
            new_population.append(population[index][:])
        return new_population

    def mutation(population):
        random.shuffle(population)
        for index in range(min(len(population), config.get('mutation', 2))):
            random.shuffle(population[index])
    # init population define
    population = [get_unit() for _ in range(population_size)]
    costs = get_costs(population)
    print_pop(population, costs)

    for _ in range(config.get('rounds', 10)):
        # choose new population
        population = selection(population, costs)
        costs = get_costs(population)
        print_pop(population, costs)
        # mutate it
        mutation(population)
        print("Mutated.")
        costs = get_costs(population)
        print_pop(population, costs)

    return sorted(zip(costs, population))


if __name__ == "__main__":
    test_graph = [
        [ 0, 20, 42, 35],
        [20,  0, 30, 34],
        [42, 30,  0, 12],
        [35, 34, 12,  0],
    ]
    test_graph = [
        [ 0, 24, 13, 13, 22],
        [24,  0, 22, 13, 13],
        [13, 22,  0, 19, 14],
        [13, 13, 19,  0, 19],
        [22, 13, 14, 19,  0],
    ]
    test_graph = [
        [ 0, 28, 33, 30, 25, 42],
        [28,  0, 18, 26, 33, 30],
        [33, 18,  0, 12, 23, 12],
        [30, 26, 12,  0, 12, 13],
        [25, 33, 23, 12,  0, 25],
        [42, 30, 12, 13, 25,  0],
    ]
    result = search(test_graph, {'population': 8})
    print(result)
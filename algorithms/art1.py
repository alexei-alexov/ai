import codecs
import copy
import csv
import random
import sys
from functools import reduce


def vector_and(vector1, vector2):
    return [element1 & element2 for element1, element2 in zip(vector1, vector2)]


def vector_value(vector):
    return sum(vector)


class Cluster(object):

    def __init__(self, pool, vector, ):
        self.data = [copy.copy(vector), ]
        self.vector = copy.copy(vector)
        self.pool = pool

    def similarity_test(self, vector):
        return vector_value(
            vector_and(self.vector, vector)) / (self.pool.beta + vector_value(vector))\
             > vector_value(self.vector) / (self.pool.beta + len(vector))

    def similarity(self, vector):
        return round(vector_value(vector_and(self.vector, vector)) / (self.pool.beta + vector_value(vector)), 5)

    def size_test(self, vector):
        return ()

    def add(self, vector):
        """Return True if has been added into the cluster, False otherwise."""
        result_vector = vector_and(self.vector, vector)
        united_value = vector_value(result_vector) + 0.0001
        cluster_value = vector_value(self.vector) + 0.0001
        similar = united_value / (self.pool.beta + vector_value(vector)) > cluster_value / (self.pool.beta + len(vector))
        attention = united_value / cluster_value >= self.pool.rho
        # print('result_vector: %s\nunited_vector: %s\ncluster_value: %s\nsimilar: %s\nattention: %s\n' % (result_vector, united_value, cluster_value, similar, attention, ))
        if attention:
            self.data.append(vector)
            self.vector = result_vector
            return True
        return False

    def __repr__(self):
        return '%s -> %s' % (repr(self.data), repr(self.vector), )


class ClusterPool(object):

    def __init__(self, beta=2, rho=0.4):
        self.rho = rho
        self.beta = beta
        self.clusters = []

    def add(self, vector):
        """Return True if new cluster has been created, False otherwise."""
        # print("vector: %s" % (vector, ))
        # print("ALL: %s" % (list(map(lambda cluster:  (cluster.similarity(vector), cluster), self.clusters), )))
        best_cluster = reduce(lambda best, cluster_pair: best if best[0] > cluster_pair[0] else cluster_pair,
                              map(lambda cluster:  (cluster.similarity(vector), cluster), self.clusters), (-1, None))
        # print("Best cluster: ", best_cluster)
        if best_cluster[1] and best_cluster[1].add(vector):
            # print("used cluster: %s" % (repr(best_cluster, )))
            return False
        self.clusters.append(Cluster(self, vector))
        # print("created new cluster. recalculating")
        return True

    def __repr__(self):
        return "[Cluster B: %s P: %s]\n%s" % (self.beta, self.rho, '\n'.join(map(repr, self.clusters)), )


def get_cluster_from_csv(csv_file, beta, rho):
    reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
    raw_data = []
    def _parse_line(line):
        try:
            line = [1 if c == '1' else 0 for c in line]
            raw_data.append(line)
            return line
        except: return None

    pool = ClusterPool(beta=beta, rho=rho)
    for line in filter(lambda x: x, map(_parse_line, reader)):
        try:
            pool.add(line)
        except: continue
    return pool, raw_data


if __name__ == '__main__':
    with open('test.csv') as f:
        pool = get_cluster_from_csv(f)
        print(pool)

    sys.exit(0)
    cp = ClusterPool()
    V_SIZE = 6
    for i in range(20):
        cp.add([round(random.random()) for _ in range(V_SIZE)])
    print(cp)
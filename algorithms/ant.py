def ant(graph, a=None, b=None):
    if not a:
        a = 0.3
    if not b:
        b = 1 - a
    
    def n(r, u):
        return 1 / graph[(r,u)]
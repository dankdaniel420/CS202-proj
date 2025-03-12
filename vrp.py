import sys
import itertools

"""
To use this file with example testcases, run: 

python vrp.py < example_testcases/1.in > 1.out

This reads input from 1.in and prints output to 1.out. 
"""

def read_input():
    """Reads input from stdin and returns number of locations, vehicle capacity, distance matrix, and demand vector."""
    n = int(sys.stdin.readline().strip())
    Q = int(sys.stdin.readline().strip())
    
    D = []
    for _ in range(n):
        D.append(list(map(int, sys.stdin.readline().strip().split())))
    
    q = list(map(int, sys.stdin.readline().strip().split()))
    
    return n, Q, D, q

def solve_cvrp(n, Q, D, q):
    """TODO: Solve the Capacitated Vehicle Routing Problem and return a list of routes."""
    depot_distance = D[0]
    routes = []
    curr_route = [0]
    curr_cap = 0
    visited = set([0])

    def get_closest_index(array: list):
        closest = None
        for i, dist in enumerate(array):
            if i in visited:
                continue

            if dist > 0 and closest is None:
                closest = i
                continue
            
            if dist > 0 and dist < array[closest]:
                closest = i

        return closest

    for i in range(n-1):
        target = get_closest_index(D[i])
        if curr_cap + q[target] > Q:
            curr_route.append(0)
            routes.append(curr_route)
            curr_route = [0]
            curr_cap = 0
        curr_route.append(target)
        curr_cap += q[target]
        visited.add(target)

    # capture last trip
    curr_route.append(0)
    routes.append(curr_route)
    return routes

# def check(routes, n, Q, D, q):
#     node_visited = []
#     for route in routes:
#         total_demand = sum([q[i] for i in route if i != 0])
#         if not (total_demand <= Q):
#             return False
#         node_visited += route

#     if len(set(node_visited)) != len(q):
#         return False

#     return True

def main():
    n, Q, D, q = read_input()
    routes = solve_cvrp(n, Q, D, q)

    # if check(routes, n, Q, D, q): 
    #     for route in routes:
    #         print(" ".join(map(str, route)))

    for route in routes:
        print(" ".join(map(str, route)))

if __name__ == "__main__":
    main()

import sys
import itertools

"""
To use this file with example testcases, run: 

python vrp.py < example_testcases/1.in > 1.out

This reads input from 1.in and prints output to 1.out. 
"""
"""
1. Generate a set of routes starting and ending at the depot.
+ return trip 

#2. Ensure each customer is visited exactly once.

Customers == 1 
#3. Ensure the total demand on each route does not exceed the vehicle’s capacity.

while weight <= Vehicle capaccity

#4. Minimize the total travel distance across all routes.

Recursive function to find lowest
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


def get_closest_unvisited_index(distances, visited):
    """Return the index of the nearest node not yet in visited."""
    # distances: list of dists from current node to all nodes
    return min(
        (i for i in range(len(distances)) if i not in visited),
        key=lambda i: distances[i]
    )

def solve_cvrp(n, Q, D, q):

    """
    Greedy nearest‑neighbor CVRP:
    - Start at depot (0), repeatedly go to the closest unvisited customer
    - If capacity would overflow, return to depot and start a new trip
    """
    routes = []
    visited = set([0])
    curr = 0
    curr_capacity = 0
    curr_route = [0]

    while len(visited) < n:
        target = get_closest_unvisited_index(D[curr], visited)
        # if adding target would exceed capacity, close out this route
        if curr_capacity + q[target] > Q:
            curr_route.append(0)       # return to depot
            routes.append(curr_route)
            # start a fresh trip
            curr_route = [0]
            curr_capacity = 0
            curr = 0
            continue

        # visit target
        curr_route.append(target)
        curr_capacity += q[target]
        visited.add(target)
        curr = target

    # close final trip
    curr_route.append(0)
    routes.append(curr_route)
    return routes

def check(routes, n, Q, D, q):
    node_visited = []
    for route in routes:
        total_demand = sum([q[i] for i in route if i != 0])
        if not (total_demand <= Q):
            return False
        node_visited += route

    if len(set(node_visited)) != len(q):
        return False

    return True

def main():
    n, Q, D, q = read_input()
    routes = solve_cvrp(n, Q, D, q)

    if check(routes, n, Q, D, q): 
        for route in routes:
            print(" ".join(map(str, route)))

if __name__ == "__main__":
    main()

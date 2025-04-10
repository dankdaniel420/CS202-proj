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

    # Initialize each customer in its own route: depot → i → depot
    routes = {}
    route_demand = {}
    route_of = {}

    for i in range(1, n):
        routes[i] = [0, i, 0]
        route_demand[i] = q[i]
        route_of[i] = i

    # Compute savings for every pair (i, j), i<j:
    # savings = (cost_depot→i + cost_depot→j − cost_i→j, i, j)
    savings = [
        (D[0][i] + D[0][j] - D[i][j], i, j)
        for i in range(1, n)
        for j in range(i+1, n)
    ]

    # Sort savings in descending order of potential cost reduction
    savings.sort(reverse=True, key=lambda x: x[0])


    # Clarke–Wright Savings: Part 2 (Merge phase)

    for saving, i, j in savings:
        ri, rj = route_of[i], route_of[j]
        # only consider if i and j are in different routes
        if ri != rj:
            # check i is at the end of its route and j at the start of its
            if routes[ri][-2] == i and routes[rj][1] == j:
                # ensure merging won’t exceed capacity
                if route_demand[ri] + route_demand[rj] <= Q:
                    # perform merge: drop the trailing depot of ri and leading depot of rj
                    routes[ri] = routes[ri][:-1] + routes[rj][1:]
                    # update demand
                    route_demand[ri] += route_demand[rj]
                    # reassign all nodes in rj to route ri
                    for node in routes[rj][1:-1]:
                        route_of[node] = ri
                    # remove the old route
                    del routes[rj]
                    del route_demand[rj]


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

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

def calculate_distance(routes, D):
    """
    Given a list of routes (each a list of node indices),
    and distance matrix D, return the sum of all leg distances.
    """
    total = 0
    for route in routes:
        # route is e.g. [0, 3, 5, 0]
        for i in range(len(route)-1):
            total += D[route[i]][route[i+1]]
    return total

def solve_cvrp(n, Q, D, q):   
    # Base case, depot to each location and back
    shortest_route = [[0, x, 0] for x in range(1, n)]
    shortest_dist = sum(D[0]) * 2

    for perm in itertools.permutations(n-1):
        routes = []
        curr, curr_capacity, curr_route = 0, 0, [0]
        for target in perm:
            if curr_capacity + q[target] > Q:
                routes.append(curr_route + [0])
                curr, curr_capacity, curr_route = 0, 0, [0]
            curr_route.append(target)
            curr_capacity += q[target]
            curr = target
        routes.append(curr_route + [0])  # capture last trip

        curr_dist = calculate_distance(routes)
        if curr_dist < shortest_dist:
            shortest_dist, shortest_route = curr_dist, routes


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

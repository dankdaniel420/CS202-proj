import sys

"""
To use this file with example testcases, run: 

python vrp.py < 1.in > 1.out

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

def tsp_next_neighbour(route, D):
    visited = [0]
    unvisited = set(route[1:])

    while unvisited:
        current = visited[-1]
        nearest_neighbour = min(unvisited, key=lambda x: D[current][x])
        visited.append(nearest_neighbour)
        unvisited.remove(nearest_neighbour)

    visited.append(0) # return to depot
    return visited

def solve_cvrp(n, Q, D, q):
    """TODO: Solve the Capacitated Vehicle Routing Problem and return a list of routes."""
    routes = []
    unvisited_customers = set(range(1, n))

    while unvisited_customers:
        current_route = [0]
        remaining_capacity = Q

        sorted_customers = sorted(unvisited_customers, key=lambda x: q[x], reverse=True)

        for customer in sorted_customers:
            if customer in unvisited_customers and q[customer] <= remaining_capacity:
                current_route.append(customer)
                remaining_capacity -= q[customer]
                unvisited_customers.remove(customer)

        optimised_route = tsp_next_neighbour(current_route, D)
        routes.append(optimised_route)

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

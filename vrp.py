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
            if i in visited or dist == 0:
                continue

            if closest is None:
                closest = i
                continue
            
            if dist < array[closest]:
                closest = i

        return closest

    for i in range(n-1):
        target = get_closest_index(D[i])
        if curr_cap + q[target] > Q:
            curr_route.append(0)
            routes.append(curr_route)
            curr_route = [0]
            curr_cap = 0
            target = get_closest_index(D[0])
        curr_route.append(target)
        curr_cap += q[target]
        visited.add(target)

    # capture last trip
    curr_route.append(0)
    routes.append(curr_route)

    def calculate_route_distance(route):
        distance = 0
        current_distance_array = depot_distance
        for x in route:
            distance += current_distance_array[x]
            current_distance_array = D[x]
        
        return distance


    # optimise existing routes
    def two_opt(route):
        n = len(route)
        # No way to optimise 2D / 3D shapes
        if n <= 4:
            return route 
        
        best_route = route
        improved = True
        while improved:
            improved = False
            for i in range(1, n-2):
                for j in range(i+1, n-1):
                    new_route = best_route[:i] + best_route[i:j+1:-1] + best_route[j+1:]
                    if calculate_route_distance(new_route) < calculate_route_distance(best_route):
                        best_route = new_route
                        improved = True

        return best_route
    
    for route in routes:
        two_opt(route)

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

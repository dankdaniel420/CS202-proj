import sys
import time
import heapq 

def read_input():
    n = int(sys.stdin.readline().strip())
    Q = int(sys.stdin.readline().strip())
    
    D = []
    for _ in range(n):
        D.append(list(map(int, sys.stdin.readline().strip().split())))
    
    q = list(map(int, sys.stdin.readline().strip().split()))
    
    return n, Q, D, q

def solve_cvrp(n, Q, D, q):
    depot = 0  # Depot is node 0

    routes = [[i] for i in range(1, n)]
    route_demands = [q[i] for i in range(1, n)]  # Track demands for each route

    savings_heap = []
    k = 1000  # Limit the number of savings to consider
    for i in range(1, n):
        for j in range(i + 1, n):
            s = D[depot][i] + D[depot][j] - D[i][j]
            if len(savings_heap) < k:
                heapq.heappush(savings_heap, (s, i, j))
            else:
                heapq.heappushpop(savings_heap, (s, i, j))  # Keep only the top k savings

    sorted_savings = sorted(savings_heap, reverse=True, key=lambda x: x[0])

    for s, i, j in sorted_savings:
        # Find routes containing i and j
        route_i_idx = None
        route_j_idx = None
        for idx, route in enumerate(routes):
            if i in route:
                route_i_idx = idx
            if j in route:
                route_j_idx = idx

        # Check if routes can be merged
        if route_i_idx != route_j_idx and route_demands[route_i_idx] + route_demands[route_j_idx] <= Q:
            # Merge routes
            new_route = routes[route_i_idx] + routes[route_j_idx]
            new_demand = route_demands[route_i_idx] + route_demands[route_j_idx]

            # Remove old routes and demands
            if route_i_idx < route_j_idx:
                del routes[route_j_idx]
                del routes[route_i_idx]
                del route_demands[route_j_idx]
                del route_demands[route_i_idx]
            else:
                del routes[route_i_idx]
                del routes[route_j_idx]
                del route_demands[route_i_idx]
                del route_demands[route_j_idx]

            # Add new route and demand
            routes.append(new_route)
            route_demands.append(new_demand)

    # Add depot to the beginning and end of each route
    final_routes = []
    for route in routes:
        final_routes.append([depot] + route + [depot])

    return final_routes

def check(routes, n, Q, D, q):
    """Checks if the solution is valid."""
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
    else:
        print("Invalid solution")

if __name__ == "__main__":
    main()
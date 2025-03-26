import sys
import copy

def read_input():
    n = int(sys.stdin.readline().strip())
    Q = int(sys.stdin.readline().strip())
    
    D = []
    for _ in range(n):
        D.append(list(map(int, sys.stdin.readline().strip().split())))
    
    q = list(map(int, sys.stdin.readline().strip().split()))
    
    return n, Q, D, q

def clarke_wright_savings(D, q, Q):
    n = len(q)
    savings = []
    for i in range(1, n):
        for j in range(i+1, n):
            saving = D[0][i] + D[0][j] - D[i][j]
            savings.append((saving, i, j))
    savings.sort(reverse=True, key=lambda x: x[0])
    
    # Each customer starts with its own route
    routes = { i: [0, i, 0] for i in range(1, n) }
    route_demand = { i: q[i] for i in range(1, n) }
    route_of = { i: i for i in range(1, n) }
    
    for saving, i, j in savings:
        r1 = route_of[i]
        r2 = route_of[j]
        if r1 == r2:
            continue
        
        route1 = routes[r1]
        route2 = routes[r2]
        merged = None
        # Merge if i is at the start of route1 and j is at the end of route2
        if route1[1] == i and route2[-2] == j:
            merged = route2[:-1] + route1[1:]
        # Or if i is at the end of route1 and j is at the start of route2
        elif route1[-2] == i and route2[1] == j:
            merged = route1[:-1] + route2[1:]
        
        if merged is None:
            continue
        
        merged_demand = route_demand[r1] + route_demand[r2]
        if merged_demand > Q:
            continue
        
        routes[r1] = merged
        route_demand[r1] = merged_demand
        for customer in merged[1:-1]:
            route_of[customer] = r1
        del routes[r2]
        del route_demand[r2]
    
    return list(routes.values())

def two_opt(route, D):
    improved = True
    best_route = route.copy()
    
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                current_distance = D[route[i-1]][route[i]] + D[route[j]][route[j+1]]
                new_distance = D[route[i-1]][route[j]] + D[route[i]][route[j+1]]
                if new_distance < current_distance:
                    best_route[i:j+1] = list(reversed(route[i:j+1]))
                    route = best_route.copy()
                    improved = True
                    break
            if improved:
                break
    return best_route

def compute_total_distance(routes, D):
    total_distance = 0
    for route in routes:
        for i in range(len(route) - 1):
            total_distance += D[route[i]][route[i+1]]
    return total_distance

def solve_cvrp_inner(D, q, Q, max_iterations=1):
    current_solution = clarke_wright_savings(D, q, Q)
    best_distance = compute_total_distance(current_solution, D)
    best_solution = current_solution
    
    for _ in range(max_iterations):
        new_solution = [two_opt(route, D) for route in current_solution]
        new_distance = compute_total_distance(new_solution, D)
        if new_distance < best_distance:
            best_solution = new_solution
            best_distance = new_distance
            current_solution = new_solution
    
    return best_solution, best_distance

def solve_cvrp(n, Q, D, q):
    best_routes, best_distance = solve_cvrp_inner(D, q, Q, max_iterations=1)
    return best_routes

def main():
    n, Q, D, q = read_input()
    routes = solve_cvrp(n, Q, D, q)
    for route in routes:
        print(" ".join(map(str, route)))

if __name__ == "__main__":
    main()

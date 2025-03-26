import sys
import random
import time
import tracemalloc
from collections import defaultdict

def read_input():
    n = int(sys.stdin.readline().strip())
    Q = int(sys.stdin.readline().strip())
    D = []
    for _ in range(n):
        row = list(map(int, sys.stdin.readline().strip().split()))
        D.append(row)
    q = list(map(int, sys.stdin.readline().strip().split()))
    return n, Q, D, q

def tsp_nearest_insertion(route, D):
    # Optimize a route using a nearest insertion heuristic.
    if len(route) <= 3:
        return route
    optimized = [0, route[1], 0]
    remaining = set(route[2:-1])
    while remaining:
        best_cost = float('inf')
        best_node = None
        best_pos = None
        for node in remaining:
            for pos in range(1, len(optimized)):
                prev = optimized[pos-1]
                curr = optimized[pos]
                insertion_cost = D[prev][node] + D[node][curr] - D[prev][curr]
                if insertion_cost < best_cost:
                    best_cost = insertion_cost
                    best_node = node
                    best_pos = pos
        optimized.insert(best_pos, best_node)
        remaining.remove(best_node)
    return optimized

def savings_algorithm(n, Q, D, q):
    # Initialize each customer as its own route.
    routes = [[0, i, 0] for i in range(1, n)]
    savings = []
    for i in range(1, n):
        for j in range(i+1, n):
            saving = D[0][i] + D[0][j] - D[i][j]
            savings.append((saving, i, j))
    savings.sort(reverse=True)
    node_to_route = {i: i-1 for i in range(1, n)}
    in_routes = set(range(len(routes)))
    demands = {i: q[routes[i][1]] for i in range(len(routes))}
    for saving, i, j in savings:
        route_i = node_to_route.get(i)
        route_j = node_to_route.get(j)
        if route_i not in in_routes or route_j not in in_routes:
            continue
        if route_i == route_j:
            continue
        i_at_end = routes[route_i][-2] == i
        j_at_start = routes[route_j][1] == j
        if i_at_end and j_at_start and demands[route_i] + demands[route_j] <= Q:
            new_route = routes[route_i][:-1] + routes[route_j][1:]
            demands[route_i] += demands[route_j]
            routes[route_i] = new_route
            in_routes.remove(route_j)
            for node in routes[route_j][1:-1]:
                node_to_route[node] = route_i
            demands[route_j] = 0
    final_routes = [routes[i] for i in in_routes]
    final_routes = [tsp_nearest_insertion(route, D) for route in final_routes]
    return final_routes

def calculate_total_distance(routes, D):
    total = 0
    for route in routes:
        for i in range(len(route)-1):
            total += D[route[i]][route[i+1]]
    return total

def local_search(routes, n, Q, D, q, iterations=50):
    # Randomly try swap, relocate, or 2-opt moves on routes.
    best_routes = [route.copy() for route in routes]
    best_distance = calculate_total_distance(best_routes, D)
    current_routes = [route.copy() for route in routes]
    for _ in range(iterations):
        strategy = random.choice(['swap', 'relocate', '2-opt'])
        if strategy == 'swap' and len(current_routes) > 1:
            route1_idx = random.randint(0, len(current_routes)-1)
            route2_idx = random.randint(0, len(current_routes)-1)
            while route2_idx == route1_idx:
                route2_idx = random.randint(0, len(current_routes)-1)
            route1 = current_routes[route1_idx].copy()
            route2 = current_routes[route2_idx].copy()
            if len(route1) <= 3 or len(route2) <= 3:
                continue
            cust1_idx = random.randint(1, len(route1)-2)
            cust2_idx = random.randint(1, len(route2)-2)
            cust1 = route1[cust1_idx]
            cust2 = route2[cust2_idx]
            new_demand1 = sum(q[i] for i in route1 if i != 0 and i != cust1) + q[cust2]
            new_demand2 = sum(q[i] for i in route2 if i != 0 and i != cust2) + q[cust1]
            if new_demand1 <= Q and new_demand2 <= Q:
                route1[cust1_idx] = cust2
                route2[cust2_idx] = cust1
                new_routes = current_routes.copy()
                new_routes[route1_idx] = route1
                new_routes[route2_idx] = route2
                new_distance = calculate_total_distance(new_routes, D)
                if new_distance < best_distance:
                    best_routes = [r.copy() for r in new_routes]
                    best_distance = new_distance
                    current_routes = new_routes
        elif strategy == 'relocate' and len(current_routes) > 1:
            route1_idx = random.randint(0, len(current_routes)-1)
            route2_idx = random.randint(0, len(current_routes)-1)
            while route2_idx == route1_idx:
                route2_idx = random.randint(0, len(current_routes)-1)
            route1 = current_routes[route1_idx].copy()
            route2 = current_routes[route2_idx].copy()
            if len(route1) <= 3:
                continue
            cust_idx = random.randint(1, len(route1)-2)
            cust = route1[cust_idx]
            new_demand2 = sum(q[i] for i in route2 if i != 0) + q[cust]
            if new_demand2 <= Q:
                route1.pop(cust_idx)
                best_pos = 1
                best_insert_cost = float('inf')
                for pos in range(1, len(route2)):
                    prev = route2[pos-1]
                    curr = route2[pos]
                    insert_cost = D[prev][cust] + D[cust][curr] - D[prev][curr]
                    if insert_cost < best_insert_cost:
                        best_insert_cost = insert_cost
                        best_pos = pos
                route2.insert(best_pos, cust)
                new_routes = current_routes.copy()
                new_routes[route1_idx] = route1
                new_routes[route2_idx] = route2
                new_distance = calculate_total_distance(new_routes, D)
                if new_distance < best_distance:
                    best_routes = [r.copy() for r in new_routes]
                    best_distance = new_distance
                    current_routes = new_routes
        elif strategy == '2-opt':
            if not current_routes:
                continue
            route_idx = random.randint(0, len(current_routes)-1)
            route = current_routes[route_idx].copy()
            if len(route) <= 4:
                continue
            i = random.randint(1, len(route)-3)
            j = random.randint(i+1, len(route)-2)
            route[i:j+1] = list(reversed(route[i:j+1]))
            new_routes = current_routes.copy()
            new_routes[route_idx] = route
            new_distance = calculate_total_distance(new_routes, D)
            if new_distance < best_distance:
                best_routes = [r.copy() for r in new_routes]
                best_distance = new_distance
                current_routes = new_routes
    return best_routes

def final_2opt(routes, D, max_iter=50):
    improved_routes = []
    for route in routes:
        improved_route = route.copy()
        improved = True
        iter_count = 0
        while improved and iter_count < max_iter:
            improved = False
            best_dist = sum(D[improved_route[i]][improved_route[i+1]] for i in range(len(improved_route)-1))
            for i in range(1, len(improved_route)-2):
                for j in range(i+1, len(improved_route)-1):
                    new_route = improved_route[:i] + list(reversed(improved_route[i:j+1])) + improved_route[j+1:]
                    new_dist = sum(D[new_route[k]][new_route[k+1]] for k in range(len(new_route)-1))
                    if new_dist < best_dist:
                        improved_route = new_route
                        best_dist = new_dist
                        improved = True
            iter_count += 1
        improved_routes.append(improved_route)
    return improved_routes

def inter_route_relocate(routes, D, q, Q, max_iter=10):
    # Try relocating a customer from one route to another if it reduces distance.
    improved = True
    iter_count = 0
    while improved and iter_count < max_iter:
        improved = False
        for i in range(len(routes)):
            for j in range(len(routes)):
                if i == j:
                    continue
                route_from = routes[i]
                route_to = routes[j]
                for cust_idx in range(1, len(route_from)-1):
                    cust = route_from[cust_idx]
                    new_demand_to = sum(q[x] for x in route_to if x != 0) + q[cust]
                    if new_demand_to > Q:
                        continue
                    best_pos = None
                    best_increase = float('inf')
                    for pos in range(1, len(route_to)):
                        prev = route_to[pos-1]
                        curr = route_to[pos]
                        insertion_cost = D[prev][cust] + D[cust][curr] - D[prev][curr]
                        if insertion_cost < best_increase:
                            best_increase = insertion_cost
                            best_pos = pos
                    if best_pos is None:
                        continue
                    removal_cost = D[route_from[cust_idx-1]][cust] + D[cust][route_from[cust_idx+1]] - D[route_from[cust_idx-1]][route_from[cust_idx+1]]
                    if best_increase - removal_cost < -1e-6:
                        new_route_from = route_from[:cust_idx] + route_from[cust_idx+1:]
                        new_route_to = route_to[:best_pos] + [cust] + route_to[best_pos:]
                        routes[i] = new_route_from
                        routes[j] = new_route_to
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
        iter_count += 1
    return routes

def solve_cvrp(n, Q, D, q):
    start_time = time.time()
    tracemalloc.start()
    
    # Phase 1: Base solution using Clarke-Wright savings algorithm
    phase1_start = time.time()
    routes = savings_algorithm(n, Q, D, q)
    phase1_time = time.time() - phase1_start
    
    # Phase 2: Local search improvement (random moves)
    phase2_start = time.time()
    routes = local_search(routes, n, Q, D, q, iterations=50)
    phase2_time = time.time() - phase2_start
    
    # Phase 3: Final deterministic 2-opt improvement on each route
    phase3_start = time.time()
    routes = final_2opt(routes, D, max_iter=50)
    phase3_time = time.time() - phase3_start

    # Phase 4: Inter-route relocate improvement to further reduce distance
    phase4_start = time.time()
    routes = inter_route_relocate(routes, D, q, Q, max_iter=10)
    phase4_time = time.time() - phase4_start

    total_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    total_distance = calculate_total_distance(routes, D)
    total_routes = len(routes)
    
    sys.stderr.write(f"Total distance: {total_distance}\n")
    sys.stderr.write(f"Total routes: {total_routes}\n")
    sys.stderr.write(f"Total runtime: {total_time:.6f} seconds\n")
    sys.stderr.write(f"  - Phase 1 (Savings): {phase1_time:.6f} seconds\n")
    sys.stderr.write(f"  - Phase 2 (Local Search): {phase2_time:.6f} seconds\n")
    sys.stderr.write(f"  - Phase 3 (Final 2-opt): {phase3_time:.6f} seconds\n")
    sys.stderr.write(f"  - Phase 4 (Inter-route Relocate): {phase4_time:.6f} seconds\n")
    sys.stderr.write(f"Memory usage: {current/10**6:.2f} MB (current) / {peak/10**6:.2f} MB (peak)\n")
    
    return routes

def check(routes, n, Q, D, q):
    visited_nodes = []
    for route in routes:
        demand_sum = sum(q[node] for node in route if node != 0)
        if demand_sum > Q:
            return False
        visited_nodes.extend(route)
    visited_customers = set(visited_nodes) - {0}
    if visited_customers != set(range(1, n)):
        return False
    return True

def main():
    n, Q, D, q = read_input()
    routes = solve_cvrp(n, Q, D, q)
    for route in routes:
        print(" ".join(map(str, route)))

if __name__ == "__main__":
    main()

import sys
import random
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
    """Optimize a route using nearest insertion heuristic."""
    if len(route) <= 3:
        return route
    
    optimized = [0, route[1], 0]
    remaining = set(route[2:-1])
    
    while remaining:
        best_cost = float('inf')
        best_node = None
        best_pos = None
        
        for node in remaining:
            # Try inserting this node at every possible position
            for pos in range(1, len(optimized)):
                prev = optimized[pos-1]
                curr = optimized[pos]
                
                # Calculate insertion cost
                insertion_cost = D[prev][node] + D[node][curr] - D[prev][curr]
                
                if insertion_cost < best_cost:
                    best_cost = insertion_cost
                    best_node = node
                    best_pos = pos
        
        # Insert the best node at the best position
        optimized.insert(best_pos, best_node)
        remaining.remove(best_node)
    
    return optimized

def savings_algorithm(n, Q, D, q):
    """Clarke-Wright savings algorithm for CVRP."""
    # Initialize with each customer in a separate route
    routes = [[0, i, 0] for i in range(1, n)]
    
    # Calculate savings for all customer pairs
    savings = []
    for i in range(1, n):
        for j in range(i+1, n):
            # Savings formula: s_ij = d_0i + d_0j - d_ij
            saving = D[0][i] + D[0][j] - D[i][j]
            savings.append((saving, i, j))
    
    # Sort savings in descending order
    savings.sort(reverse=True)
    
    # Track route assignments and depot-to-customer links
    node_to_route = {i: i-1 for i in range(1, n)}
    in_routes = set(range(len(routes)))
    demands = {i: q[routes[i][1]] for i in range(len(routes))}
    
    # Process savings list
    for saving, i, j in savings:
        route_i = node_to_route.get(i)
        route_j = node_to_route.get(j)
        
        # Skip if either node has been removed from its original route
        if route_i not in in_routes or route_j not in in_routes:
            continue
        
        # Skip if routes are already merged
        if route_i == route_j:
            continue
        
        # Check if i is at the end of its route (position before depot)
        i_at_end = routes[route_i][-2] == i
        
        # Check if j is at the start of its route (position after depot)
        j_at_start = routes[route_j][1] == j
        
        # Check if merging is possible based on capacity
        if i_at_end and j_at_start and demands[route_i] + demands[route_j] <= Q:
            # Merge routes: remove depots between i and j
            new_route = routes[route_i][:-1] + routes[route_j][1:]
            demands[route_i] = demands[route_i] + demands[route_j]
            
            # Update routes
            routes[route_i] = new_route
            in_routes.remove(route_j)
            
            # Update assignments for all nodes in route_j
            for node in routes[route_j][1:-1]:
                node_to_route[node] = route_i
            
            # Update demands
            demands[route_j] = 0
    
    # Collect the final routes
    final_routes = [routes[i] for i in in_routes]
    
    # Optimize each route using nearest insertion
    final_routes = [tsp_nearest_insertion(route, D) for route in final_routes]
    
    return final_routes

def local_search(routes, n, Q, D, q, iterations=100):
    """Improve routes with local search operations."""
    best_routes = routes.copy()
    best_distance = calculate_total_distance(best_routes, D)
    
    for _ in range(iterations):
        # Choose a random improvement strategy
        strategy = random.choice(['swap', 'relocate', '2-opt'])
        
        if strategy == 'swap' and len(routes) > 1:
            # Swap customers between routes
            route1_idx = random.randint(0, len(routes) - 1)
            route2_idx = random.randint(0, len(routes) - 1)
            while route2_idx == route1_idx:
                route2_idx = random.randint(0, len(routes) - 1)
                
            route1 = routes[route1_idx].copy()
            route2 = routes[route2_idx].copy()
            
            if len(route1) <= 3 or len(route2) <= 3:  # Skip routes with only one customer
                continue
                
            # Choose random customers to swap
            cust1_idx = random.randint(1, len(route1) - 2)
            cust2_idx = random.randint(1, len(route2) - 2)
            
            cust1 = route1[cust1_idx]
            cust2 = route2[cust2_idx]
            
            # Check capacity constraint
            new_demand1 = sum(q[i] for i in route1 if i != 0 and i != cust1) + q[cust2]
            new_demand2 = sum(q[i] for i in route2 if i != 0 and i != cust2) + q[cust1]
            
            if new_demand1 <= Q and new_demand2 <= Q:
                route1[cust1_idx] = cust2
                route2[cust2_idx] = cust1
                
                new_routes = routes.copy()
                new_routes[route1_idx] = route1
                new_routes[route2_idx] = route2
                
                new_distance = calculate_total_distance(new_routes, D)
                if new_distance < best_distance:
                    best_routes = new_routes
                    best_distance = new_distance
                    routes = new_routes
        
        elif strategy == 'relocate' and len(routes) > 1:
            # Move a customer to another route
            route1_idx = random.randint(0, len(routes) - 1)
            route2_idx = random.randint(0, len(routes) - 1)
            while route2_idx == route1_idx:
                route2_idx = random.randint(0, len(routes) - 1)
                
            route1 = routes[route1_idx].copy()
            route2 = routes[route2_idx].copy()
            
            if len(route1) <= 3:  # Must have at least one customer to relocate
                continue
                
            # Choose random customer to relocate
            cust_idx = random.randint(1, len(route1) - 2)
            cust = route1[cust_idx]
            
            # Check capacity constraint for destination route
            new_demand2 = sum(q[i] for i in route2 if i != 0) + q[cust]
            
            if new_demand2 <= Q:
                # Remove from route1
                route1.pop(cust_idx)
                
                # Insert into route2 at best position
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
                
                new_routes = routes.copy()
                new_routes[route1_idx] = route1
                new_routes[route2_idx] = route2
                
                new_distance = calculate_total_distance(new_routes, D)
                if new_distance < best_distance:
                    best_routes = new_routes
                    best_distance = new_distance
                    routes = new_routes
        
        elif strategy == '2-opt':
            # Internal route optimization with 2-opt
            route_idx = random.randint(0, len(routes) - 1)
            route = routes[route_idx].copy()
            
            if len(route) <= 4:  # Need at least 2 customers
                continue
            
            # Choose random segment to reverse
            i = random.randint(1, len(route) - 3)
            j = random.randint(i + 1, len(route) - 2)
            
            # Reverse the segment
            route[i:j+1] = reversed(route[i:j+1])
            
            new_routes = routes.copy()
            new_routes[route_idx] = route
            
            new_distance = calculate_total_distance(new_routes, D)
            if new_distance < best_distance:
                best_routes = new_routes
                best_distance = new_distance
                routes = new_routes
    
    return best_routes

def calculate_total_distance(routes, D):
    """Calculate the total distance of all routes."""
    total = 0
    for route in routes:
        for i in range(len(route) - 1):
            total += D[route[i]][route[i+1]]
    return total

def solve_cvrp(n, Q, D, q):
    routes = savings_algorithm(n, Q, D, q)
    routes = local_search(routes, n, Q, D, q, iterations=50)
    
    return routes

def check(routes, n, Q, D, q):
    # Basic feasibility checks
    visited_nodes = []
    for route in routes:
        # Check capacity
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
#!/usr/bin/env python3
import os
import sys
import time
import csv
import tracemalloc
import random
import importlib.util
from glob import glob

# --- CONFIGURATION ---
EXAMPLES_DIR = 'example_testcases'
# Problem sizes to benchmark
RANDOM_SIZES = [10, 100, 1000]
# Vehicle capacity factor (Q = n * Q_FACTOR)
Q_FACTOR     = 10
# Repetitions per random instance
RANDOM_REPS  = 1
# ----------------------

def discover_solvers():
    """Auto‑discover all Python modules in this dir that define solve_cvrp."""
    me = os.path.basename(__file__)
    solvers = {}
    for fn in os.listdir('.'):
        if fn.endswith('.py') and fn != me:
            name = fn[:-3]
            spec = importlib.util.spec_from_file_location(name, fn)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'solve_cvrp'):
                solvers[name] = mod.solve_cvrp
    return solvers

def read_instance(path):
    """Read a .in file from example_testcases."""
    with open(path) as f:
        n = int(f.readline())
        Q = int(f.readline())
        D = [list(map(int, f.readline().split())) for _ in range(n)]
        q = list(map(int, f.readline().split()))
    return n, Q, D, q

def generate_instance(n, Q):
    """Generate random symmetric distance matrix D and demand vector q."""
    D = [[0 if i==j else random.randint(1,100) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            D[j][i] = D[i][j]
    q = [0] + [random.randint(1, Q//2) for _ in range(n-1)]
    return n, Q, D, q

def calc_distance(routes, D):
    """Sum total distance of all routes."""
    total = 0
    for r in routes:
        for i in range(len(r)-1):
            total += D[r[i]][r[i+1]]
    return total

def check_feasible(routes, n, Q, q):
    """Verify capacity and that every customer 1..n-1 is visited."""
    visited = []
    for r in routes:
        load = sum(q[i] for i in r if i != 0)
        if load > Q:
            return False
        visited += r
    return set(visited) >= set(range(1, n))

def benchmark_full():
    solvers = discover_solvers()
    if not solvers:
        print(" No solvers found! Place your solver .py files here.", file=sys.stderr)
        sys.exit(1)

    out = 'benchmark_full.csv'
    with open(out, 'w', newline='') as csvf:
        w = csv.writer(csvf)
        w.writerow([
            'solver','test_type','case','n','Q',
            'time_s','peak_mem_mb','total_dist','route_count','feasible'
        ])

        # 1) Official example testcases
        for path in sorted(glob(os.path.join(EXAMPLES_DIR, '*.in'))):
            case = os.path.basename(path)
            n, Q, D, q = read_instance(path)
            for name, solver in solvers.items():
                tracemalloc.start()
                t0 = time.perf_counter()
                routes = solver(n, Q, D, q)
                t1 = time.perf_counter()
                curr, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                dist = calc_distance(routes, D)
                feas = check_feasible(routes, n, Q, q)
                w.writerow([
                    name, 'example', case, n, Q,
                    f"{(t1-t0):.6f}", f"{peak/1e6:.2f}",
                    dist, len(routes), feas
                ])

        # 2) Random instances
        for n in RANDOM_SIZES:
            Q = n * Q_FACTOR
            for rep in range(1, RANDOM_REPS+1):
                _, _, D, q = generate_instance(n, Q)
                case = f"rand_{n}_{rep}"
                for name, solver in solvers.items():
                    tracemalloc.start()
                    t0 = time.perf_counter()
                    routes = solver(n, Q, D, q)
                    t1 = time.perf_counter()
                    curr, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    dist = calc_distance(routes, D)
                    feas = check_feasible(routes, n, Q, q)
                    w.writerow([
                        name, 'random', case, n, Q,
                        f"{(t1-t0):.6f}", f"{peak/1e6:.2f}",
                        dist, len(routes), feas
                    ])

    print(f"Benchmark complete: {out}")

if __name__ == '__main__':
    benchmark_full()

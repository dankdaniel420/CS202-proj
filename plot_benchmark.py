import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
CSV_FILE = 'benchmark_full.csv'
if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(f"Cannot find {CSV_FILE} in current directory")

df = pd.read_csv(CSV_FILE)

# Ensure proper types
df['n'] = df['n'].astype(int)
df['time_s'] = pd.to_numeric(df['time_s'])
df['peak_mem_mb'] = pd.to_numeric(df['peak_mem_mb'])
df['total_dist'] = pd.to_numeric(df['total_dist'])
df['route_count'] = df['route_count'].astype(int)

# Focus on random instances for scaling plots
rand = df[df['test_type'] == 'random']

def plot_and_save(x, y, ylabel, title, filename):
    plt.figure()
    for solver in rand['solver'].unique():
        grp = rand[rand['solver'] == solver].groupby(x)[y].mean().reset_index()
        plt.plot(grp[x], grp[y], marker='o', label=solver)
    plt.xlabel('Problem size (n)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")

# 1) Runtime vs Problem Size
plot_and_save(
    x='n',
    y='time_s',
    ylabel='Avg runtime (s)',
    title='Runtime vs Problem Size',
    filename='runtime_vs_n.png'
)

# 2) Memory vs Problem Size
plot_and_save(
    x='n',
    y='peak_mem_mb',
    ylabel='Avg peak memory (MB)',
    title='Memory Usage vs Problem Size',
    filename='memory_vs_n.png'
)

# 3) Solution Quality vs Problem Size
plot_and_save(
    x='n',
    y='total_dist',
    ylabel='Avg total distance',
    title='Solution Quality vs Problem Size',
    filename='distance_vs_n.png'
)

# 4) Route Count vs Problem Size
plot_and_save(
    x='n',
    y='route_count',
    ylabel='Avg number of routes',
    title='Route Count vs Problem Size',
    filename='routes_vs_n.png'
)

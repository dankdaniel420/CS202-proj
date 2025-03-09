import random

random.seed('knapsack')
n = 20
weight = []
for _ in range(n):
    while True:
        i = random.randint(4*n, 6*n)
        if i not in weight:
            weight.append(i)
            break
sum_weight = sum(weight)
value = [0] * n
for i in range(n):
    value[i] = random.randint(5*weight[i], 6*weight[i])

weight_limit = sum_weight // 2

print('generating data...')
print('list of "item:weight:value":')
print(' '.join(['item_'+str(i+1)+':'+str(weight[i])+':'+str(value[i]) for i in range(n)]))
print('knapsack capacity:', weight_limit)

# if the final maximum value is the only concern
knapsack = [[0] * (weight_limit+1) for _ in range(n+1)]
for i in range(n):
    for j in range(1, weight_limit+1):
        knapsack[i+1][j] = knapsack[i][j]
        if j >= weight[i]:
            m = knapsack[i][j-weight[i]]+value[i]
            if m > knapsack[i+1][j]:
                knapsack[i+1][j] = m

print('maximum value for this knapsack:', knapsack[n][weight_limit])

# validate with enumeration
import itertools
curr_best = 0
for k in range(n+1):
    for l in list(itertools.combinations(range(n), k)):
        w_sum, v_sum = 0, 0
        for i in l:
            w_sum += weight[i]
            v_sum += value[i]
        if w_sum <= weight_limit and v_sum > curr_best:
            curr_best = v_sum
print('result from brute-force enumerating all combinations:', curr_best)

# however, we would like to know which item are selected

knapsack = [[0] * (weight_limit+1) for _ in range(n+1)]
choose = [[False] * (weight_limit+1) for _ in range(n)]
for i in range(n):
    for j in range(1, weight_limit+1):
        knapsack[i+1][j] = knapsack[i][j]
        if j >= weight[i]:
            m = knapsack[i][j-weight[i]]+value[i]
            if m > knapsack[i+1][j]:
                knapsack[i+1][j] = m
                choose[i][j] = True

print('maximum value for this knapsack:', knapsack[n][weight_limit])
chosen, j = [], weight_limit
for i in range(n-1, -1, -1):
    if choose[i][j]:
        chosen.append(i)
        j -= weight[i]
chosen = chosen[::-1]
print('selected items are:')
print(' '.join(['item_'+str(i+1)+':'+str(weight[i])+':'+str(value[i]) for i in chosen]))

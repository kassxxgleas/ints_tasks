import random
import time
import matplotlib.pyplot as plt

# -----------------------------
# 1. Activity Selection Variants
# -----------------------------
def greedy_finish(tasks):
    tasks = sorted(tasks, key=lambda x: x[1])
    selected, last_end = [], 0
    for start, end in tasks:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected

def greedy_start(tasks):
    tasks = sorted(tasks, key=lambda x: x[0])
    selected, last_end = [], 0
    for start, end in tasks:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected

def greedy_shortest(tasks):
    tasks = sorted(tasks, key=lambda x: (x[1] - x[0]))
    selected, last_end = [], 0
    for start, end in tasks:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected

def randomized_greedy(tasks, p=0.2):
    tasks = sorted(tasks, key=lambda x: x[1])
    selected, last_end = [], 0
    for start, end in tasks:
        if start >= last_end:
            if random.random() > p or random.random() > 0.5:
                selected.append((start, end))
                last_end = end
    return selected

# -----------------------------
# 2. Fractional Knapsack Variants
# -----------------------------
def fractional_knapsack(cap, items):
    items = sorted(items, key=lambda x: x[1]/x[0], reverse=True)
    val, w = 0, 0
    for weight, value in items:
        if w >= cap: break
        take = min(weight, cap - w)
        val += value * (take / weight)
        w += take
    return val

def randomized_fractional(cap, items, p=0.2):
    items = sorted(items, key=lambda x: x[1]/x[0], reverse=True)
    val, w = 0, 0
    for weight, value in items:
        if w >= cap: break
        if random.random() > p:
            take = min(weight, cap - w)
        else:
            take = min(weight, cap - w) * random.random()
        val += value * (take / weight)
        w += take
    return val

# -----------------------------
# Utilities
# -----------------------------
def gen_activities(n):
    return [(random.randint(0, 90), random.randint(10, 100)) for _ in range(n)]

def gen_items(n):
    return [(random.randint(1, 50), random.randint(10, 100)) for _ in range(n)]

# -----------------------------
# Experiments
# -----------------------------
# Activity Selection
sizes = [10, 50, 100, 500]
variants_act = {
    'Greedy-Finish': greedy_finish,
    'Greedy-Start': greedy_start,
    'Shortest-Duration': greedy_shortest,
    'Randomized': lambda a: randomized_greedy(a, 0.2)
}
results_act = {name: [] for name in variants_act}
counts_act = {name: [] for name in variants_act}

for n in sizes:
    acts = gen_activities(n)
    for name, fn in variants_act.items():
        t_sum = 0
        c_sum = 0
        for _ in range(10):
            start = time.time()
            sel = fn(acts)
            t_sum += (time.time() - start) * 1000
            c_sum += len(sel)
        results_act[name].append(t_sum / 10)
        counts_act[name].append(c_sum / 10)

# Fractional Knapsack
sizes_k = [10, 50, 100]
variants_knap = {
    'Greedy': lambda items: fractional_knapsack(100 if len(items) > 10 else 50, items),
    'Randomized': lambda items: randomized_fractional(100 if len(items) > 10 else 50, items, 0.2)
}
results_knap = {name: [] for name in variants_knap}
values_knap = {name: [] for name in variants_knap}

for n in sizes_k:
    items = gen_items(n)
    for name, fn in variants_knap.items():
        t_sum = 0
        v_sum = 0
        for _ in range(10):
            start = time.time()
            v = fn(items)
            t_sum += (time.time() - start) * 1000
            v_sum += v
        results_knap[name].append(t_sum / 10)
        values_knap[name].append(v_sum / 10)

# -----------------------------
# Print Tables
# -----------------------------
print("Activity Selection Results (time ms / avg count):")
print("| n | " + " | ".join(f"{name}" for name in variants_act) + " |")
print("|---|" + "|".join("---" for _ in variants_act) + "|")
for i, n in enumerate(sizes):
    row = f"| {n} | " + " | ".join(f"{results_act[name][i]:.3f} / {counts_act[name][i]:.1f}"
                                for name in variants_act) + " |"
    print(row)

print("\nFractional Knapsack Results (time ms / avg value):")
print("| n | " + " | ".join(f"{name}" for name in variants_knap) + " |")
print("|---|" + "|".join("---" for _ in variants_knap) + "|")
for i, n in enumerate(sizes_k):
    row = f"| {n} | " + " | ".join(f"{results_knap[name][i]:.3f} / {values_knap[name][i]:.1f}"
                                for name in variants_knap) + " |"
    print(row)

# -----------------------------
# Plotting Comparisons
# -----------------------------
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for name, vals in results_act.items():
    plt.plot(sizes, vals, marker='o', label=name)
plt.title('Activity Selection Variants')
plt.xlabel('n')
plt.ylabel('Avg time (ms)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
for name, vals in results_knap.items():
    plt.plot(sizes_k, vals, marker='s', label=name)
plt.title('Fractional Knapsack Variants')
plt.xlabel('n')
plt.ylabel('Avg time (ms)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

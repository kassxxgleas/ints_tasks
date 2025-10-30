import time
import matplotlib.pyplot as plt
import numpy as np
import random
# ============================================================================
# INTERVAL SCHEDULING
# ============================================================================

class Activity:
    def __init__(self, name, start, finish):
        self.name = name
        self.start = start
        self.finish = finish
        self.duration = finish - start
    
    def __repr__(self):
        return f"{self.name}[{self.start}-{self.finish}]"
    
    def conflicts_with(self, other):
        return not (self.finish <= other.start or other.finish <= self.start)

def interval_scheduling_earliest_finish(activities):
    if not activities:
        return []
    sorted_activities = sorted(activities, key=lambda a: (a.finish, a.start))
    selected = [sorted_activities[0]]
    last_finish = sorted_activities[0].finish
    for activity in sorted_activities[1:]:
        if activity.start >= last_finish:
            selected.append(activity)
            last_finish = activity.finish
    return selected

def interval_scheduling_earliest_start(activities):
    if not activities:
        return []
    sorted_activities = sorted(activities, key=lambda a: (a.start, a.finish))
    selected = [sorted_activities[0]]
    last_finish = sorted_activities[0].finish
    for activity in sorted_activities[1:]:
        if activity.start >= last_finish:
            selected.append(activity)
            last_finish = activity.finish
    return selected

def interval_scheduling_shortest_duration(activities):
    if not activities:
        return []
    sorted_activities = sorted(activities, key=lambda a: (a.duration, a.start))
    selected = [sorted_activities[0]]
    for activity in sorted_activities[1:]:
        has_conflict = any(activity.conflicts_with(s) for s in selected)
        if not has_conflict:
            selected.append(activity)
    return selected

def interval_scheduling_random(activities, seed=42):
    if not activities:
        return []
    random.seed(seed)
    shuffled = activities.copy()
    random.shuffle(shuffled)
    selected = [shuffled[0]]
    for activity in shuffled[1:]:
        has_conflict = any(activity.conflicts_with(s) for s in selected)
        if not has_conflict:
            selected.append(activity)
    return selected

# ============================================================================
# COIN CHANGE PROBLEM
# ============================================================================

def coin_change_greedy(coins, amount):
    if amount == 0:
        return 0, []
    sorted_coins = sorted(coins, reverse=True)
    result = []
    remaining = amount
    for coin in sorted_coins:
        while remaining >= coin:
            result.append(coin)
            remaining -= coin
    if remaining > 0:
        return -1, []
    return len(result), result

def coin_change_dynamic_programming(coins, amount):
    if amount == 0:
        return 0, []
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin
    if dp[amount] == float('inf'):
        return -1, []
    result = []
    current = amount
    while current > 0:
        coin_used = parent[current]
        result.append(coin_used)
        current -= coin_used
    return dp[amount], result

# ============================================================================
# GENEROVANIE VSTUPNÝCH DÁT
# ============================================================================

def generate_interval_scheduling_dataset(num_activities, time_range, seed=42):
    random.seed(seed)
    activities = []
    for i in range(num_activities):
        start = random.randint(0, time_range - 5)
        duration = random.randint(1, min(10, time_range - start))
        finish = start + duration
        activities.append(Activity(f"A{i+1}", start, finish))
    return activities

def generate_coin_change_datasets():
    return [
        ([1, 5, 10, 25], 63, "US coins"),
        ([1, 2, 5, 10, 20, 50], 87, "EU cents"),
        ([1, 5, 10, 25], 999, "Large"),
        ([1, 6, 10], 12, "6,10 sys"),
        ([1, 5, 6, 9], 11, "5,6,9 sys"),
        ([1, 7, 10], 14, "7,10 sys"),
        ([1, 3, 4], 6, "3,4 sys"),
        ([1, 5, 10], 1, "Small"),
        ([1, 5, 10, 25, 50], 100, "Medium"),
    ]

# ============================================================================
# EXPERIMENTY
# ============================================================================

def run_interval_scheduling_experiments():
    print("="*80)
    print("INTERVAL SCHEDULING")
    print("="*80)
    
    strategies = [
        ("EFT", interval_scheduling_earliest_finish),
        ("EST", interval_scheduling_earliest_start),
        ("SDF", interval_scheduling_shortest_duration),
        ("Random", interval_scheduling_random),
    ]
    
    test_sizes = [10, 20, 30, 50, 100]
    results = []
    
    for size in test_sizes:
        print(f"\nDataset: {size}")
        activities = generate_interval_scheduling_dataset(size, size * 2, seed=size)
        
        for strategy_name, strategy_func in strategies:
            start_time = time.perf_counter()
            selected = strategy_func(activities)
            exec_time = (time.perf_counter() - start_time) * 1000
            
            results.append({
                'size': size,
                'strategy': strategy_name,
                'count': len(selected),
                'time': exec_time
            })
            print(f"  {strategy_name:8s}: {len(selected):3d} activities")
    return results

def run_coin_change_experiments():
    print("\n" + "="*80)
    print("COIN CHANGE PROBLEM")
    print("="*80)
    
    datasets = generate_coin_change_datasets()
    results = []
    
    for coins, amount, description in datasets:
        print(f"\n{description}: {coins}, sum={amount}")
        
        start_time = time.perf_counter()
        greedy_count, _ = coin_change_greedy(coins, amount)
        greedy_time = (time.perf_counter() - start_time) * 1000
        
        start_time = time.perf_counter()
        dp_count, _ = coin_change_dynamic_programming(coins, amount)
        dp_time = (time.perf_counter() - start_time) * 1000
        
        if greedy_count != -1 and dp_count != -1:
            optimal = greedy_count == dp_count
            difference = greedy_count - dp_count
        else:
            optimal = False
            difference = None
        
        results.append({
            'description': description,
            'greedy_count': greedy_count if greedy_count != -1 else None,
            'greedy_time': greedy_time,
            'dp_count': dp_count if dp_count != -1 else None,
            'dp_time': dp_time,
            'optimal': optimal,
            'difference': difference
        })
        print(f"  Greedy: {greedy_count if greedy_count != -1 else 'N/A'}, DP: {dp_count if dp_count != -1 else 'N/A'}")
    return results

# ============================================================================
# VIZUALIZÁCIA
# ============================================================================

def plot_results(interval_results, coin_results):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    strategies = list(set(r['strategy'] for r in interval_results))
    sizes = sorted(set(r['size'] for r in interval_results))
    
    # 1-2: Interval Scheduling
    for i, (metric, ylabel, title) in enumerate([
        ('count', 'Selected Activities', 'Quality'),
        ('time', 'Time (ms)', 'Performance')
    ]):
        for strategy in strategies:
            data = sorted([r for r in interval_results if r['strategy'] == strategy], 
                         key=lambda x: x['size'])
            axes[0, i].plot(sizes, [r[metric] for r in data], 
                          marker='o' if i == 0 else 's', label=strategy, linewidth=2)
        axes[0, i].set_xlabel('Dataset Size')
        axes[0, i].set_ylabel(ylabel)
        axes[0, i].set_title(f'Interval Scheduling: {title}')
        axes[0, i].legend()
        axes[0, i].grid(True, alpha=0.3)
    
    # 3: Interval Scheduling
    optimal_counts = [sum(1 for size in sizes 
                         if max(r['count'] for r in interval_results if r['size'] == size) ==
                         next(r['count'] for r in interval_results 
                              if r['size'] == size and r['strategy'] == strategy))
                     for strategy in strategies]
    axes[0, 2].bar(strategies, optimal_counts, 
                   color=['#2ca02c', '#ff7f0e', '#d62728', '#9467bd'])
    axes[0, 2].set_ylabel('Optimal Solutions')
    axes[0, 2].set_title('Interval Scheduling:Optimality Rate')
    axes[0, 2].set_ylim(0, len(sizes) + 0.5)
    for i, v in enumerate(optimal_counts):
        axes[0, 2].text(i, v + 0.1, f'{v}/{len(sizes)}', ha='center', fontweight='bold')
    
    # 4-5: Coin Change
    valid = [r for r in coin_results if r['greedy_count'] is not None]
    x_pos = np.arange(len(valid))
    width = 0.35
    
    for i, (metric, ylabel, title) in enumerate([
        ('_count', 'Coins', 'Quality'),
        ('_time', 'Time (ms)', 'Performance')
    ]):
        axes[1, i].bar(x_pos - width/2, [r[f'greedy{metric}'] for r in valid],
                      width, label='Greedy', color='#ff7f0e')
        axes[1, i].bar(x_pos + width/2, [r[f'dp{metric}'] for r in valid],
                      width, label='DP', color='#2ca02c')
        axes[1, i].set_xlabel('Test Cases')
        axes[1, i].set_ylabel(ylabel)
        axes[1, i].set_title(f'Coin Change: {title}')
        axes[1, i].set_xticks(x_pos)
        axes[1, i].set_xticklabels([r['description'] for r in valid], 
                                   rotation=45, ha='right')
        axes[1, i].legend()
        axes[1, i].grid(True, alpha=0.3, axis='y')
    
    # 6: Coin Change
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('HI_HOP/results.png', dpi=300, bbox_inches='tight')
    plt.close()
# ============================================================================
# MAIN
# ============================================================================

def main():
    interval_results = run_interval_scheduling_experiments()
    coin_results = run_coin_change_experiments()
    
    plot_results(interval_results, coin_results)
    

if __name__ == "__main__":
    main()
# Analýza Greedy Algoritmov: Interval Scheduling a Coin Change Problem

## Úvod

Tento projekt porovnáva rôzne **greedy heurístiky** na dvoch klasických optimalizačných problémoch:
- **Interval Scheduling**: Výber maximálneho počtu nezapadajúcich aktivít
- **Coin Change Problem**: Minimalizácia počtu mincí na daný obnos

Cieľom je demonštrovať, že greedy algoritmy nie sú vždy optimálne a že výber správnej stratégie má kritický vplyv na kvalitu a výkon.

---

## 1. INTERVAL SCHEDULING

### Problém

Máme súbor aktivít s časom začatia a konca. Cieľom je vybrať **maximálny počet aktivít, ktoré sa vzájomne neprekrývajú sa**.

### Dátová Trieda: Activity

```python
class Activity:
    """Reprezentuje jednu aktivitu s časovým intervalom."""
    
    def __init__(self, name, start, finish):
        """
        Inicializácia aktivity.
        : Ukladáme všetky informácie potrebné na manipuláciu s aktivitami.
        """
        self.name = name
        self.start = start
        self.finish = finish
        self.duration = finish - start  # Trvanie = koniec - začiatok
    
    def __repr__(self):
        """
        Definuje textovú reprezentáciu aktivity.
        """
        return f"{self.name}[{self.start}-{self.finish}]"
    
    def conflicts_with(self, other):
        """
        Zistí, či dve aktivity sa neprekrývajú.
        
            Dve aktivity sa NEZAPADAJÚ iba ak:
            - Prvá skončí pred tým, ako druhá začne: self.finish <= other.start
            - Alebo druhá skončí pred tým, ako prvá začne: other.finish <= self.start
            
            Ak ani jedno nie je pravda, zapadajú sa.
        """
        return not (self.finish <= other.start or other.finish <= self.start)
```

### Stratégia 1: Earliest Finish Time (EFT) - OPTIMÁLNA

```python
def interval_scheduling_earliest_finish(activities):
    """
    - Greedy voľba lokálne optimálna → globálne optimálna

    ČASOVÁ KOMPLEXNOSŤ: O(n log n) - kvôli triedeniu
    PRIESTOROVÁ KOMPLEXNOSŤ: O(n) - na ukladanie vybraných aktivít
    """
    if not activities:
        return []
    
    # KROK 1: Triedenie podľa času ukončenia, potom podľa začatia
    sorted_activities = sorted(activities, key=lambda a: (a.finish, a.start))
    
    # KROK 2: Vždy vyberáme prvú aktivitu
    selected = [sorted_activities[0]]
    last_finish = sorted_activities[0].finish
    
    # KROK 3: Greedy voľba - vyberieme, ak sa nezapadá s poslednou
    for activity in sorted_activities[1:]:
        if activity.start >= last_finish:  # Bez prekrytia
            selected.append(activity)
            last_finish = activity.finish
    
    return selected
```

**Výsledok**: V 100% prípadov dáva optimálne riešenie.

---

### Stratégia 2: Earliest Start Time (EST)

```python
def interval_scheduling_earliest_start(activities):
    """
    PREČO JE SUBOPTIMÁLNA:
        Príklad: [(1,10), (2,3), (4,5)]
        - EST: Vyberie (1,10), potom nemôže vybrať (2,3) ani (4,5) = 1 aktivita
        - EFT: Vyberie (2,3), potom (4,5) = 2 aktivity ✓
        
        Zatiaľ čo (1,10) začína skôr, blokuje veľa ďalších aktivít!

    """
    if not activities:
        return []
    
    # Triedenie podľa času začatia (opačný prístup ako EFT)
    sorted_activities = sorted(activities, key=lambda a: (a.start, a.finish))
    selected = [sorted_activities[0]]
    last_finish = sorted_activities[0].finish
    
    for activity in sorted_activities[1:]:
        if activity.start >= last_finish:
            selected.append(activity)
            last_finish = activity.finish
    
    return selected
```

**Výsledok**: Dáva slabšie výsledky ako EFT, ale niekedy funguje.

---

### Stratégia 3: Shortest Duration First (SDF)

```python
def interval_scheduling_shortest_duration(activities):
    """
    PRÍKLAD: [(1,2), (1,10), (3,4)]
        - SDF: (1,2) má trvanie 1, (3,4) má trvanie 1
          Vyberie (1,2), potom (3,4) = 2 aktivity
        - Ale (1,10) má trvanie 9, (1,2) samo = vyberie (1,2) = 1 aktivita
        
        V tomto prípade sa to rovná, ale všeobecne to negarantuje optimálnosť.
    
    PROBLÉM: Trvanie je absolútne nezávislé od toho, kedy sa aktivita 
             končí. Koniec je dôležitý!
    """
    if not activities:
        return []
    
    # Triedenie podľa trvania, potom podľa času začatia
    sorted_activities = sorted(activities, key=lambda a: (a.duration, a.start))
    selected = [sorted_activities[0]]
    
    for activity in sorted_activities[1:]:
        # Tu kontrolujeme konflikt s KAŽDOU vybratou aktivitou
        has_conflict = any(activity.conflicts_with(s) for s in selected)
        if not has_conflict:
            selected.append(activity)
    
    return selected
```

**Výsledok**: Nepredvídateľné, často horší výkon ako EFT.

---

### Stratégia 4: Random Order (RND)

```python
def interval_scheduling_random(activities, seed=42):
    """
    ÚČEL TEJTO STRATÉGIE:
    - Demonštrácia toho, čo sa stane, keď greedy voľba nie je inteligentná
    - Baseline pre porovnanie - "aspoň lepšie ako náhodné"
    
    VÝKON: Hrôzny - zvyčajne oveľa menej aktivít ako EFT
    """
    if not activities:
        return []
    
    random.seed(seed)
    shuffled = activities.copy()  # Duplikát, aby sme nemodifikovali originál
    random.shuffle(shuffled)  # Náhodné premiešanie
    
    selected = [shuffled[0]]
    for activity in shuffled[1:]:
        has_conflict = any(activity.conflicts_with(s) for s in selected)
        if not has_conflict:
            selected.append(activity)
    
    return selected
```

**Výsledok**: Podľa množstva náhody, zvyčajne najhorší.

---

## 2. COIN CHANGE PROBLEM

### Problém

Máme súbor mincí s danými hodnotami. Cieľom je nájsť **minimálny počet mincí** na vytvorenie presnej sumy.

---

### Stratégia 1: Greedy Algoritmus - ČI JE OPTIMÁLNY?

```python
def coin_change_greedy(coins, amount):
    """
    GREEDY STRATÉGIA: Vždy vyberieme najväčšiu mincu, ktorá sa zmestí.
    
    ALGORITMUS:
    1. Zoradiť mince v zostupnom poradí (od najväčšej)
    2. Dokiaľ nie je suma 0:
       - Vziať najväčšiu mincu menšiu alebo rovnú súčasnej sume
       - Odčítať z sumy, pridať do výsledku
       - Opakovať
    3. Ak po skončení suma ≠ 0, vrátenie -1 (nemožné)
    
    PROBLÉM - GREEDY NIE JE VŽDY OPTIMÁLNY:
    
    Príklad 1: coins=[1, 6, 10], amount=12
        - Greedy: 10 + 1 + 1 = 3 mince
        - Optimálne: 6 + 6 = 2 mince
    
    Príklad 2: coins=[1, 5, 6, 9], amount=11
        - Greedy: 9 + 1 + 1 = 3 mince
        - Optimálne: 5 + 6 = 2 mince
    
    Príklad 3: coins=[1, 3, 4], amount=6
        - Greedy: 4 + 1 + 1 = 3 mince
        - Optimálne: 3 + 3 = 2 mince
    
    ZÁVER: Greedy funguje len pre niektoré množiny mincí (napr. USD, EUR).
           Pre iné množiny je úplne nevhodný!
    
    """
    if amount == 0:
        return 0, []
    
    sorted_coins = sorted(coins, reverse=True)  # Najväčšie mince prvé
    result = []
    remaining = amount
    
    # Hladový výber - najväčšia možná minca v každom kroku
    for coin in sorted_coins:
        while remaining >= coin:
            result.append(coin)
            remaining -= coin
    
    # Ak nám ostala nejaká suma, je to nemožné
    if remaining > 0:
        return -1, []
    
    return len(result), result
```

---

### Stratégia 2: Dynamic Programming - GARANTOVANE OPTIMÁLNY ✓

```python
def coin_change_dynamic_programming(coins, amount):
    """
    DYNAMIC PROGRAMMING RIEŠENIE - OPTIMÁLNE.
    
    - Rozbijeme problém na čiastkové problémy
    - Riešime každý čiastkový problém raz a ukladáme si výsledok
    - Kombinujeme čiastkové riešenia na vytvorenie celkového riešenia
    
    DEFINÍCIA DP STATE:
    dp[i] = minimálny počet mincí na vytvorenie sumy i
    
    PRECHODOVÁ FUNKCIA:
    Pre každú sumu i a každú mincu c:
        dp[i] = min(dp[i], dp[i-c] + 1)
    
    Vysvetlenie: Ak máme sumu i, môžeme:
    1. Vzať mincu c a mať sumu i-c (ktorá má dp[i-c] mincí)
    2. Pridať 1 za mincu c
    3. Porovnať s predchádzajúcim najlepším riešením
    
    PRÍKLAD: coins=[1,6,10], amount=12
    ┌─────────────────────────────────────────┐
    │ i  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │... 12 │
    ├─────────────────────────────────────────┤
    │ dp │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 1 │... 2 │
    │ op │ - │ 1 │ 1 │ 1 │ 1 │ 1 │ 6 │... 6 │
    └─────────────────────────────────────────┘
    
    dp[12] = 2 (pomocou 6+6), parent[12] = 6
             → dp[6] = 1 (pomocou 6), parent[6] = 6
             → Výsledok: [6, 6]
    
    ČASOVÁ KOMPLEXNOSŤ: O(n * amount), kde n = počet mincí
                        - V praxi rýchlejšie ako sa zdá
    PRIESTOROVÁ KOMPLEXNOSŤ: O(amount) na dp a parent polia
    
    if amount == 0:
        return 0, []
    
    # INICIALIZÁCIA
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Suma 0 potrebuje 0 mincí
    parent = [-1] * (amount + 1)  # Na rekonštrukciu riešenia
    
    # VYPLNENIE DP TABUĽKY
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin  # Zapamätáme si, ktorú mincu sme použili
    
    # CHECK NEMOŽNOSTI
    if dp[amount] == float('inf'):
        return -1, []
    
    # REKONŠTRUKCIA RIEŠENIA - SPÄTNÝ CHOD
    result = []
    current = amount
    while current > 0:
        coin_used = parent[current]
        result.append(coin_used)
        current -= coin_used
    
    return dp[amount], result
```

**Výsledok**: Vždy garantuje optimálne riešenie.

---

## 3. GENEROVANIE TESTOVACÍCH DÁT

```python
def generate_interval_scheduling_dataset(num_activities, time_range, seed=42):
    """
    Generuje náhodné aktivity pre testovanie.
    
    PARAMETRY:
    - num_activities: Počet aktivít na vygenerovanie
    - time_range: Časový rozsah [0, time_range]
    - seed: Reprodukovateľnosť
    
    LOGIKA GENEROVANIA:
    1. Pre každú aktivitu: náhodný začiatok v rozsahu [0, time_range - 5]
    2. Náhodné trvanie: [1, min(10, time_range - start)]
    3. Koniec = začiatok + trvanie
    
    WHY "time_range - 5":
    Chceme byť v bezpečí pred hraničnými prípadmi
    """
    random.seed(seed)
    activities = []
    for i in range(num_activities):
        start = random.randint(0, time_range - 5)
        duration = random.randint(1, min(10, time_range - start))
        finish = start + duration
        activities.append(Activity(f"A{i+1}", start, finish))
    return activities

def generate_coin_change_datasets():
    """
    Množina testovacích prípadov pre coin change.

    1. [1,5,10,25], 63 - "US coins": 
       Greedy funguje
    
    2. [1,2,5,10,20,50], 87 - "EU cents":
       Greedy funguje optimálne pre eurá
    
    3. [1,5,10,25], 999 - "Large":
       Veľké číslo - meranie výkonu na väčších prípadoch
    
    4. [1,6,10], 12 - "6,10 sys":
       KLASICKÝ FAIL GREEDY, Greedy=3 (10+1+1), Optimal=2 (6+6)
    
    5. [1,5,6,9], 11 - "5,6,9 sys":
       FAIL, Greedy=3 (9+1+1), Optimal=2 (5+6)
    
    6. [1,7,10], 14 - "7,10 sys":
       Zaujímavý prípad - test robustnosti
    
    7. [1,3,4], 6 - "3,4 sys":
       FAIL, Greedy=3 (4+1+1), Optimal=2 (3+3)
    
    8. [1,5,10], 1 - "Small":
       Minimálny prípad - hraničný test
    
    9. [1,5,10,25,50], 100 - "Medium":
       Stredný prípad
    
    ?: Demonštrujeme, že greedy nie je univerzálny!
    """
    return [
        ([1, 5, 10, 25], 63, "US coins"),
        ([1, 2, 5, 10, 20, 50], 87, "EU cents"),
        ([1, 5, 10, 25], 999, "Large"),
        ([1, 6, 10], 12, "6,10 sys"),  # GREEDY FAILS
        ([1, 5, 6, 9], 11, "5,6,9 sys"),  # GREEDY FAILS
        ([1, 7, 10], 14, "7,10 sys"),
        ([1, 3, 4], 6, "3,4 sys"),  # GREEDY FAILS
        ([1, 5, 10], 1, "Small"),
        ([1, 5, 10, 25, 50], 100, "Medium"),
    ]
```

---

## 4. EXPERIMENTY A MERANIE VÝKONU

```python
def run_interval_scheduling_experiments():
    """
    Porovnanie všetkých 4 stratégií na interval scheduling.
    
    EXPERIMENTY:
    - Testovanie na rôznych veľkostiach: 10, 20, 30, 50, 100 aktivít
    - Meranie: počet vybratých aktivít (kvalita) a čas (výkon)
    - Porovnanie stratégií
    
    METRIKY:
    1. count: Počet vybratých aktivít
       - Vyššie = lepšie (chceme viac aktivít)
    
    2. time: Čas vykonania v ms
       - Nižšie = lepšie
       - Čakáme: O(n log n) pre všetky
    
    OČAKÁVANÉ VÝSLEDKY:
    - EFT: najlepší v kvalite
    - EST: Často horší
    - SDF: Nepredvídateľný
    - RND: Najhorší
    """
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
            # MERANIE ČASU
            start_time = time.perf_counter()
            selected = strategy_func(activities)
            exec_time = (time.perf_counter() - start_time) * 1000  # ms
            
            # ZBIERANIE VÝSLEDKOV
            results.append({
                'size': size,
                'strategy': strategy_name,
                'count': len(selected),
                'time': exec_time
            })
            print(f"  {strategy_name:8s}: {len(selected):3d} activities")
    return results
```

```python
def run_coin_change_experiments():
    """
    Experiment s coin change - greedy vs DP.
    
    EXPERIMENT DESIGN:
    - 9 testovacích prípadov s rôznymi množinami mincí
    - Meranie výkonu oboch algoritmov
    - Porovnanie optimality (či sú rovnaké alebo iné)
    - DÔKAZ, že greedy nie je vždy optimálny
    
    METRIKY:
    1. greedy_count: Počet mincí (greedy riešenie)
    2. dp_count: Počet mincí (DP riešenie)
    3. optimal: Či sú rovnaké (true = rovnaké, false = greedy je horší)
    4. difference: dp_count - greedy_count (negative = greedy je lepší?!)
    
    OČAKÁVANÉ VÝSLEDKY:
    - Príklady ako "6,10 sys" a "3,4 sys": dp < greedy
    - US/EU mince: dp == greedy (greedy je optimálny)
    """
    print("\n" + "="*80)
    print("COIN CHANGE PROBLEM")
    print("="*80)
    
    datasets = generate_coin_change_datasets()
    results = []
    
    for coins, amount, description in datasets:
        print(f"\n{description}: {coins}, sum={amount}")
        
        # GREEDY
        start_time = time.perf_counter()
        greedy_count, _ = coin_change_greedy(coins, amount)
        greedy_time = (time.perf_counter() - start_time) * 1000
        
        # DYNAMIC PROGRAMMING
        start_time = time.perf_counter()
        dp_count, _ = coin_change_dynamic_programming(coins, amount)
        dp_time = (time.perf_counter() - start_time) * 1000
        
        # POROVNANIE
        if greedy_count != -1 and dp_count != -1:
            optimal = greedy_count == dp_count
            difference = greedy_count - dp_count  # Kladné = greedy je horší
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
```

---

## 5. VIZUALIZÁCIA VÝSLEDKOV

```python
def plot_results(interval_results, coin_results):
    """
    Vytvára 6 grafov (2x3 grid) na analýzu výsledkov.
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    strategies = list(set(r['strategy'] for r in interval_results))
    sizes = sorted(set(r['size'] for r in interval_results))
    
    # GRAF 1: Kvalita - počet vybratých aktivít
    for i, (metric, ylabel, title) in enumerate([
        ('count', 'Selected Activities', 'Quality'),
        ('time', 'Time (ms)', 'Performance')
    ]):
        for strategy in strategies:
            # Vyberieme len dáta pre túto stratégiu, zoradiť podľa veľkosti
            data = sorted([r for r in interval_results if r['strategy'] == strategy], 
                         key=lambda x: x['size'])
            
            # Nakreslenie línie s markermi
            marker = 'o' if i == 0 else 's'  # Kruhy pre count, štvorce pre čas
            axes[0, i].plot(sizes, [r[metric] for r in data], 
                          marker=marker, label=strategy, linewidth=2)
        
        axes[0, i].set_xlabel('Dataset Size')
        axes[0, i].set_ylabel(ylabel)
        axes[0, i].set_title(f'Interval Scheduling: {title}')
        axes[0, i].legend()
        axes[0, i].grid(True, alpha=0.3)
    
    # GRAF 3: ako často každá stratégia dáva optimálne riešenie
    optimal_counts = [
        sum(1 for size in sizes 
            if max(r['count'] for r in interval_results if r['size'] == size) ==
            next(r['count'] for r in interval_results 
                 if r['size'] == size and r['strategy'] == strategy))
        for strategy in strategies
    ]
    
    axes[0, 2].bar(strategies, optimal_counts, 
                   color=['#2ca02c', '#ff7f0e', '#d62728', '#9467bd'])
    axes[0, 2].set_ylabel('Optimal Solutions')
    axes[0, 2].set_title('Interval Scheduling: Optimality Rate')
    axes[0, 2].set_ylim(0, len(sizes) + 0.5)
    
    for i, v in enumerate(optimal_counts):
        axes[0, 2].text(i, v + 0.1, f'{v}/{len(sizes)}', ha='center', fontweight='bold')
    
    # Vyberieme len valídne výsledky (kde greedy_count nie je None)
    valid = [r for r in coin_results if r['greedy_count'] is not None]
    x_pos = np.arange(len(valid))
    width = 0.35
    
    # GRAFY 4-5: Porovnanie greedy vs DP
    for i, (metric, ylabel, title) in enumerate([
        ('_count', 'Coins', 'Quality'),
        ('_time', 'Time (ms)', 'Performance')
    ]):
        # Greedy - ľavé stĺpce
        axes[1, i].bar(x_pos - width/2, [r[f'greedy{metric}'] for r in valid],
                      width, label='Greedy', color='#ff7f0e')
        # DP - pravé stĺpce
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
    
    axes[1, 2].axis('off')
    
    # Uloženie a zobrazenie
    plt.tight_layout()
    plt.savefig('HI_HOP/results.png', dpi=300, bbox_inches='tight')
    plt.close()
```

---

## 6. MAIN PROGRAM

```python
def main():
    """
    Hlavný program - spustenie všetkých experimentov.
    
    1. Spustenie interval scheduling experimentov
    2. Spustenie coin change experimentov
    3. Vizualizácia všetkých výsledkov do jedného obrázka
    """
    interval_results = run_interval_scheduling_experiments()
    coin_results = run_coin_change_experiments()
    
    plot_results(interval_results, coin_results)

if __name__ == "__main__":
    main()
```



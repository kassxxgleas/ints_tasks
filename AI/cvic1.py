import numpy as np

my_list = [x * 10 for x in range(1, 11)]
np.array(my_list)
np.array(my_list).shape
np.array(my_list).size
np.array(my_list).dtype

np.arange(10, 101, 10).reshape(5, 2).dtype

random_array = np.random.RandomState(2022).rand(3, 3) # or randomSeed
print(random_array)

print(random_array[:2])
print(random_array[:, 0])
print(random_array[2,2])

prices = np.array([5.99, 6.99, 22.49, 99.99, 4.99, 49.99])
total = prices+5
print(total)
discount_pct = random_array.flatten()[:6]
print(discount_pct)

pct_owed = (1 - discount_pct)
print(pct_owed)
owed = pct_owed * total


products = np.array(
    ["salad", "bread", "mustard", "rare tomato", "cola", "gourmet ice cream"]
)

res =  products[owed > 25]
print(res)

print(products[owed > 25])
    
fancy_feast_special = products[(owed > 25) | (products == "cola")]
shipping_cost = np.where(owed > 20, 0, 5)
print(fancy_feast_special)

pric = np.array([5.99, 6.99, 22.49, 99.99, 4.99, 49.99])

pric.sort()
print(pric[-3:])

print(pric[-3:].max())
print(pric[-3:].min())
print(pric[-3:].mean())
print(np.median(pric[-3:]))

price_tiers = np.array(["budget", "budget", "mid-tier", "luxury", "mid-tier", "luxury"])
price_tiers = np.unique(price_tiers)
print(len(price_tiers)) # pandas netebook and end this task
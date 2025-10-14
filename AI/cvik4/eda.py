import pandas as pd

data = pd.read_csv("AI/cvik4/breast-cancer.csv")

print(data.head())

print(data.info())

print(data.isnull().sum())
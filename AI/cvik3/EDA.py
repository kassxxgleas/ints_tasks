import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("AI/cvik3/Titanic-Dataset.csv")

print(df.head())

print(df.shape)

print(df.describe())

print(df.info())
# data = pd.read_csv("")
# data.head()
# data.info()
# data.isnull().sum()
# data['Цена'].fillna(data['Цена'].mean(), inplace=True)
# data.describe() // mode, mean, median, fillna
#
#
#
print(df.isnull().sum())

df.groupby('Sex')['Survived'].mean()
df.groupby('Pclass')['Survived'].mean()
df['Age'].fillna(1, inplace=True)
print(df.isnull().sum())

plt.hist(df['Age'].dropna(), bins=30)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

df[['Fare', 'Survived']].groupby('Survived').mean()
df.groupby('Embarked')['Survived'].mean()

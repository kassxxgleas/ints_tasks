import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("AI/cvik3/Titanic-Dataset.csv")
print(df.shape)
print(df.info())
print(df.describe())

df.isnull().sum()
df.groupby('Sex')['Survived'].mean()
df.groupby('Pclass')['Survived'].mean()


plt.hist(df['Age'].dropna(), bins=30)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

df[['Fare', 'Survived']].groupby('Survived').mean()
df.groupby('Embarked')['Survived'].mean()


sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
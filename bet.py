import pandas as pd
import numpy as np

df = pd.read_csv("bet.csv")

print(df.head())

print(df.columns)

df['Change %'] = df['Change %'].apply(lambda x: x.replace('%', ""))
print(df.head())
df['Change %'] = df['Change %'].astype(float).apply(lambda x: x*100)
print(df['Change %'].std())

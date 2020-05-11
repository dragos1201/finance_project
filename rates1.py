import pandas as pd

data = pd.read_excel('Excelrates1.xlsx')
print(data.head())
print(data['Change %'].mean())
print(data['Change %'].std())

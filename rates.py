import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('Excelrates.xlsx')
print(data.head())
data.drop('RON', axis=1, inplace=True)
data['Date'] = pd.to_datetime(data['Date'])
data.rename(columns={'HUF':'RON/HUF'}, inplace=True)
print(data.head())
data.set_index('Date', inplace=True)
print(data.head())
data.plot()
plt.show()

print(data['RON/HUF'].mean())
print(data['RON/HUF'].std())

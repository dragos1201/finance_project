import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# get adjusted closing prices of 5 selected companies with Quandl
quandl.ApiConfig.api_key = 'z_6yQyiBUp4gsAcxa5wJ'
selected = ['CNP', 'F', 'WMT', 'GE', 'TSLA']
data = quandl.get_table('WIKI/PRICES', ticker = selected,
                        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                        date = { 'gte': '2017-1-1', 'lte': '2018-12-31' }, paginate=True)


clean = data.set_index('date')
table = clean.pivot(columns='ticker')


returns_daily = table.pct_change()
returns_annual = returns_daily.mean() * 250


cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250


port_returns = []
port_volatility = []
sharpe_ratio = []
stock_weights = []


num_assets = len(selected)
num_portfolios = 50000


np.random.seed(101)

for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

for counter,symbol in enumerate(selected):
    portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]


df = pd.DataFrame(portfolio)

column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected]

df = df[column_order]

plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
axes = plt.gca()
axes.set_xlim([0, 0.5])
axes.set_ylim([-0.5, 0.35])
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()

min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()

sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]

plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
axes = plt.gca()
axes.set_xlim([0, 0.5])
axes.set_ylim([-0.5, 0.35])
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier (no impact)')
plt.show()


print(df.head())
new_table = df
new_table['Volatility'] = new_table['Volatility'].apply(lambda x: x+0.1)
new_table['Returns'] = new_table['Returns'].apply(lambda x: x+0.1)
print(new_table.head())

plt.style.use('seaborn-dark')
new_table.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
axes = plt.gca()
axes.set_xlim([0, 0.5])
axes.set_ylim([-0.5, 0.35])
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()

min_volatility = new_table['Volatility'].min()
max_sharpe = new_table['Sharpe Ratio'].max()

sharpe_portfolio = new_table.loc[new_table['Sharpe Ratio'] == max_sharpe]
min_variance_port = new_table.loc[new_table['Volatility'] == min_volatility]

plt.style.use('seaborn-dark')
new_table.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
axes = plt.gca()
axes.set_xlim([0, 0.5])
axes.set_ylim([-0.5, 0.35])
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier (Covid impact)')
plt.show()

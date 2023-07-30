
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
from util import get_data

def author():  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    :return: The GT username of the student  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: str  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    return "mmaya3"  # replace tb34 with your Georgia Tech username.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def gtid():  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    :return: The GT ID of the student  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: int  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    return 903743727  # replace with your GT ID number

def get_daily_rets(port_val):
    """
    calc daily returns
    port_val: daily porfolio values as series
    returns daily_rets: daily returns for sharpe ratio calculations!! (meaning all values except [0] which is 0)
    """
    daily_rets = (port_val / port_val.shift(1)) - 1
    daily_rets.iloc[0] = 0
    return daily_rets.iloc[1:]

def get_sharpe_ratio(daily_rets):
    """
    calc sharpe ratio
    daily_rets: daily porfolio returns as series
    returns adr, sddr, sr
    """
    sample_freq = 252 #daily
    sr = (daily_rets.mean()/daily_rets.std())* sqrt(sample_freq) #sharpe ratio
    return sr

def get_portvals_stats(portvals):
    # Get portfolio stats
    # !!!! portvals should be aseries, if dataframe, the return value will be a series
    daily_rets = get_daily_rets(portvals)
    cum_ret = (portvals.iloc[-1]/portvals.iloc[0])-1 #cumulative returns 
    avg_daily_ret = daily_rets.mean() #average daily returns  
    std_daily_ret = daily_rets.std() #standard daily return
    sharpe_ratio = get_sharpe_ratio(daily_rets) #sharpe ratio
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio

def trades2orders(df,symbol):
    # prepare an orders dataframe to apply marketsimcode function
    orders = df.copy()
    orders['Symbol'] = symbol
    orders['Order'] = 'BUY'
    orders.loc[orders.trades < 0,'Order'] = 'SELL'
    orders.loc[orders.trades == 0,'Order'] = 'HOLD'
    orders['Shares'] = abs(orders.trades)
    orders.drop('trades',axis=1, inplace=True)
    orders.index.name='Date'
    return orders

def compute_portvals(orders, start_val, commission, impact):  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    Computes the portfolio values.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    :param df: dataframe object from TheoreticallyOptimalStrategy.testPolicy 		  	   		  		 			  		 			 	 	 		 		 	
    :type dataframe: pandas dataframe  		  	   		  		 			  		 			 	 	 		 		 	
    :param start_val: The starting value of the portfolio  		  	   		  		 			  		 			 	 	 		 		 	
    :type start_val: int  		  	   		  		 			  		 			 	 	 		 		 	
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 			  		 			 	 	 		 		 	
    :type commission: float  		  	   		  		 			  		 			 	 	 		 		 	
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 			  		 			 	 	 		 		 	
    :type impact: float  		  	   		  		 			  		 			 	 	 		 		 	
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: pandas.DataFrame  		  	   		  		 			  		 			 	 	 		 		 	
    """
    orders.index.name='Date' #making sure the dtaframe index is name Date

    start_date = min(orders.index)
    end_date = max(orders.index)
    dates = pd.date_range(start_date,end_date)
    symbols = orders.Symbol.unique().tolist()

    prices = get_data(symbols, dates)
    prices.drop('SPY',axis=1, inplace=True)

    # get prices by order
    orders['price'] = [prices.loc[d,s.Symbol] for d,s in orders.iterrows()]
    # apply impact to prices
    orders.loc[orders.Order == 'BUY','price'] *= (1+impact)
    orders.loc[orders.Order == 'SELL','price'] *= (1-impact)
    # calc cash value by order and change the sign if BUY(-) or SELL(+)
    orders['cash'] = orders.Shares*orders.price
    orders.loc[orders.Order == 'BUY','cash'] *= -1
    # to calc the qty of shares by symbol and day
    orders['calc'] = orders['Shares']
    orders.loc[orders.Order == 'SELL','calc'] *= -1
    trades = pd.pivot_table(data=orders
                , values='calc'
                , index='Date'
                , columns='Symbol'
                , aggfunc='sum')
    trades = trades.fillna(0)
    cash_sum = pd.pivot_table(data=orders
                , values='cash'
                , index='Date'
                , aggfunc='sum')
    trades['cash'] = cash_sum['cash']

    # calc commisions
    comm = pd.pivot_table(data=orders
                , values='Order'
                , index='Date'
                , aggfunc='count')
    comm *= commission
    trades.loc[:,'cash'] -= comm.Order
    
    holdings = pd.DataFrame(0, index=prices.index, columns=prices.columns)
    holdings['cash']=0
    holdings.loc[trades.index,:] = trades.copy()
    holdings.iloc[0,-1] += start_val
    holdings = holdings.cumsum()
    
    # dollar value of each asset (prices * holdings), need to add cash col to prices
    prices['cash'] = 1
    value = prices * holdings
    port_val = value.sum(axis=1)
    port_val = port_val.to_frame()
    port_val.rename(columns={0:'port_val'}, inplace=True)
    port_val.index.name = 'Date'
    
    return port_val

def exp1(df_trades1, name_ref1,df_trades2,name_ref2,symbol,sv,commission,impact, title):
    df_orders1 = trades2orders(df_trades1,symbol)
    orders_pv1 = compute_portvals(df_orders1,sv,commission,impact)
    
    df_orders2 = trades2orders(df_trades2,symbol)
    orders_pv2 = compute_portvals(df_orders2,sv,commission,impact)

    temp = {"Symbol": [symbol, symbol],
        "Order": ["BUY", "SELL"],
        "Shares": [1000, 1000]}
    benchmark = pd.DataFrame(data=temp, index=[df_trades1.index[0], df_trades1.index[-1]])
    b_pv = compute_portvals(benchmark,sv,commission,impact)

    df_chart = pd.concat(  		  	   		  		 			  		 			 	 	 		 		 	
    [orders_pv1.iloc[:,0], orders_pv2.iloc[:,0], b_pv.iloc[:,0]], keys=[name_ref1, name_ref2, "Benchmark"], axis=1  		  	   		  		 			  		 			 	 	 		 		 	
    )
    #To normalize
    ax = (df_chart/df_chart.iloc[0])
    plt.figure()
    plt.plot(ax.index, ax[name_ref1], color='red')
    plt.plot(ax.index, ax[name_ref2], color='black')
    plt.plot(ax.index, ax['Benchmark'], color='purple')

    plt.xlabel('Date')
    plt.ylabel('Norm Value')
    plt.title(f"Daily Value Portfolio {title} [{symbol}] stock")
    plt.xticks(fontsize=8)
    plt.legend()
    plt.grid()
    plt.savefig(f'{title}.png')

    pass

def benchmark_comparison(df_trades,symbol,sv,commission,impact, name_ref = 'Reference'):
  
    df_orders = trades2orders(df_trades,symbol)
    orders_pv = compute_portvals(df_orders,sv,commission,impact)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portvals_stats(orders_pv.iloc[:,0])

    ''' Create benchmark
    Benchmark: The performance of a portfolio starting with $100,000 cash, 
    investing in 1000 shares of the symbol in use on the first trading day,  
    and holding that position. Include transaction costs. 
    '''
    temp = {"Symbol": [symbol, symbol],
        "Order": ["BUY", "SELL"],
        "Shares": [1000, 1000]}
    benchmark = pd.DataFrame(data=temp, index=[df_trades.index[0], df_trades.index[-1]])
    b_pv = compute_portvals(benchmark,sv,commission,impact)
    cum_ret_b, avg_daily_ret_b, std_daily_ret_b, sharpe_ratio_b = get_portvals_stats(b_pv.iloc[:,0])

    # Comparison chart
    df_chart = pd.concat(  		  	   		  		 			  		 			 	 	 		 		 	
    [orders_pv.iloc[:,0], b_pv.iloc[:,0]], keys=[name_ref, "Benchmark"], axis=1  		  	   		  		 			  		 			 	 	 		 		 	
    )
    #To normalize
    ax = (df_chart/df_chart.iloc[0])

    plt.figure()
    plt.plot(ax.index, ax[name_ref], color='red')
    plt.plot(ax.index, ax['Benchmark'], color='purple')

    #Add vertical lines
    #The vertical lines are short and long entry points, not buy and sell indicators.
    #when you enter a long position (+1000) or enter a short position (-1000), a line will be plotted.
    for i in range(len(df_orders[df_orders.Order=='BUY'].index)):
        plt.axvline(x=df_orders[df_orders.Order=='BUY'].index[i], color='blue',linewidth=.5)

    for i in range(len(df_orders[df_orders.Order=='SELL'].index)):
        plt.axvline(x=df_orders[df_orders.Order=='SELL'].index[i], color='black',linewidth=.5)

    plt.xlabel('Date')
    plt.ylabel('Norm Value')
    plt.title(f"Daily Value of {name_ref} VS Benchmark Portfolio [{symbol}]")
    plt.xticks(fontsize=8)
    plt.legend()
    plt.savefig(f'{name_ref}.png')
    # plt.show()

    # Comparation metrics
    print(f"{name_ref} VS benchmark for the tiker {symbol}")
    print(f"Date Range: {df_trades.index[0]} to {df_trades.index[-1]}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print(f"Sharpe Ratio of benchmark : {sharpe_ratio_b}")
    print()
    print(f"Cumulative Return of Fund: {cum_ret}")
    print(f"Cumulative Return of benchmark : {cum_ret_b}")
    print()
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print(f"Standard Deviation of benchmark : {std_daily_ret_b}")
    print()
    print(f"Average Daily Return of Fund: {avg_daily_ret}")
    print(f"Average Daily Return of benchmark : {avg_daily_ret_b}")
    print()
    print(f"Final Portfolio Value: {name_ref} {orders_pv.iloc[-1,0]} vs benchmark Value: {b_pv.iloc[-1,0]}")

    pass
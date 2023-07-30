
import pandas as pd
import numpy as np
import datetime as dt 
from util import get_data
import matplotlib.pyplot as plt

def author(): 
  return 'mmaya3' # replace tb34 with your Georgia Tech username. 

def bbp(df, symbol, period):
    sma = df[symbol].rolling(period).mean()
    rstd = df[symbol].rolling(period).std()
    lb = sma - 2*rstd
    ub = sma + 2*rstd
    df['BBP'] = (df[symbol] - lb)/(ub - lb)

def rsi(df, symbol, period):
    # Calculate the price changes
    prices_change = df[symbol].diff()

    # Separate the price changes into gains and losses
    gain = prices_change.apply(lambda x: x if x > 0 else 0)
    loss = prices_change.apply(lambda x: x if x < 0 else 0)

    # Calculate the sum gain and average loss (avg or sum is ok, rs it is an index)
    sum_gain = gain.rolling(window=period).sum()
    sum_loss = loss.rolling(window=period).sum()

    # Calculate the relative strength and RSI
    rs= sum_gain / abs(sum_loss)
    df['RSI'] = 100 - (100 / (1 + rs))
    #if avg_loss == 0 
    df['RSI'].loc[df['RSI'] == np.inf] = 100

def macd(df, symbol):
    #???? ewm: adjust=False (recursively)
    macd = df[symbol].ewm(span=12,adjust=False).mean() - df[symbol].ewm(span=26,adjust=False).mean()
    df["MACD"] = macd
    df["MACD_signal"] = macd.ewm(span=9).mean() 

##### indicators just for reference, these were not used in the project
def priceSMA_ratio(df, symbol, period):
    df['PSMA'] = df[symbol]/df[symbol].rolling(period).mean()

def roc(df, symbol, period):
    df['ROC'] = (df[symbol].diff(period) / df[symbol].shift(period)) * 100

def corr2SPY(df, symbol, period):
    start_date = min(df.index)
    end_date = max(df.index)
    dates = pd.date_range(start_date,end_date)
    df_t = get_data([symbol], dates)
    df['CORR2SPY'] = df_t[symbol].rolling(window=period).corr(df_t['SPY'])
#############

def stdz_col(df, col):
    mean = df[col].mean()
    std = df[col].std()
    df[f'{col}_std'] = (df[col] - mean) / std

def discret_ind_df(symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), verbose = False):
    #have to get past data (24 days) to calculate indicators with 14 days window
    dates = pd.date_range(sd- dt.timedelta(days=24),ed)
    df = get_data([symbol], dates)
    df.drop('SPY',axis=1, inplace=True)
    #indicators
    period = 14
    rsi(df,symbol,period)
    stdz_col(df, 'RSI')
    bbp(df,symbol,period)
    stdz_col(df, 'BBP')
    macd(df,symbol)
    #MACD creates columns MACD and MACD_signal, I need to combine them into MACDH
    df['MACDH'] = df['MACD'] - df['MACD_signal']
    stdz_col(df, 'MACDH')

    #discar dates not required
    df = df.loc[sd:ed]

    # ### DISCRETIZE INDICATORS: buy:1, hold:0, sell:-1 acording to levels
    buy_level= -1
    sell_level = 1
    df['RSI_d'] = 0
    df.loc[df.RSI_std < buy_level, 'RSI_d'] = 1
    df.loc[df.RSI_std > sell_level, 'RSI_d'] = -1
    df['BBP_d'] = 0
    df.loc[df.BBP_std < buy_level, 'BBP_d'] = 1
    df.loc[df.BBP_std > sell_level, 'BBP_d'] = -1
    df['MACDH_d'] = 0
    df.loc[df.MACDH_std < buy_level, 'MACDH_d'] = 1
    df.loc[df.MACDH_std > sell_level, 'MACDH_d'] = -1

    if verbose == True:
        # df.to_csv('discret_ind_df.csv')
        stdz_col(df, symbol) #standardize the price
        plt.figure
        plt.plot(df.index, df['JPM_std'], color='red')
        plt.plot(df.index, df['MACDH_std'], color='purple',linewidth=.5)
        plt.plot(df.index, df['RSI_std'], color='orange',linewidth=.5)
        plt.plot(df.index, df['BBP_std'], color='green',linewidth=.5)

        plt.axhline(1, linestyle = '--', linewidth = 1, color = 'black')
        plt.axhline(-1, linestyle = '--', linewidth = 1, color = 'black')

        plt.grid(True)
        plt.legend()
        plt.xticks(fontsize=8)
        plt.title('Standardized values of the JPM stock price and technical indicators')
        plt.savefig('Figure1.png')
    
    df = df[[symbol,'RSI_d','BBP_d','MACDH_d']]
    df.columns=[symbol,'RSI','BBP','MACDH']

    return df

if __name__ == "__main__":  		  	   		  		 			  		 			 	 	 		 		 	
    #remember to run < PYTHONPATH=../:. python indicators.py > to get util code
    print("Just teating")
    discret_ind_df(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31),verbose=True)
    
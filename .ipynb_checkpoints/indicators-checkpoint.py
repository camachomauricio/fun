
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


def bbp(df, col_price, period=14):
    sma = df[col_price].rolling(period).mean()
    rstd = df[col_price].rolling(period).std()
    lb = sma - 2*rstd
    ub = sma + 2*rstd
    df['BBP'] = (df[col_price] - lb)/(ub - lb)

def rsi(df, col_price, period=14):
    # Calculate the price changes
    prices_change = df.loc[:,col_price].diff()

    # Separate the price changes into gains and losses
    gain = prices_change.apply(lambda x: x if x > 0 else 0)
    loss = prices_change.apply(lambda x: x if x < 0 else 0)

    # Calculate the sum gain and average loss (avg or sum is ok, rs it is an index)
    sum_gain = gain.rolling(window=period).sum()
    sum_loss = loss.rolling(window=period).sum()

    # Calculate the relative strength and RSI
    rs= sum_gain / abs(sum_loss)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df.loc[df['RSI'] == np.inf,'RSI'] = 100

def macd(df, col_price, short_period=12, long_period=26):
    #???? ewm: adjust=False (recursively)
    macd = df[col_price].ewm(span=short_period,adjust=False).mean() - df[col_price].ewm(span=long_period,adjust=False).mean()
    df["MACD"] = macd
    df["MACD_signal"] = macd.ewm(span=9).mean()

def chaikin(df, short_period=3, long_period=10):
    #Acumulation-distribution line
    df['ADL'] = ((2 * df['Close'] - df['Low'] - df['High']) / (df['High'] - df['Low'])) * df['Volume']
    df['CO'] = df['ADL'].ewm(span=short_period, min_periods=1, adjust=False).mean() - df['ADL'].ewm(span=long_period, min_periods=1, adjust=False).mean()

##### indicators just for reference, these were not used in the project
def priceSMA_ratio(df, col_price, period):
    df['PSMA'] = df[col_price]/df[col_price].rolling(period).mean()

def roc(df, col_price, period):
    df['ROC'] = (df[col_price].diff(period) / df[col_price].shift(period)) * 100

def corr2SPY(df, col_price, period):
    start_date = min(df.index)
    end_date = max(df.index)
    dates = pd.date_range(start_date,end_date)
    df_t = get_data([col_price], dates)
    df['CORR2SPY'] = df_t[col_price].rolling(window=period).corr(df_t['SPY'])
#############

def stdz_col(df, col):
    mean = df[col].mean()
    std = df[col].std()
    df[f'{col}_std'] = (df[col] - mean) / std


if __name__ == "__main__":  		  	   		  		 			  		 			 	 	 		 		 	
    #remember to run < PYTHONPATH=../:. python indicators.py > to get util code
    print("Just teating")
    
# Similar to TheoricallyOptionalStrategy but based on indicators
'''
Code implementing a ManualStrategy object (your Manual Strategy) 
in the strategy_evaluation/ directory. It should implement testPolicy() 
which returns a trades data frame (see below). The main part of this code 
should call marketsimcode as necessary to generate the plots used in the report. 
NOTE: You will have to create this file yourself. 
'''

import datetime as dt
import pandas as pd
import indicators as ind
import marketsimcode as msim

def author(): 
  return 'mmaya3' # replace tb34 with your Georgia Tech username. 

class ManualStrategy:
  def __init__(self, verbose=False, impact=0.0, commission=0.0):
      self.verbose = verbose
      self.impact = impact
      self.commission = commission

  def testPolicy(self,
                   symbol='IBM',
                   sd=dt.datetime(2008, 1, 1, 0, 0),
                   ed=dt.datetime(2009, 1, 1, 0, 0),
                   sv=100000):

    df = ind.discret_ind_df(symbol,sd,ed, verbose= False)
    dates = df.index

    # to create a consensus between indicators
    # 0:short, 1:hold, 2:long
    df['signal'] = 1
    df.loc[(df.RSI+df.BBP+df.MACDH >= 2),'signal'] = 2
    df.loc[(df.RSI+df.BBP+df.MACDH <= -2),'signal'] = 0

    #build list of orders
    df['trades']=0
    dates = df.index
    
    curr_position = 0

    for i in range(len(dates)):
      today = dates[i]
      a = df.loc[today,'signal']
      # 0:short, 1:hold, 2:long
      if a== 0:
          trade = -1000 - curr_position
      elif a == 1:
          trade = 0
      else:
          trade = 1000 - curr_position
      
      curr_position = curr_position + trade

      df.loc[today,'trades'] = trade

      if self.verbose:
        actions={0:'short', 1:'hold', 2:'long'}
        print(f'day:{today}, action:{a}:{actions[a]}, trade:{trade} curr_position{curr_position}')
        pass

    return df.trades.to_frame()

def main():
  '''
  The in-sample period is January 1, 2008 to December 31, 2009. 
  The out-of-sample/testing period is January 1, 2010 to December 31, 2011. 
  Starting cash is $100,000.
  ManualStrategy and StrategyLearner: Commission: $9.95, Impact: 0.005 
  (unless stated otherwise in an experiment). 
  '''
  ### IN-SMAPLE
  symbol = 'JPM'
  sd = dt.datetime(2008, 1, 1)
  ed = dt.datetime(2009,12,31)
  sv=100000
  commission = 9.95
  impact = 0.005

  ms = ManualStrategy(verbose=False, impact=impact, commission=commission)
  df_trades = ms.testPolicy(symbol, sd, ed,sv)
  msim.benchmark_comparison(df_trades,symbol,sv,commission,impact,name_ref='IN-SAMPLE-MS')

  ### OUT-OFF-SAMPLE
  symbol = 'JPM'
  sd = dt.datetime(2010, 1, 1)
  ed = dt.datetime(2011,12,31)
  sv=100000
  commission = 9.95
  impact = 0.005

  ms = ManualStrategy(verbose=False, impact=impact, commission=commission)
  df_trades = ms.testPolicy(symbol, sd, ed,sv)
  msim.benchmark_comparison(df_trades,symbol,sv,commission,impact, name_ref = 'OUT-OF-SAMPLE-MS')


if __name__ == "__main__":
  #remember to run < PYTHONPATH=../:. python ManualStrategy.py > to get util code
  print('Just testing')
  main()


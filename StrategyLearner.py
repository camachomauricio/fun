""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			 	 	 		 		 	
Atlanta, Georgia 30332  		  	   		  		 			  		 			 	 	 		 		 	
All Rights Reserved  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Template code for CS 4646/7646  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			 	 	 		 		 	
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			 	 	 		 		 	
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			 	 	 		 		 	
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			 	 	 		 		 	
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			 	 	 		 		 	
or edited.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			 	 	 		 		 	
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			 	 	 		 		 	
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			 	 	 		 		 	
GT honor code violation.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
-----do not edit anything above this line---  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Student Name: Mauricio Camacho (replace with your name)  		  	   		  		 			  		 			 	 	 		 		 	
GT User ID: mmaya3 (replace with your User ID)  		  	   		  		 			  		 			 	 	 		 		 	
GT ID: 903743727 (replace with your GT ID)  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
import datetime as dt
import pandas as pd  		  	   		  		 			  		 			 	 	 		 		 	
import QLearner as ql
import indicators as ind
import marketsimcode as msim

def author(): 
  return 'mmaya3' # replace tb34 with your Georgia Tech username.   		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
class StrategyLearner(object):  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			 	 	 		 		 	
        If verbose = False your code should not generate ANY output.  		  	   		  		 			  		 			 	 	 		 		 	
    :type verbose: bool  		  	   		  		 			  		 			 	 	 		 		 	
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 			  		 			 	 	 		 		 	
    :type impact: float  		  	   		  		 			  		 			 	 	 		 		 	
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 			  		 			 	 	 		 		 	
    :type commission: float  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    # constructor  		  	   		  		 			  		 			 	 	 		 		 	
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        Constructor method  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        self.verbose = verbose  		  	   		  		 			  		 			 	 	 		 		 	
        self.impact = impact  		  	   		  		 			  		 			 	 	 		 		 	
        self.commission = commission

        #num_actions = 3 => 0:short, 1:hold, 2:long
        #num_states =3^4 = 81 (4 groups with 3 options each)
        # - position:-1000, 0, 1000
        # - indicators: RSI, BBP, MACDH each with -1:SELL, 0:HOLD, 1:BUY
        self.learner = ql.QLearner(num_states=81,
            num_actions = 3,
            alpha = 0.2,
            gamma = 0.9,
            rar = 0.9,
            radr = 0.99,
            dyna = 0,
            verbose=False)
    
        self.states = self.create_all_states()
    #create all posible states
    def create_all_states(self):
        groups = [
            [-1000, 0, 1000],
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ]
        combinations = []
        # Nested loops to generate combinations
        for a in groups[0]:
            for b in groups[1]:
                for c in groups[2]:
                    for d in groups[3]:
                        combinations.append([a, b, c, d])
        columns = ['P', 'RSI', 'BBP', 'MACDH']
        all_states_df = pd.DataFrame(combinations, columns=columns)

        return all_states_df
    
    def handle_order(self,curr_position,curr_cash,action,price):
        #num_actions = 3 => 0:short, 1:hold, 2:long
        if action == 0:
            trade = -1000 - curr_position
        elif action == 1:
            trade = 0
        else:
            trade = 1000 - curr_position

        curr_position = curr_position + trade
        cost = price * trade
        imp_cost = self.impact * price * abs(trade)
        curr_cash = curr_cash - cost - imp_cost - self.commission
        
        return curr_position, trade, curr_cash
  		  	   		  		 			  		 			 	 	 		 		 	
    # this method should create a QLearner, and train it for trading  		  	   		  		 			  		 			 	 	 		 		 	
    def add_evidence(  		  	   		  		 			  		 			 	 	 		 		 	
        self,  		  	   		  		 			  		 			 	 	 		 		 	
        symbol="IBM",  		  	   		  		 			  		 			 	 	 		 		 	
        sd=dt.datetime(2008, 1, 1),  		  	   		  		 			  		 			 	 	 		 		 	
        ed=dt.datetime(2009, 1, 1),  		  	   		  		 			  		 			 	 	 		 		 	
        sv=10000,  		  	   		  		 			  		 			 	 	 		 		 	
    ):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        Trains your strategy learner over a given time frame.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
        :param symbol: The stock symbol to train on  		  	   		  		 			  		 			 	 	 		 		 	
        :type symbol: str  		  	   		  		 			  		 			 	 	 		 		 	
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			 	 	 		 		 	
        :type sd: datetime  		  	   		  		 			  		 			 	 	 		 		 	
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			 	 	 		 		 	
        :type ed: datetime  		  	   		  		 			  		 			 	 	 		 		 	
        :param sv: The starting value of the portfolio  		  	   		  		 			  		 			 	 	 		 		 	
        :type sv: int  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	  		  	   		  		 			  		 			 	 	 		 		 	
        # add your code to do learning here
        ######### MY CODE
  		#Create princesdataframe with discretize indicators
        df_prices = ind.discret_ind_df(symbol,sd,ed, verbose= False)
        df_prices['trades']=0
        dates = df_prices.index

        # set initial values and all posible states to query later
        states = self.states
        
        if self.verbose:
            print(df_prices.head())
            print(states.head())
            pass
        
        ####loop While not converged (pd.corr() used)
        converge = 0.0
        count = 0
        while (count < 30) & (converge < 0.99) :
            curr_position = 0
            curr_cash = sv
            prev_position = 0
            prev_cash = sv

            s = states.loc[(states.P==curr_position)&
                                    (states.RSI==df_prices.loc[dates[0],'RSI'])&
                                    (states.BBP==df_prices.loc[dates[0],'BBP'])&
                                    (states.MACDH==df_prices.loc[dates[0],'MACDH'])].index[0]
            
            a = self.learner.querysetstate(s)
            curr_position, trade, curr_cash = self.handle_order(curr_position,
                                                                curr_cash,
                                                                a,
                                                                df_prices.loc[dates[0],symbol])
            df_prices.loc[dates[0],'trades'] = trade

            for i in range(1,len(dates)):
                today = dates[i]
                yesterday = dates[i - 1]

                s_prime = states.loc[(states.P==curr_position)&
                                    (states.RSI==df_prices.loc[today,'RSI'])&
                                    (states.BBP==df_prices.loc[today,'BBP'])&
                                    (states.MACDH==df_prices.loc[today,'MACDH'])].index[0]
                
                today_equity = curr_position * df_prices.loc[today,symbol] + curr_cash
                yest_equity = prev_position * df_prices.loc[yesterday, symbol] + prev_cash
                r = (today_equity - yest_equity)/today_equity
                
                prev_position = curr_position
                prev_cash = curr_cash
                
                a = self.learner.query(s_prime, r)
                curr_position, trade, curr_cash = self.handle_order(curr_position,
                                                                    curr_cash,
                                                                    a,
                                                                    df_prices.loc[today,symbol])
                df_prices.loc[today,'trades'] = trade
                
            if count>0:
                converge = old_trades.corr(df_prices.trades)

            old_trades = df_prices.trades.copy()
            count+=1
            
            
            if self.verbose:
                print(f'**** ----- {count}th run:')
                print(converge)
                # print(self.learner.q)
                pass

        ######### END OF MY CODE
        # # example usage of the old backward compatible util function  		  	   		  		 			  		 			 	 	 		 		 	
        # syms = [symbol]  		  	   		  		 			  		 			 	 	 		 		 	
        # dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			 	 	 		 		 	
        # prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		  	   		  		 			  		 			 	 	 		 		 	
        # prices = prices_all[syms]  # only portfolio symbols  		  	   		  		 			  		 			 	 	 		 		 	
        # prices_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  		 			  		 			 	 	 		 		 	
        # if self.verbose:  		  	   		  		 			  		 			 	 	 		 		 	
        #     print(prices)  		  	   		  		 			  		 			 	 	 		 		 	

        # # example use with new colname  		  	   		  		 			  		 			 	 	 		 		 	
        # volume_all = ut.get_data(  		  	   		  		 			  		 			 	 	 		 		 	
        #     syms, dates, colname="Volume"  		  	   		  		 			  		 			 	 	 		 		 	
        # )  # automatically adds SPY  		  	   		  		 			  		 			 	 	 		 		 	
        # volume = volume_all[syms]  # only portfolio symbols  		  	   		  		 			  		 			 	 	 		 		 	
        # volume_SPY = volume_all["SPY"]  # only SPY, for comparison later  		  	   		  		 			  		 			 	 	 		 		 	
        # if self.verbose:  		  	   		  		 			  		 			 	 	 		 		 	
        #     print(volume)  		  	   		  		 			  		 			 	 	 		 		 	

    # this method should use the existing policy and test it against new data  		  	   		  		 			  		 			 	 	 		 		 	
    def testPolicy(  		  	   		  		 			  		 			 	 	 		 		 	
        self,  		  	   		  		 			  		 			 	 	 		 		 	
        symbol="IBM",  		  	   		  		 			  		 			 	 	 		 		 	
        sd=dt.datetime(2009, 1, 1),  		  	   		  		 			  		 			 	 	 		 		 	
        ed=dt.datetime(2010, 1, 1),  		  	   		  		 			  		 			 	 	 		 		 	
        sv=10000,  		  	   		  		 			  		 			 	 	 		 		 	
    ):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        Tests your learner using data outside of the training data  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
        :param symbol: The stock symbol that you trained on on  		  	   		  		 			  		 			 	 	 		 		 	
        :type symbol: str  		  	   		  		 			  		 			 	 	 		 		 	
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			 	 	 		 		 	
        :type sd: datetime  		  	   		  		 			  		 			 	 	 		 		 	
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			 	 	 		 		 	
        :type ed: datetime  		  	   		  		 			  		 			 	 	 		 		 	
        :param sv: The starting value of the portfolio  		  	   		  		 			  		 			 	 	 		 		 	
        :type sv: int  		  	   		  		 			  		 			 	 	 		 		 	
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		  		 			  		 			 	 	 		 		 	
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		  		 			  		 			 	 	 		 		 	
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		  		 			  		 			 	 	 		 		 	
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		  		 			  		 			 	 	 		 		 	
        :rtype: pandas.DataFrame  		  	   		  		 			  		 			 	 	 		 		 	
        """
        ##### MY CODE
  		#Create princesdataframe with discretize indicators
        df_prices = ind.discret_ind_df(symbol,sd,ed, verbose= False)
        df_prices['trades']=0
        dates = df_prices.index
        states = self.states

        curr_position = 0

        for i in range(len(dates)):
            today = dates[i]
            
            s = states.loc[(states.P==curr_position)&
                                    (states.RSI==df_prices.loc[today,'RSI'])&
                                    (states.BBP==df_prices.loc[today,'BBP'])&
                                    (states.MACDH==df_prices.loc[today,'MACDH'])].index[0]
            a = self.learner.querysetstate(s)
            
            #num_actions = 3 => 0:short, 1:hold, 2:long
            #same part from the handleorder function
            if a == 0:
                trade = -1000 - curr_position
            elif a == 1:
                trade = 0
            else:
                trade = 1000 - curr_position
            
            curr_position = curr_position + trade

            df_prices.loc[today,'trades'] = trade
        
            if self.verbose:
                actions={0:'short', 1:'hold', 2:'long'}
                print(f'state:{s}, action:{a}:{actions[a]}, trade:{trade} curr_position{curr_position}')
                pass

        return df_prices.trades.to_frame()
        ######### END OF MY CODE
        # # here we build a fake set of trades  		  	   		  		 			  		 			 	 	 		 		 	
        # # your code should return the same sort of data  		  	   		  		 			  		 			 	 	 		 		 	
        # dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			 	 	 		 		 	
        # prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		  	   		  		 			  		 			 	 	 		 		 	
        # trades = prices_all[[symbol,]]  # only portfolio symbols  		  	   		  		 			  		 			 	 	 		 		 	
        # trades_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  		 			  		 			 	 	 		 		 	
        # trades.values[:, :] = 0  # set them all to nothing  		  	   		  		 			  		 			 	 	 		 		 	
        # trades.values[0, :] = 1000  # add a BUY at the start  		  	   		  		 			  		 			 	 	 		 		 	
        # trades.values[40, :] = -1000  # add a SELL  		  	   		  		 			  		 			 	 	 		 		 	
        # trades.values[41, :] = 1000  # add a BUY  		  	   		  		 			  		 			 	 	 		 		 	
        # trades.values[60, :] = -2000  # go short from long  		  	   		  		 			  		 			 	 	 		 		 	
        # trades.values[61, :] = 2000  # go long from short  		  	   		  		 			  		 			 	 	 		 		 	
        # trades.values[-1, :] = -1000  # exit on the last day  		  	   		  		 			  		 			 	 	 		 		 	
        # if self.verbose:  		  	   		  		 			  		 			 	 	 		 		 	
        #     print(type(trades))  # it better be a DataFrame!  		  	   		  		 			  		 			 	 	 		 		 	
        # if self.verbose:  		  	   		  		 			  		 			 	 	 		 		 	
        #     print(trades)  		  	   		  		 			  		 			 	 	 		 		 	
        # if self.verbose:  		  	   		  		 			  		 			 	 	 		 		 	
        #     print(prices_all)  		  	   		  		 			  		 			 	 	 		 		 	
        # return trades  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def main():
    ### IN-SMAPLE
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009,12,31)
    sv=100000
    commission = 9.95
    impact = 0.005

    learner = StrategyLearner(verbose = False, impact = impact, commission=commission)
    learner.add_evidence(symbol,sd,ed,sv)
    df_trades = learner.testPolicy(symbol,sd,ed,sv)
    msim.benchmark_comparison(df_trades,symbol,sv,commission,impact, name_ref = 'IN-SAMPLE-SL')

    ### OUT-OFF-SAMPLE
    symbol = 'JPM'
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011,12,31)
    sv=100000
    commission = 9.95
    impact = 0.005

    df_trades = learner.testPolicy(symbol,sd,ed,sv)
    msim.benchmark_comparison(df_trades,symbol,sv,commission,impact, name_ref = 'OUT-OF-SAMPLE-SL')  


if __name__ == "__main__":  		  	   		  		 			  		 			 	 	 		 		 	
    #remember to run < PYTHONPATH=../:. python StrategyLearner.py > to get util code
    print("One does not simply think up a strategy")
    main()
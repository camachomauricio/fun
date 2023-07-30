""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
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
  		  	   		  		 			  		 			 	 	 		 		 	
import random as rand  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
import numpy as np  		  	   		  		 			  		 			 	 	 		 		 	


class QLearner(object):  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    This is a Q learner object.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    :param num_states: The number of states to consider.  		  	   		  		 			  		 			 	 	 		 		 	
    :type num_states: int  		  	   		  		 			  		 			 	 	 		 		 	
    :param num_actions: The number of actions available..  		  	   		  		 			  		 			 	 	 		 		 	
    :type num_actions: int  		  	   		  		 			  		 			 	 	 		 		 	
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		  		 			  		 			 	 	 		 		 	
    :type alpha: float  		  	   		  		 			  		 			 	 	 		 		 	
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		  		 			  		 			 	 	 		 		 	
    :type gamma: float  		  	   		  		 			  		 			 	 	 		 		 	
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		  		 			  		 			 	 	 		 		 	
    :type rar: float  		  	   		  		 			  		 			 	 	 		 		 	
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		  		 			  		 			 	 	 		 		 	
    :type radr: float  		  	   		  		 			  		 			 	 	 		 		 	
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		  		 			  		 			 	 	 		 		 	
    :type dyna: int  		  	   		  		 			  		 			 	 	 		 		 	
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			 	 	 		 		 	
    :type verbose: bool  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    def __init__(  		  	   		  		 			  		 			 	 	 		 		 	
        self,  		  	   		  		 			  		 			 	 	 		 		 	
        num_states=100,  		  	   		  		 			  		 			 	 	 		 		 	
        num_actions=4,  		  	   		  		 			  		 			 	 	 		 		 	
        alpha=0.2,  		  	   		  		 			  		 			 	 	 		 		 	
        gamma=0.9,  		  	   		  		 			  		 			 	 	 		 		 	
        rar=0.5,  		  	   		  		 			  		 			 	 	 		 		 	
        radr=0.99,  		  	   		  		 			  		 			 	 	 		 		 	
        dyna=0,  		  	   		  		 			  		 			 	 	 		 		 	
        verbose=False):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        Constructor method  		  	   		  		 			  		 			 	 	 		 		 	
        """
        ####MY CODE
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose

        #curent stare and action
        self.s = 0
        self.a = 0

        #q table
        self.q = np.zeros((num_states, num_actions))

        #Transition dictionary T{s,a,r,s' : count} for Dyna
        self.T = {}
        

    def querysetstate(self, s):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        Update the state without updating the Q-table  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
        :param s: The new state  		  	   		  		 			  		 			 	 	 		 		 	
        :type s: int  		  	   		  		 			  		 			 	 	 		 		 	
        :return: The selected action  		  	   		  		 			  		 			 	 	 		 		 	
        :rtype: int  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        self.s = s
        # action = rand.randint(0, self.num_actions - 1) => just pick a random action
        
        ####### MY CODE
        # get an action considering rar, explotation vs exploration
        if rand.random() < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q[s])
        
        self.a = action
        ########
        
        # if self.verbose:  		  	   		  		 			  		 			 	 	 		 		 	
        #     print(f"s = {s}, a = {action}")  		  	   		  		 			  		 			 	 	 		 		 	
        
        return action
  		  	   		  		 			  		 			 	 	 		 		 	
    def query(self, s_prime, r):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        Update the Q table and return an action  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
        :param s_prime: The new state  		  	   		  		 			  		 			 	 	 		 		 	
        :type s_prime: int  		  	   		  		 			  		 			 	 	 		 		 	
        :param r: The immediate reward  		  	   		  		 			  		 			 	 	 		 		 	
        :type r: float  		  	   		  		 			  		 			 	 	 		 		 	
        :return: The selected action  		  	   		  		 			  		 			 	 	 		 		 	
        :rtype: int  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        # action = rand.randint(0, self.num_actions - 1) => just to pick a random action

        #####MY CODE
        # to assemble the equation to calculate the new value of Q in status S (not S' !!!)
        q_old = self.q[self.s][self.a]
        
        # for improved estimate if future q values
        a_best = np.argmax(self.q[s_prime])
        q_best = self.q[s_prime][a_best]
        
        # Formula for Q'[S,A]
        q_new = (1 - self.alpha) * q_old + self.alpha * (r + self.gamma * q_best)
        self.q[self.s][self.a] = q_new
        
        #choose new action now with s_prime, same code as querysetstate
        if rand.random() < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q[s_prime])

        # Update random rar according to rdar
        self.rar = self.rar * self.radr
    
        ##### DYNA
        if self.dyna > 0:
            # #OP1 update model or trancision dict T{s,a:s',r} only if a better r
            # s_a = (self.s,self.a)
            # if s_a not in self.T:
            #     self.T[s_a] = (s_prime,r)
            # elif self.T[s_a][1] <= r:
            #     self.T[s_a] = (s_prime,r)

            # #Dyna loop
            # for _ in range(self.dyna):
            #     ds, da = rand.choice(list(self.T))
            #     ds_prime, dr = self.T[(ds,da)]
            #     #Update Q with Dyna variables , same code/equation than before
            #     q_old = self.q[ds][da]
            #     a_best = np.argmax(self.q[ds_prime])
            #     q_best = self.q[ds_prime][a_best]
            #     q_new = (1 - self.alpha) * q_old + self.alpha * (dr + self.gamma * q_best)
            #     self.q[ds][da] = q_new
            
            #OP2  update model or trancision dict T{s,a,r,s' : count} and keep only the most common ones
            exp_tup = (self.s,self.a,r,s_prime)
            if exp_tup not in self.T:
                self.T[exp_tup] = 1
            else:
                self.T[exp_tup] += 1

            #To make T2 = {s,a:r,s'} for only the biggest count.
            T2={}
            for t,v in self.T.items():
                s_a = (t[0],t[1])
                r_sp_c = (t[2],t[3],v)
                if s_a not in T2:
                    T2[s_a] = r_sp_c
                elif v > T2[s_a][2]:
                        T2[s_a] = r_sp_c
            
            #Dyna loop
            for _ in range(self.dyna):
                ds, da = rand.choice(list(T2))
                dr, ds_prime, _ = T2[(ds,da)]
                #Update Q with Dyna variables , same code/equation than before
                q_old = self.q[ds][da]
                a_best = np.argmax(self.q[ds_prime])
                q_best = self.q[ds_prime][a_best]
                q_new = (1 - self.alpha) * q_old + self.alpha * (dr + self.gamma * q_best)
                self.q[ds][da] = q_new     

        ##### END DYNA

        self.a = action
        self.s = s_prime

        ######   		  	   		  		 			  		 			 	 	 		 		 	
        # if self.verbose:  		  	   		  		 			  		 			 	 	 		 		 	
        #     print(f"s = {s_prime}, a = {action}, r={r}")  		  	   		  		 			  		 			 	 	 		 		 	
        return action  		  	   		  		 			  		 			 	 	 		 		 	
        
    def author(self):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        :return: The GT username of the student  		  	   		  		 			  		 			 	 	 		 		 	
        :rtype: str  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        return "mmaya3"  # replace tb34 with your Georgia Tech username.  		  	   		  		 			  		 			 	 	 		 		 	

    def gtid(self):  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        :return: The GT ID of the student  		  	   		  		 			  		 			 	 	 		 		 	
        :rtype: int  		  	   		  		 			  		 			 	 	 		 		 	
        """  		  	   		  		 			  		 			 	 	 		 		 	
        return 903743727  # replace with your GT ID number

  		  	   		  		 			  		 			 	 	 		 		 	
if __name__ == "__main__":  		  	   		  		 			  		 			 	 	 		 		 	
    print("Remember Q from Star Trek? Well, this isn't him")
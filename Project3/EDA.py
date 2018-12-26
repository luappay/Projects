# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 15:28:07 2018

@author: Paul Yap
"""

import numpy as np
import pandas as pd
import patsy

from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression, RidgeCV, LassoCV, ElasticNetCV
from sklearn.model_selection import cross_val_score, KFold

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')


import Views as Vs

## %config InlineBackend.figure_format = 'retina'
## %matplotlib inline


class go_cray_EDA():
    
    def __init__(self, df, hist_pref=None):
        
        self.df = df
        self.hist_pref = hist_pref 
        
    def initiate(self):
        """
            Initiates the EDA aid program
            Runs on a while loop whereby it lists down the possible options to run EDA on the data df
            Depending on the options, different Methods are executed
            Once an option is selected, the program will run the method, and return to the menu page
            The while loop breaks out when you selected the end option
        """
        
        while True: 
            Vs.EDA_options_msg()
            try: 
                choice = int(input("What would you like to do?: "))
            except:
                choice = None
            
            if choice == 1: 
                self.df_shape()
                
            elif choice == 2: 
                Vs.print_nice_column_names(self.df)
                
            elif choice == 0:
                print ('Go Cray! Bye!!')
                break
            
            else:
                print ("""There's no such option, try again:)""")
            
    
    def EDA_options_msg(self):
        """
            Option messages for the menu page 
        """
        
        print ( "EDA Options: ")
        print ( " (1)  Shape of data ")  
        print ( " (2)  Colum names")
        print ( " (0)  I'm done with EDA")
        
    def df_shape(self):
        """
            Prints the shape information and prints the number of rows and columns 
        """
        print ( self.df.shape )
        print ('There are {} rows.'.format(self.df.shape[0]))
        print ('There are {} columns.'.format(self.df.shape[1]))
        
    def print_nice_column_names(self):
        """
            Prints column names in neat order
        """
        index = [i for i in range(len(self.df.columns)) if (i % 3) == 0]
        columns = self.df.columns
        for i in index:
            try: 
                print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= columns[i+1], col3= columns[i+2], i1 = i, i2 = i+1, i3 = i+2, fill='', align='<', num_width=2, col_width=15))
            except:
                try:
                    print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= columns[i+1], col3= '', i1 = i, i2 = i+1, i3 = '##', fill='', align='<', num_width=2, col_width=15))
                except:
                    print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= '', col3= '', i1 = i, i2 = '##', i3 = '##', fill='', align='<', num_width=2, col_width=15))
                           
                           
                           
house = pd.read_csv('./housing.csv')

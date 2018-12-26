# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 13:02:57 2018

@author: Paul Yap
"""

import numpy as np
import pandas as pd

from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression, RidgeCV, LassoCV, ElasticNetCV
from sklearn.model_selection import cross_val_score, KFold

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')


def EDA_options_msg():
        """
            Option messages for the menu page 
        """
        
        print ( "EDA Options: ")
        print ( " (1)  Shape of data ")  
        print ( " (2)  Colum names")
        print ( " (0)  I'm done with EDA")
        
def df_shape(df):
        """
            Prints the shape information and prints the number of rows and columns 
        """
        print ( df.shape )
        print ('There are {} rows.'.format(df.shape[0]))
        print ('There are {} columns.'.format(df.shape[1]))
        
def print_nice_column_names(df):
        """
            Prints column names in neat order
        """
        index = [i for i in range(len(df.columns)) if (i % 3) == 0]
        columns = df.columns
        for i in index:
            try: 
                print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= columns[i+1], col3= columns[i+2], i1 = i, i2 = i+1, i3 = i+2, fill='', align='<', num_width=2, col_width=15))
            except:
                try:
                    print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= columns[i+1], col3= '', i1 = i, i2 = i+1, i3 = '##', fill='', align='<', num_width=2, col_width=15))
                except:
                    print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= '', col3= '', i1 = i, i2 = '##', i3 = '##', fill='', align='<', num_width=2, col_width=15))
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


def run(df):
    """
        Runs the functions in this module
    """
    while True:
        EDA_Views_options_msg()
        try: 
            choice = int(input("What would you like to know about the Dataset?: "))
        except:
            choice = None
            
        if choice ==  1:
            df_shape(df)
        
        elif choice == 2:
            print_nice_column_names(df)
            
        elif choice == 3:
            show_nulls(df)
            
        elif choice == 4:
            col_values_count(df)
            
        elif choice == 0:
            break
        
        elif choice == 99: 
            return 0
            
        else:
            print (choice)
            print ("No such option, try again.")

def EDA_Views_options_msg():
        """
            Prints menu page for to view information on the dataset
            Includs all function available in this library
        """
        
        print ( "Dataset Information Views Options: ")
        print ( " (1 )  Shape of data ")  
        print ( " (2 )  Colum names")
        print ( " (3 )  How many Null values are there?")
        print ( " (4 )  Count of values of columns")
        print ( " (0 )  I'm done with Views")
        print ( " (99)  Hard ESC")
        
def df_shape(df):
        """
            Prints the shape information and prints the number of rows and columns 
        """
        print ( df.shape )
        print ('There are {} rows.'.format(df.shape[0]))
        print ('There are {} columns.'.format(df.shape[1]))
        
def print_nice_column_names(df):
        """
            Takes in a dataframe as df and extract its column names    
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
                           
def show_nulls(df):
    """
        Takes in a DataFrame df
        Find the sum of the np.NaN values in the dataset for each column in the dataset
    """
    
    columns = pd.DataFrame(df.isnull().sum()).reset_index()
    columns.columns = ['Name', 'Sum']
    index = [i for i in columns.index.values if (i % 2) == 0]
    
    ### Find number of print spaces to use for sum amount
    num_spaces = int(np.max([len(str(num)) for num in columns['Sum']]))
    
    for i in index: 
        try:
            print ("{i1:{fill}{align}{index_width}}-{col1:{fill}{align}{col_width}} {sum1:{fill}{sum_align}{sum_width}} | {i2:{fill}{align}{index_width}}-{col2:{fill}{align}{col_width}} {sum2:{fill}{sum_align}{sum_width}}".format(col1 = columns.loc[i, 'Name'], col2 = columns.loc[i+1, 'Name'], i1 = i, i2 = i+1, sum1 = columns.loc[i, 'Sum'], sum2 = columns.loc[i+1, 'Sum'], fill='', align='<', sum_align='>', index_width=2, col_width=15, sum_width=num_spaces))
        except:
            print ("{i1:{fill}{align}{index_width}}-{col1:{fill}{align}{col_width}} {sum1:{fill}{sum_align}{sum_width}} | {i2:{fill}{align}{index_width}}-{col2:{fill}{align}{col_width}} {sum2:{fill}{sum_align}{sum_width}}".format(col1 = columns.loc[i, 'Name'], col2 = '', i1 = i, i2 = '##', sum1 = columns.loc[i, 'Sum'], sum2 = '', fill='', align='<', sum_align='>', index_width=2, col_width=15, sum_width=num_spaces))

def col_values_count(df):
    """
        Takes in a DataFRame, df 
        Cre
    """
    
    col_index_dict = {i:name for i,name in enumerate(df.columns)}
    
    while True:
        print ('\nList of columns available...')
        print_nice_column_names(df)
        try:
            col_choice = int(input('What column would you like to view?: '))
        
        except: 
            col_choice = None
        
        if col_choice in range(len(df.columns)):
            print (df[col_index_dict[col_choice]].value_counts())
            break
            
        else: 
            print ('No such option, try again')

               
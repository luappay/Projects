# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 15:28:07 2018

@author: PaulY
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



## %config InlineBackend.figure_format = 'retina'
## %matplotlib inline


class go_cray_EDA():
    
    def __init__(self, df, hist_pref=None):
        
        
        self.df_raw = df.copy(deep=True)
        self.df = df.copy(deep=True)
        
        self.hist_pref = hist_pref 
        
        self.save_directory = {}
        
        ### Column names and its order number for easy reference later on 
        self.col_index_dict = {i:name for i,name in enumerate(self.df.columns)}
        
    def initiate(self):
        """
            Initiates the EDA aid program
            Runs on a while loop whereby it lists down the possible options to run EDA on the data df
            Depending on the options, different Methods are executed
            Once an option is selected, the program will run the method, and return to the menu page
            The while loop breaks out when you selected the end option
        """
        
        while True: 
            self.EDA_options_msg()
            try: 
                choice = int(input("What would you like to do?: "))
            except:
                choice = None
            
            if choice == 1: 
                self.view_exit_choice = None
                self.run_views()
                if self.view_exit_choice == 0:
                    break

                
            elif choice == 2: 
                self.edit_exit_choice = None
                self.run_edits()
                if self.edit_exit_choice == 0:
                    break
                
                
            elif choice == 0:
                print ('Go Cray! Bye!!')
                break
            
            else:
                print ("""There's no such option, try again:)""")
    
    def EDA_options_msg(self):
        """
            Option messages for the menu page 
        """
        
        print ( "\nEDA Options: ")
        print ( " (1)  Information on Dataset ")  
        print ( " (2)  Feature engineering")
        print ( " (3)  Plot Graphs")
        print ( " (4)  Modeling")
        
        print ( " (0)  I'm done with EDA")
    
    

######################################################################################
### This part governs the Views funcatinality of the class. 
### All informative stuff


    def run_views(self):
        """
            Runs the methods of the Views module
            All descriptive information of the DataFrame
            No editing methods 
        """
        while True:
            self.EDA_Views_options_msg()
            try: 
                choice = int(input("What would you like to know about the Dataset?: "))
            except:
                choice = None
            
            if choice ==  1:
                self.df_shape()
        
            elif choice == 2:
                self.print_nice_column_names()
                
            elif choice == 3:
                self.show_nulls()
            
            elif choice == 4:
                self.col_values_count()
            
            elif choice == 0:
                break
        
            elif choice == 99: 
                self.view_exit_choice = 0
                break
            
            else:
                print (choice)
                print ("No such option, try again.")

    def EDA_Views_options_msg(self):
            """
                Prints menu page for to view information on the dataset
                Includs all function available in this library
            """
        
            print ( "\nDataset Information Views Options: ")
            print ( " (1 )  Shape of data ")  
            print ( " (2 )  Colum names")
            print ( " (3 )  How many Null values are there?")
            print ( " (4 )  Count of values of columns")
            print ( " (0 )  I'm done with Views")
            print ( " (99)  Hard ESC")
        
    def df_shape(self):
            """
                Prints the shape information and prints the number of rows and columns 
            """
            print ( self.df.shape )
            print ('There are {} rows.'.format(self.df.shape[0]))
            print ('There are {} columns.'.format(self.df.shape[1]))
        
    def print_nice_column_names(self):
            """
                Takes in a dataframe as df and extract its column names    
                Prints column names in neat order
            """
            index = [i for i in range(len(self.df.columns)) if (i % 3) == 0]
            columns = self.df.columns
            print ('\ncolumn names: ')
            for i in index:
                try:
                    print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= columns[i+1], col3= columns[i+2], i1 = i, i2 = i+1, i3 = i+2, fill='', align='<', num_width=2, col_width=15))
                except:
                
                    try:
                        print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= columns[i+1], col3= '', i1 = i, i2 = i+1, i3 = '##', fill='', align='<', num_width=2, col_width=15))
                    except:
                        print ("{i1:{fill}{align}{num_width}}-{col1:{fill}{align}{col_width}} | {i2:{fill}{align}{num_width}}-{col2:{fill}{align}{col_width}} | {i3:{fill}{align}{num_width}}-{col3:{fill}{align}{col_width}}".format(col1= columns[i], col2= '', col3= '', i1 = i, i2 = '##', i3 = '##', fill='', align='<', num_width=2, col_width=15))
                           


    def show_nulls(self):
        """
            Takes in a DataFrame df
            Find the sum of the np.NaN values in the dataset for each column in the dataset
        """
    
        columns = pd.DataFrame(self.df.isnull().sum()).reset_index()
        columns.columns = ['Name', 'Sum']
        index = [i for i in columns.index.values if (i % 2) == 0]
    
        ### Find number of print spaces to use for sum amount
        num_spaces = int(np.max([len(str(num)) for num in columns['Sum']]))
    
        for i in index: 
            try:
                print ("{i1:{fill}{align}{index_width}}-{col1:{fill}{align}{col_width}} {sum1:{fill}{sum_align}{sum_width}} | {i2:{fill}{align}{index_width}}-{col2:{fill}{align}{col_width}} {sum2:{fill}{sum_align}{sum_width}}".format(col1 = columns.loc[i, 'Name'], col2 = columns.loc[i+1, 'Name'], i1 = i, i2 = i+1, sum1 = columns.loc[i, 'Sum'], sum2 = columns.loc[i+1, 'Sum'], fill='', align='<', sum_align='>', index_width=2, col_width=15, sum_width=num_spaces))
            except:
                print ("{i1:{fill}{align}{index_width}}-{col1:{fill}{align}{col_width}} {sum1:{fill}{sum_align}{sum_width}} | {i2:{fill}{align}{index_width}}-{col2:{fill}{align}{col_width}} {sum2:{fill}{sum_align}{sum_width}}".format(col1 = columns.loc[i, 'Name'], col2 = '', i1 = i, i2 = '##', sum1 = columns.loc[i, 'Sum'], sum2 = '', fill='', align='<', sum_align='>', index_width=2, col_width=15, sum_width=num_spaces))

    def col_values_count(self):
        """
            Takes in a DataFRame, df 
            Cre
        """
    
        while True:
            print ('\nList of columns available...')
            self.print_nice_column_names()
            try:
                col_choice = int(input('What column would you like to view?: '))
        
            except: 
                col_choice = None
        
            if col_choice in range(len(self.df.columns)):
                print (self.df[self.col_index_dict[col_choice]].value_counts())
                break
            
            else: 
                print ('No such option, try again')
                
                
                
                
                
                
                
                
                

############################################################################
### This part governs making changes of the dataframe
### Please REMEMBER TO USE self.df when making changes

    def run_edits(self):
        """
            Runs the methods of the Edits module
            All editing functionality of the module will be placed here
            Edits will be made on the DataFrame in these module
        """
        while True:
            self.EDA_Edits_options_msg()
            try: 
                choice = int(input("What would you like to do to the Dataset?: "))
            except:
                choice = None
            
            if choice ==  1:
                self.replace_cells()
        
            elif choice == 9: 
                self.reset_df()
                print ('\nThe Dataset (DataFrame) has been reset.')
                
                
            elif choice == 0:
                break
        
            elif choice == 99: 
                self.edit_exit_choice = 0
                break
            
            else:
                print (choice)
                print ("No such option, try again.")
                
                

    
    def EDA_Edits_options_msg(self):
        """
            Prints menu page to edit the dataset
            Includs all function available in this module
        """
        
        print ( "\nDataset Information Editing Options: ")
        print ( " (1 )  Replace values of cells ")
        print ( " (9 )  Hard reset DataFrame ")
        print ( " (0 )  I'm done making Edits")
        print ( " (99)  Hard ESC")
        
        
        
        
    def replace_cells(self):
        """
            Replaces all the instances of a particular value in the selected columns
            Method will request input on the columns to make the change on
            Once the columns is selected, the module will run a value_counts on the column and request for another input of the value to change 
            Finally, the method will ask for the input to be changed to
            Changes will be stored in self.df
        """
        
        cont = None
        
        while True:
            
            if cont == 'n':
                break
            
            ### Print columns to choose option 
            self.print_nice_column_names()
            try:
                col_choice = int(input('\nWhich column would you like to work on?: '))
            except:
                print ('No such option, try again!')
                self.replace_cells()
                break
            
            
            ### Print column values to choose option 
            try:
                col_name, val_map = self.print_unique_msg_orderly(col_choice)
            except:
                print ('No such column index, try again!')
                self.replace_cells()
                break
            
            ### Asking for input to initiate the replacement
            try:
                val_choice = int(input('\nWhich value would you like to replace?: '))
            except:
                val_choice = None
            new_val = input('\nWhat do you want the new value to be?: ')
            
            ### Replace values
            try:
                self.df[col_name].replace(to_replace= val_map[val_choice], value= new_val, inplace= True)
                print ('\nAll {to_replace} in the {col_name} column have been replaced with {new_val}'.format(to_replace= val_map[val_choice], col_name= col_name, new_val= new_val))
            except:
                print ('Please only choose index options available to you.\nPlease try from the start again')
                self.replace_cells()
            
            
            ### Ask if user wants to continue editing
            cont = None
            while cont not in ['y','n']:
                cont = input('Edit another value?(y/n): ')
                if cont.lower() == 'n':
                    break
                else:
                    print ('No such option, try again!')
            
        
    def print_unique_msg_orderly(self, col_choice):
        """
            Support function for <replace_cells(self)>
            Takes in the column of choice in the form of an index, col_choice and prints the unique values of the column neatly
            Also prints its associating index for manipulation
        """
        
        ### Get col name
        col_name = self.col_index_dict[col_choice]
        
        
        ### Get unique values of column
        uniq_vals = self.df[col_name].unique()
        
        ### set index for unique col values
        map_index_to_vals = {i:val for i,val in enumerate(uniq_vals)}
        
        ### map col values to their count number
        val_counts = self.df[col_name].value_counts()
        map_val_to_num = {val_counts.index[i] : amt for i,amt in enumerate(val_counts)}
        
        ### Add np.nan count into the mapping
        map_val_to_num[np.nan] = self.df[col_name].isnull().sum()


        
        for i, val in enumerate(uniq_vals):
            print ('{i:{fill}{align}{i_width}}-{name:{fill}{align}{val_width}} {count}'.format(i=i, name=val, fill=' ', align='<', i_width = 2, val_width = 10, count= map_val_to_num[val]))
            
        return col_name, map_index_to_vals
    
    def reset_df(self):
        """
            As the name suggests, it resets the DataFrame to the initial state where it was first loaded in.
            Nothing too fancy
        """
        
        self.df = self.df_raw.copy(deep=True)
        
        
        
#    def create_dummy_vars(self):
       # """
        #    Create dummy variables for the 
        
            
            
            


    







                           
house = pd.read_csv('./housing.csv')

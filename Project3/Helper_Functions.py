# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 23:29:25 2019

@author: Paul Yap
"""

### Find names of non-zero coefficients from lasso regression 

def lasso_coef_filter(df): 
    """
        Takes in DataFrame, df, of the post lasso regression coefficent values
        Return a list of column names that have non-zero coefficient
    """
    return_list = []
    
    df_non_zeros = df[~(abs(df['Coef']) == 0)]
    for index in df_non_zeros.index.values:
        return_list += [index]
        
    return return_list


### Generate formula for statsmodel ols 

def formula_generator(lis, y): 
    """
        Takes in list of coefficient names, lis
        Takes in target column name, y
        Generate formula string for statesmodel ols use
        Note: If 'Intercept' is present in the list, function will remove it
    """
    formula = '{y} ~ '.format(y=y)
    
    if lis[0] == 'Intercept':
        lis.pop(0)
    
    for names in lis: 
        formula += '{} + '.format(str(names))
    
    formula = formula[:-2]
    return formula

### Filter out names with P-Values in acceptable range

def sig_p_filter(pvalues, target=0.05):
    """
        Takes in an array of P-values as pvalues, with the coefficient names as its index
        Returns list of coefficients with P-values smaller than the target p-value
    """
    accepted_list = []
    for i, value in enumerate(pvalues):
        if value < target: 
            accepted_list += [pvalues.index[i]]
            
    return accepted_list
names = sig_p_filter(model.pvalues)
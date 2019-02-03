# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 23:25:47 2019

@author: Paul Yap
"""


from selenium import webdriver
import os
import requests
from bs4 import BeautifulSoup
import json
import pprint
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time
from timeit import default_timer as timer

class CFMiner():
    
    def __init__(self): 
        """
            initiates a JSMiner spider object
        """
        
        ### Assigm variables for dataset
        self.Job_Title = []
        self.Company_Name = []
        self.Industry = []
        self.Commitment = []
        self.Address = []
        self.Seniority = []
        self.Salary_Range = []
        self.Salary_Period = []
        self.Posting_Date = []
        self.Closing_Date = []
        self.Roles_And_Responsibilities = []
        self.Requirements = []
        self.About_The_Company = []
        self.Govt_Support =[]
        
        ### Ready column names for later use
        self.Column_Names = ['Url',
                        'Job_Title',
                        'Company_Name',
                        'Industry',
                        'Commitment',
                        'Address',
                        'Seniority',
                        'Salary_Range',
                        'Salary_Period',
                        'Posting_Date',
                        'Closing_Date',
                        'Roles_And_Responsibilities',
                        'Requirements',
                        'About_The_Company',
                        'Govt_Support']
        
        
        
        ### Initiate driver for webscraping 
        chromedriver = '.\chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver

        ### Create/initiate browser
        self.browser = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe')
        
        ### Setup url to enter to
        url = 'https://www.mycareersfuture.sg/'
        
        ### Enter page
        self.browser.get(url)
        
        
    def grab_links(self, query_list = None):
        
        start = timer()
        self.links = []
        
        if query_list == None:
            queries = ['data']
        else:
            queries = query_list
            
        for query in queries:
            
            ### Enter search bar
            search_bar = self.browser.find_element_by_id('search-text')
            search_bar.clear()
            search_bar.send_keys(query)
            self.browser.find_element_by_id('search-button').click()
            
            ### Setup loop information
            main_url = self.browser.current_url[:-1]
            next_page = True
            page_num = 0
            
            while next_page:
                url = main_url + str(page_num)
                
                
                try:
                    self.browser.get(url)
                    time.sleep(6)
                    html = self.browser.page_source
                    bs = BeautifulSoup(html)
                    
                except:
                    pd.DataFrame(self.links, columns=['links']).to_csv(path_or_buf='links.csv')
                    next_page = False
                    end = timer()
                    print ('Reached page limit for search results for: {}\nTotal {} links grabbed.'.format(query, len(self.links)))
                    print ('{} seconds elapsed...'.format(end - start))
    
                    
                if len(self.links) % 200 == 0: 
                    pd.DataFrame(self.links, columns=['links']).to_csv(path_or_buf='links.csv')
                    end = timer()
                    print ('{} Links grabbed... {} seconds elapsed.'.format(len(self.links), end - start))
                
                for link in bs.findAll("a", {'class' : 'bg-white mb3 w-100 dib v-top pa3 no-underline flex-ns flex-wrap JobCard__card___22xP3'}):
                    self.links += [link['href']]
                    
                if page_num > 208:
                    pd.DataFrame(self.links, columns=['links']).to_csv(path_or_buf='links.csv')
                    end = timer()
                    print ('{} Links grabbed, task completed. {} Seconds elapsed...'.format(len(self.links), end - start))
                    break
                
                page_num += 1
                





###############################################################################################



        
    def automode(self):
        
        start = timer()
        self.grab_links()
        self.dont_look_back()
        end = timer()
        print ('Scrapping completed, {} seconds elapsed...'.format(end - start))
        
        
##############################################################################################
    
    def dont_look_back(self, but_maybe_look_back_at = None, start_from = 0, filepath= None):
        
        self.count = 0
        self.data = {}
        start = timer()
        self.error_count = 0
        
        if filepath != None: 
            self.links = pd.read_csv(filepath)['links']
            
        else:
            self.links = pd.read_csv('./links.csv')['links']
        
        if but_maybe_look_back_at == None:
            check = len(self.links)
        else:
            check = but_maybe_look_back_at
        
        for i, link in enumerate(self.links[start_from:]):
            url = 'https://www.mycareersfuture.sg' + link
            
            try:
                self.data[url] = self.scrap(str(url), return_=True)
                self.count += 1
            
            except:
                self.save_data()
                self.error_count += 1
                
                
                try:
                    self.browser.get(url)
                    print ('Error at scrapping Index No. {} Url... Skipping...'.format(i+start_from))
                    pass
                
                except:
                    print ('Browser seems to stop working when processing Url with Index No. {}... Exiting script...'.format(i+start_from))
                    break
                    
                    
            if self.count % 50 == 0:
                self.save_data()
                end = timer()
                print ('Scrapped {} JDs... {} seconds elapsed.'.format(self.count, end - start))

 
            
            if self.count > check:
                self.save_data()
                break
            
            
                 
        self.save_data()
        end = timer()
        print ('Scrapping successfully completed. {} JDs scrapped'.format(self.count))
        print ('Task(s) was/were completed in {} seconds'.format(end - start))

            
#################################################################################################
        
    def save_data(self):
        
        agg_information_list = []
 
        for row in self.data.keys():
            agg_information_list += [[row, 
                                      self.data[row]['Job_Title'],
                                      self.data[row]['Company_Name'],
                                      self.data[row]['Industry'],
                                      self.data[row]['Commitment'],
                                      self.data[row]['Address'],
                                      self.data[row]['Seniority'],
                                      self.data[row]['Salary_Range'],
                                      self.data[row]['Salary_Period'],
                                      self.data[row]['Posting_Date'],
                                      self.data[row]['Closing_Date'],
                                      self.data[row]['Roles_And_Responsibilities'],
                                      self.data[row]['Requirements'],
                                      self.data[row]['About_The_Company'],
                                      self.data[row]['Govt_Support']]]
            
        pd.DataFrame(agg_information_list, columns=self.Column_Names).to_csv(path_or_buf='dataset.csv')
            
#############################################################################################            

    def scrap(self, url, return_=False):
        """
            Takes in an url as a string
            Scraps Job listing information from the page 
            Returns a dictionary of dictionary format information dump, if parameter set True
        """
        information = {}
        
        self.browser.get(url)
        time.sleep(np.random.randint(3,4))
        
        html = self.browser.page_source
        bs = BeautifulSoup(html)
        
        
    ### Job Title
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job_title"]').text != '':
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job_title"]').text
                information['Job_Title'] = holding_str
                self.Job_Title += [holding_str]
                
            else:
                information['Job_Title'] = 'No Information'
                self.Job_Title += [holding_str]
                
        except:
            information['Job_Title'] = 'Error'
            self.Job_Title += [holding_str]
            
            
    ### Company Name
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[2]/div[1]/section[1]/p').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[2]/div[1]/section[1]/p').text
                information['Company_Name'] = holding_str
                self.Company_Name += [holding_str]
                
            else:
                information['Company_Name'] = 'No Information'
                self.Company_Name += [holding_str]
                
        except:
            information['Company_Name'] = 'Error'
            self.Company_Name += [holding_str]
            
            
    ### Industry
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job-categories"]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job-categories"]').text
                information['Industry'] = holding_str
                self.Industry += [holding_str]
                
            else:
                information['Industry'] = 'No Information'
                self.Industry += [holding_str]
                
        except:
            information['Industry'] = 'Error'
            self.Industry += [holding_str]         
            

    ### Commitment
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="employment_type"]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="employment_type"]').text
                information['Commitment'] = holding_str
                self.Commitment += [holding_str]
                
            else:
                information['Commitment'] = 'No Information'
                self.Commitment += [holding_str]
                
        except:
            information['Commitment'] = 'Error'
            self.Commitment += [holding_str]   
            
            

    ### Address
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="address"]/a').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="address"]/a').text
                information['Address'] = holding_str
                self.Address += [holding_str]
                
            else:
                information['Address'] = 'No Information'
                self.Address += [holding_str]
                
        except:
            information['Address'] = 'Error'
            self.Address += [holding_str]   
            
            
            
    ### Seniority
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="seniority"]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="seniority"]').text
                information['Seniority'] = holding_str
                self.Seniority += [holding_str]
                
            else:
                information['Seniority'] = 'No Information'
                self.Seniority += [holding_str]
                
        except:
            information['Seniority'] = 'Error'
            self.Seniority += [holding_str]   
            
            
            
    ### Salary_Range
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[2]/div[1]/div/section[2]/div/span[2]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[2]/div[1]/div/section[2]/div/span[2]').text
                information['Salary_Range'] = holding_str
                self.Salary_Range += [holding_str]
                
            else:
                information['Salary_Range'] = 'No Information'
                self.Salary_Range += [holding_str]
                
        except:
            information['Salary_Range'] = 'Error'
            self.Salary_Range += [holding_str]  
            
            
            
    ### Salary_Period
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[2]/div[1]/div/section[2]/div/span[3]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[2]/div[1]/div/section[2]/div/span[3]').text
                information['Salary_Period'] = holding_str
                self.Salary_Period += [holding_str]
                
            else:
                information['Salary_Period'] = 'No Information'
                self.Salary_Period += [holding_str]
                
        except:
            information['Salary_Period'] = 'Error'
            self.Salary_Period += [holding_str] 
            
            
            
    ### Posting_Date
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="last_posted_date"]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="last_posted_date"]').text
                information['Posting_Date'] = holding_str
                self.Posting_Date += [holding_str]
                
            else:
                information['Posting_Date'] = 'No Information'
                self.Posting_Date += [holding_str]
                
        except:
            information['Posting_Date'] = 'Error'
            self.Posting_Date += [holding_str]  
            
            
    ### Closing_Date
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="expiry_date"]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="expiry_date"]').text
                information['Closing_Date'] = holding_str
                self.Closing_Date += [holding_str]
                
            else:
                information['Closing_Date'] = 'No Information'
                self.Closing_Date += [holding_str]
                
        except:
            information['Closing_Date'] = 'Error'
            self.Closing_Date += [holding_str]  
            
            
            
    ### Roles_And_Responsibilities
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job_description"]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job_description"]').text
                information['Roles_And_Responsibilities'] = holding_str
                self.Roles_And_Responsibilities += [holding_str]
                
            else:
                information['Roles_And_Responsibilities'] = 'No Information'
                self.Roles_And_Responsibilities += [holding_str]
                
        except:
            information['Roles_And_Responsibilities'] = 'Error'
            self.Roles_And_Responsibilities += [holding_str] 
            
            
            
    ### Requirements
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="requirements"]').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="requirements"]').text
                information['Requirements'] = holding_str
                self.Requirements += [holding_str]
                
            else:
                information['Requirements'] = 'No Information'
                self.Requirements += [holding_str]
                
        except:
            information['Requirements'] = 'Error'
            self.Requirements += [holding_str] 
            
            
            
    ### About_The_Company
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job_details"]/div[2]/div[1]/div/div/section/section/div[2]/div').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job_details"]/div[2]/div[1]/div/div/section/section/div[2]/div').text
                information['About_The_Company'] = holding_str
                self.About_The_Company += [holding_str]
                
            else:
                information['About_The_Company'] = 'No Information'
                self.About_The_Company += [holding_str]
                
        except:
            information['About_The_Company'] = 'Error'
            self.About_The_Company += [holding_str] 
            
            
            
    ### Govt_Support?
        
        try:
            if self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[4]/section').text:
                holding_str = ''
                
                holding_str = self.browser.find_element_by_xpath('//*[@id="job_details"]/div[1]/div[4]/section').text
                information['Govt_Support'] = holding_str
                self.Govt_Support += [holding_str]
                
            else:
                information['Govt_Support'] = 'No Information'
                self.Govt_Support += [holding_str]
                
        except:
            information['Govt_Support'] = 'Error'
            self.Govt_Support += [holding_str] 
            
            
            
        if return_:
            return information         
        
        
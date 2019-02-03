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

class JSMiner():
    
    def __init__(self): 
        """
            initiates a JSMiner spider object
        """
        
        ### Assigm variables for dataset
        self.Job_Description = []
        self.Company_Overview = []
        self.Why_Join_Us_Statement = []
        self.Work_Location = []
        self.Position_Title = []
        self.Avg_Processing_Time = []
        self.Industry = []
        self.Company_Size = []
        self.Working_Hours = []
        self.Dress_Code = []
        self.Work_Benefits = []
        self.Spoken_Language = []
        self.Salary_Range =[]
        self.Experience_Needed = []
        self.General_Work_Location =[]
        self.Company_Name = []
        
        ### Ready column names for later use
        self.Column_Names = ['Url',
                        'Job_Description',
                        'Company_Overview',
                        'Why_Join_Us_Statement',
                        'Work_Location',
                        'Position_Title',
                        'Avg_Processing_Time',
                        'Industry',
                        'Company_Size',
                        'Working_Hours',
                        'Dress_Code',
                        'Work_Benefits',
                        'Spoken_Language',
                        'Salary_Range',
                        'Experience_Needed',
                        'General_Work_Location',
                        'Company_Name']
        
        
        
        ### Initiate driver for webscraping 
        chromedriver = '.\chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver

        ### Create/initiate browser
        self.browser = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe')
        
        ### Setup url to enter to
        url = 'https://www.jobstreet.com.sg/'
        
        ### Enter page
        self.browser.get(url)
        
        ### Login to Jobstreet
        username = 'paulyap.h@gmail.com'
        password = 'TESTing12345'
        
        ### Login to Jobstreet 
        search_job_button = self.browser.find_element_by_id('header-login-button')
        search_job_button.click()
        
        ### Rest before interacting with the login bar
        time.sleep(2)
        
        ### Enter username
        username_bar = self.browser.find_element_by_name('login_id')
        username_bar.clear()
        username_bar.send_keys(username)
        
        ### Enter password
        pw_bar = self.browser.find_element_by_name('password')
        pw_bar.clear()
        pw_bar.send_keys(password)
        
        ### Log in 
        login_button = self.browser.find_element_by_name('btnSignIn')
        login_button.click()
        
        ### Close irritating login button
        close_icon = self.browser.find_element_by_class_name('icon-close')
        close_icon.click()
        
        ### Click 'Search Jobs'
        self.browser.find_element_by_id('header_job_link').click()
        
        ### Search for 'data' related jobs
        time.sleep(2)
        search_bar = self.browser.find_element_by_id('search_box_keyword')
        search_bar.clear()
        search_bar.send_keys('data')
        
        ### Click 'search'
        self.browser.find_element_by_id('header_searchbox_btn').click()
        self.url = self.browser.current_url

    def load_links(self, links_to_get=None):
        """
            Start from the first page of the 'job search' page
                Grab all the job posts links
                Click into the next page
                    Repeat: Grab all the job posts links again
                    Repeat this cycle until you reached the amount of links you are supposed to get
                        or in the case where var 'links_to_get' == None, GRAB ALL WHAHAHAHA
        """

        self.links = []
        next_page= True
        
        ### Go to initial search page, grab the page source and load it in beautifulsoup
        self.browser.get(self.url)
        html = self.browser.page_source
        bs = BeautifulSoup(html)
        
        ### Record start time to time function 
        start = timer()
        
        while next_page:
            
            for link in bs.find_all('a', {'class':'position-title-link'}):
                if 'Rank' in link['href']:
                    self.links += [link['href']]
                    
            try:
                if len(self.links) > links_to_get:
                    next_page = False
            except:
                
                try:
                    self.browser.find_element_by_id('page_next').click()
                    html = self.browser.page_source
                    bs = BeautifulSoup(html)
                except: 
                    print ('Got an error going into the next page')
                    next_page = False
            
            if len(self.links) % 1000 == 0:
                pd.DataFrame(self.links, columns=['links']).to_csv(path_or_buf='links.csv')
                end = timer()
                print ('{} Links grabbed... {} seconds elapsed.'.format(len(self.links), end - start))
            
            time.sleep(np.random.randint(1,2))
               
                
        pd.DataFrame(self.links, columns=['links']).to_csv(path_or_buf='links.csv')
        print ('{} links successfully saved'.format(len(self.links)))
        end = timer()
        print ('Task(s) took {} seconds to complete'.format(end-start))
#        return self.links
    
##############################################################################################
        
    def automode(self):
        
        start = timer()
        self.load_links()
        self.dont_look_back()
        end = timer()
        print ('Scrapping completed, {} seconds elapsed...'.format(end - start))
        
        
##############################################################################################
    
    def dont_look_back(self, but_maybe_look_back_at = None, filepath= None):
        
        self.count = 0
        self.data = {}
        start = timer()
        self.error_count = 0
        
        if filepath != None: 
            self.links = pd.read_csv(filepath)['links']
        
        if but_maybe_look_back_at == None:
            check = len(self.links)
        else:
            check = but_maybe_look_back_at
        
        for link in self.links:
            
            try:
                self.data[link] = self.scrap(str(link), return_=True)
                self.count += 1
            
            except:
                self.save_data()
                self.error_count += 1
#                r = requests.get(link)
#                print (r.status_codes)
                print ('No. {} Error at scrapping JD... Skipping...'.format(self.error_count))
                pass
            
            if self.count % 100 == 0:
                self.save_data()
                end = timer()
                print ('Scrapped {} JDs... {} seconds elapsed.'.format(self.count, end - start))
 #               open('JobStreet.txt', 'w', encoding="utf-8").write(str(self.data))
 
            if self.count % 10 == 0:
                time.sleep(np.random.randint(20,30))
            
            if self.count > check:
                self.save_data()
                break

            
 #               with open('JobStreet.txt', 'w') as file:
 #                   file.write(str(self.data))
            #time.sleep(np.random.randint(1,6))
                 
        self.save_data()
        end = timer()
        print ('Scrapping successfully completed. {} JDs scrapped'.format(self.count))
        print ('Task(s) was/were completed in {} seconds'.format(end - start))

            
#################################################################################################
        
    def save_data(self):
        
        agg_information_list = []
 
        for row in self.data.keys():
            agg_information_list += [[row, 
                                      self.data[row]['Job_Description'],
                                      self.data[row]['Company_Overview'],
                                      self.data[row]['Why_Join_Us_Statement'],
                                      self.data[row]['Work_Location'],
                                      self.data[row]['Position_Title'],
                                      self.data[row]['Avg_Processing_Time'],
                                      self.data[row]['Industry'],
                                      self.data[row]['Company_Size'],
                                      self.data[row]['Working_Hours'],
                                      self.data[row]['Dress_Code'],
                                      self.data[row]['Work_Benefits'],
                                      self.data[row]['Spoken_Language'],
                                      self.data[row]['Salary_Range'],
                                      self.data[row]['Experience_Needed'],
                                      self.data[row]['General_Work_Location'],
                                      self.data[row]['Company_Name']]]
            
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
        html = self.browser.page_source
        
        bs = BeautifulSoup(html)
        
        
    ### Job Description
        
        try:
            if len(bs.findAll('div', {'id' : 'job_description'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('div', {'id' : 'job_description'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Job_Description'] = holding_lis
                self.Job_Description += [holding_lis]
                
            else:
                information['Job_Description'] = 'No Information'
                self.Job_Description += [holding_lis]
                
        except:
            information['Job_Description'] = 'Error'
            self.Job_Description += [holding_lis]
            
    ### Company Overview       
            
        try:
            if len(bs.findAll('div', {'id' : 'company_overview_all'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('div', {'id' : 'company_overview_all'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Company_Overview'] = holding_lis
                self.Company_Overview += [holding_lis]
                
            else:
                information['Company_Overview'] = 'No Information'
                self.Company_Overview += [holding_lis]
        
        except:
            information['Company_Overview'] = 'Error'
            self.Company_Overview += [holding_lis]
        
            
    ### Why Join Us Statement       
            
        try:
            if len(bs.findAll('div', {'id' : 'why_join_us_all'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('div', {'id' : 'why_join_us_all'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Why_Join_Us_Statement'] = holding_lis
                self.Why_Join_Us_Statement += [holding_lis]
        
            else:
                information['Why_Join_Us_Statement'] = 'No Information'
                self.Why_Join_Us_Statement += [holding_lis]
        
        except:
            information['Why_Join_Us_Statement'] = 'Error'
            self.Why_Join_Us_Statement += [holding_lis]    
            
    ### Work Location       
            
        try:
            if len(bs.findAll('p', {'class' : 'add-detail-p'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'class' : 'add-detail-p'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Work_Location'] = holding_lis
                self.Work_Location += [holding_lis]
        
            else:
                information['Work_Location'] = 'No Information'
                self.Work_Location += [holding_lis]
        
        except:
            information['Work_Location'] = 'Error'
            self.Work_Location += [holding_lis]    
            
    ### Position Title       
            
        try:
            if len(bs.findAll('h1', {'id' : 'position_title'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('h1', {'id' : 'position_title'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Position_Title'] = holding_lis
                self.Position_Title += [holding_lis]
        
            else:
                information['Position_Title'] = 'No Information'
                self.Position_Title += [holding_lis]
        
        except:
            information['Position_Title'] = 'Error'
            self.Position_Title += [holding_lis]    
    
    ### Average Processing Time       
            
        try:
            if len(bs.findAll('p', {'id' : 'fast_average_processing_time'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'id' : 'fast_average_processing_time'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Avg_Processing_Time'] = holding_lis
                self.Avg_Processing_Time += [holding_lis]
        
            else:
                information['Avg_Processing_Time'] = 'No Information'
                self.Avg_Processing_Time += [holding_lis]
        
        except:
            information['Avg_Processing_Time'] = 'Error'    
            self.Avg_Processing_Time += [holding_lis]    
            
    ### Industry     
            
        try:
            if len(bs.findAll('p', {'id' : 'company_industry'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'id' : 'company_industry'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Industry'] = holding_lis
                self.Industry += [holding_lis]
                
            else:
                information['Industry'] = 'No Information'
                self.Industry += [holding_lis]
        
        except:
            information['Industry'] = 'Error'    
            self.Industry += [holding_lis]    
    
    ### Company Size     
            
        try:
            if len(bs.findAll('p', {'id' : 'company_size'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'id' : 'company_size'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Company_Size'] = holding_lis
                self.Company_Size += [holding_lis]
        
            else:
                information['Company_Size'] = 'No Information'
                self.Company_Size += [holding_lis]
            
        except:
            information['Company_Size'] = 'Error'    
            self.Company_Size += [holding_lis]
            
    ### Working Hours     
            
        try:
            if len(bs.findAll('p', {'id' : 'work_enviroment_working_hours'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'id' : 'work_enviroment_working_hours'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Working_Hours'] = holding_lis
                self.Working_Hours += [holding_lis]
            
            else:
                information['Working_Hours'] = 'No Information'
                self.Working_Hours += [holding_lis]
        
        except:
            information['Working_Hours'] = 'Error'   
            self.Working_Hours += [holding_lis]    
            
    ### Dress Code     
            
        try:
            if len(bs.findAll('p', {'id' : 'work_enviroment_dress_code'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'id' : 'work_enviroment_dress_code'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Dress_Code'] = holding_lis
                self.Dress_Code += [holding_lis]
        
            else:
                information['Dress_Code'] = 'No Information'
                self.Dress_Code += [holding_lis]
        
        except:
            information['Dress_Code'] = 'Error'   
            self.Dress_Code += [holding_lis]    
            
    ### Work Benefits     
            
        try:
            if len(bs.findAll('p', {'id' : 'work_enviroment_benefits'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'id' : 'work_enviroment_benefits'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Work_Benefits'] = holding_lis
                self.Work_Benefits += [holding_lis]
        
            else:
                information['Work_Benefits'] = 'No Information'
                self.Work_Benefits += [holding_lis]
                
        except:
            information['Work_Benefits'] = 'Error'
            self.Work_Benefits += [holding_lis]
            
            
    ### Spoken Language     
            
        try:
            if len(bs.findAll('p', {'id' : 'work_enviroment_spoken_language'})) > 0:
                holding_lis = ''
                
                for info in bs.findAll('p', {'id' : 'work_enviroment_spoken_language'}):
                    holding_lis += info.text.replace('\n','').replace('\t','').replace('\xa0', ' ')
                information['Spoken_Language'] = holding_lis
                self.Spoken_Language += [holding_lis]
                
            else:
                information['Spoken_Language'] = 'No Information'
                self.Spoken_Language += [holding_lis]
        
        except:
            information['Spoken_Language'] = 'Error'
            self.Spoken_Language += [holding_lis]    
            
    ### Salary Range     
            
        try:
            holding_lis = self.browser.find_element_by_xpath('//*[@id="salary_range"]').text.replace('\n','').replace('\t','').replace('\xa0', ' ')
            information['Salary_Range'] = holding_lis
            self.Salary_Range += [holding_lis]    
        
        except:
            information['Salary_Range'] = 'Error'
            self.Salary_Range += [holding_lis]
            
    
    ### Experience Needed / Required     
            
        try:
            holding_lis = self.browser.find_element_by_xpath('//*[@id="years_of_experience"]').text.replace('\n','').replace('\t','').replace('\xa0', ' ')
            information['Experience_Needed'] = holding_lis
            self.Experience_Needed += [holding_lis]
        
        except:
            information['Experience_Needed'] = 'Error'
            self.Experience_Needed += [holding_lis]
            
            
    ### General Work Location     
            
        try:
            holding_lis = self.browser.find_element_by_xpath('//*[@id="single_work_location"]').text.replace('\n','').replace('\t','').replace('\xa0', ' ')
            information['General_Work_Location'] = holding_lis
            self.General_Work_Location += [holding_lis]
        
        except:
            information['General_Work_Location'] = 'Error'
            self.General_Work_Location += [holding_lis]
            
    ### Company Name
            
        try:
            holding_lis = self.browser.find_element_by_xpath('//*[@id="company_name"]/a').text.replace('\n','').replace('\t','').replace('\xa0', ' ')
            information['Company_Name'] = holding_lis
            self.Company_Name += [holding_lis]
        
        except:
            information['Company_Name'] = 'Error'
            self.Company_Name += [holding_lis]
            
        if return_:
            return information         
        
        
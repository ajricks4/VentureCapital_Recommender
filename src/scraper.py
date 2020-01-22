import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import selenium.webdriver.support.ui as ui
import time

class VC_Scrape:

    def __init__(self,vc_df):
        self.df = vc_df
        self.driver = webdriver.Safari()

    def al_check(self):
        self.df['AL_Check'] = self.df['Angellist_Tag'].apply(lambda x: al_check_webpage(x,self.driver))


    def save_progress(self):
        self.df.to_csv('CB_csv/scraped_df.csv')

    def load_progress(self):
        self.df = pd.read_csv('CB_csv/scraped_df.csv')

    def al_scrape_investments(self):
        port_comps = []
        comp_markets = []
        for i,j in zip(self.df['AL_Check'],self.df['Angellist_Tag']):
            comps = []
            links = []
            markets = []
            if i == 'Exists':
                time.sleep(5)
                url = j
                self.driver.get(url)
                time.sleep(2)
                try:
                    elems = self.driver.find_element_by_css_selector("section.component_aa8ec").find_elements_by_css_selector("a.component_21e4d")
                except:
                    elems = []
                time.sleep(5)
                for i in elems:
                    if i.text != '' and i.text != 'Exit':
                        comps.append(i.text)
                for i in range(0,len(elems),2):
                    links.append(elems[i].get_attribute('href'))
                for k in links:
                    try:
                        self.driver.get(k)
                    except:
                        continue
                    time.sleep(5)
                    try:
                        market_tags = self.driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[4]/aside/div/div[1]/dl/dt[4]').find_elements_by_tag_name('a')
                    except:
                        continue
                    for j in market_tags:
                        markets.append(j.text)
            port_comps.append(comps)
            comp_markets.append(markets)
        self.df['AL_Portfolio'] = port_comps
        self.df['AL_Markets'] = comp_markets








def al_check_webpage(url,driver):
    """
    Scrapes Angellist to check whether a guessed Angellist url directs to a functioning page.

    Args:
    url (string): Estimated angellist url of a given venture capital firm.

    Returns:
    webpage (string): Either 'Exists' or 'Does Not Exist' to determine which estimated Angellist urls work.
    """
    time.sleep(np.random.randint(1,6))
    try:
        driver.get(url)
    except:
        return 'Unable to parse url'
    try:
        x = driver.find_element_by_class_name('h1_a61cb').text
        if x == '404':
            webpage = 'Does Not Exist'
    except:
        webpage = 'Exists'
    return webpage

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui






class Crunchbase_Scraper:

    def __init__(self,df):
        self.df = df
        self.driver = webdriver.Safari()
        self.user =

    def login(self):
        f = open('credentials.txt','r')
        user = str(f.readline())
        pw = str(f.readline())
        self.login = {'user':user,'pw':pw }


    def check_page(self):
        pass

    def scrape_page(self):
        pass

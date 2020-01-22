import numpy as np
import pandas as pd
import os
import unidecode

def extract_cb_df():
    """
    Extracts the filepaths of the Crunchbase csv files and returns a dataframe

    Args:
    None

    Returns:
    cb_df (pandas DataFrame): dataframe containing the data in the Crunchbase csvs
    that was obtained using Crunchbase Pro.
    """
    filepaths = []
    for j in os.listdir('CB_csv'):
        if 'scraped' not in j:
            filepaths.append('CB_csv/'+j)
    cb_df = pd.concat(map(pd.read_csv,filepaths))
    return cb_df

def clean_cb_df(cb_df):
    """
    Returns a dataframe that has relevant columns and
    cleaned up columns

    Args:
    cb_df (pandas DataFrame): dataframe that is created from the data pulled
    from Crunchbase containing a list of venture capital firms and their data

    Returns:
    clean_df (pandas DataFrame): a dataframe containing relevant information
    for analysis
    """
    cols = ["Organization/Person Name","Organization/Person Name URL","Location",
            "Regions","Full Description","Description","Founded Date","Website",
            "Investor Type","Investment Stage","Number of Portfolio Organizations",
            "Number of Investments","Number of Lead Investments","Number of Exits",
            "Number of Exits (IPO)","CB Rank (Investor)"]
    clean_df = cb_df[cols]
    clean_df['Founded Date'].fillna(0,inplace=True)
    clean_df['Founded_Year'] = clean_df['Founded Date'].apply(lambda x: 0 if x == 0 else int(x.split('-')[0]))
    clean_df = clean_df[(clean_df['Investor Type'].str.contains('Venture')) | (clean_df['Investor Type'].str.contains('VC')) | (clean_df['Investor Type'].str.contains('Angel')) | (clean_df['Investor Type'].str.contains('Accelerator')) | (clean_df['Investor Type'].str.contains('Incubator'))]
    clean_df['Region_ID'] = clean_df['Regions'].apply(lambda x: clean_region(x))
    clean_df.drop(['Founded Date','Regions'],axis=1,inplace=True)
    clean_df.reset_index(inplace=True)
    clean_df.drop('index',axis=1,inplace=True)
    clean_df['Angellist_Tag'] = clean_df['Organization/Person Name'].apply(lambda x: create_al_fund_tag(x))
    return clean_df



def clean_region(reg):
    """
    Classifies a region into one of the following groups:
    Silicon Valley,
    East Coast,
    Non SV / East Coast.

    Args:
    reg (string): string detailing the region of a venture capital firm as described by Crunchbase

    Returns:
    reg_code (string): string determining which of three main areas the venture capital firm is located in.
    """
    if 'San Fran' in reg:
        reg_code = 'SV'
    elif 'East Coast' in reg:
        reg_code = 'EC'
    else:
        reg_code = 'Neither'
    return reg_code

def create_al_fund_tag(name):
    """
    Creates a string url that can be used to search Angellist to gather information

    Args:
    name (string): name given by Crunchbase

    Returns:
    al_tag (string): Angellist string url to search as a potential match for a venture capital firm.
    """
    al_tag = 'https://angel.co/company/'+"-".join(name.split(' '))+'/funding'
    al_tag = unidecode.unidecode(al_tag)
    return al_tag

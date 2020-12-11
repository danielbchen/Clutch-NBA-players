from bs4 import BeautifulSoup
import numpy as np
import operator
import os
import pandas as pd
import requests


def clutch_stats_retriever():
    '''
    Scrapes website to return a dataframe containing data on a player's clutch
    statistics. 
    '''

    link = 'http://stats.inpredictable.com/nba/ssnPlayerSplit.php?season=2019&pos=ALL&team=ALL&po=0&frdt=2018-10-16&todt=2019-06-13&shot=both&dst=plyr'

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')

    raw_text = soup.find_all('td')
    data_values = [item.get_text() for item in raw_text]
    data_values = data_values[9:]

    starting_indexes = [number for number in range(0, 17)]
    nested_data = [column_getter(index) for index in starting_indexes]

    df = pd.DataFrame(nested_data)
    df = df.transpose()
    df.columns = [
        'Rank',
        'Player',
        'Position',
        'Team',
        'Games',
        'Garbage',
        'Normal',
        'Clutch',
        'Clutch_Sq',
        'Garbage_Percent',
        'Normal_Percent',
        'Clutch_Percent',
        'Clutch_Percent_Sq',
        'Garbage_EFG',
        'Normal_EFG',
        'Clutch_EFG',
        'Clutch_Sq_EFG'
    ]

    return df


def index_retriever(offset):
    '''
    '''

    indexes_to_drop = []
    for index, value in enumerate(data_values):
        if value == 'League Benchmarks:':
            indexes_to_drop.append(index + offset)

    return indexes_to_drop


def column_getter(index):
    '''
    Returns a list of values based on index location. 
    '''

    values = data_values[index::17]
    
    return values


years = [str(year) for year in range(1996, 2020)]
base_link = 'http://stats.inpredictable.com/nba/ssnPlayerSplit.php?season={}'

data_values = []
for year in years:
    response = requests.get(base_link.format(year))
    soup = BeautifulSoup(response.text, 'lxml')
    raw_text = soup.find_all('td')

    for text in raw_text:
        contents = text.get_text()
        data_values.append(contents)

indexes_to_drop = [index_retriever(number) for number in range(1, 9)]
indexes_to_drop = [item for sublist in indexes_to_drop for item in sublist]
data_values = np.delete(data_values, indexes_to_drop)







df = pd.DataFrame(data_values)















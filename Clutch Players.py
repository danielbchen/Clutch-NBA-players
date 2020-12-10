from bs4 import BeautifulSoup
import numpy as np
import os
import pandas as pd
import requests


link = 'http://stats.inpredictable.com/nba/ssnPlayerSplit.php?season=2019&pos=ALL&team=ALL&po=0&frdt=2018-10-16&todt=2019-06-13&shot=both&dst=plyr'

response = requests.get(link)
soup = BeautifulSoup(response.text, 'lxml')
raw_text = soup.find_all('td')
data_values = [item.get_text() for item in raw_text]
data_values = data_values[9:]

starting_indexes = [number for number in range(0, 17)]

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


def column_getter(index):
    '''
    '''

    values = data_values[index::17]
    
    return values

nested_data = [column_getter(index) for index in starting_indexes]

nested_data[0]

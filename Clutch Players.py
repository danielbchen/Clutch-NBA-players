from bs4 import BeautifulSoup
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import operator
import os
import pandas as pd
import requests


def clutch_stats_retriever():
    '''
    Loops through webpages on inpredictable.com, scrapes data, and returns a
    dataframe.
    '''

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

    indexes_to_drop = [index_retriever(data_values, number) for number in range(0, 9)]
    indexes_to_drop = [item for sublist in indexes_to_drop for item in sublist]
    data_values = np.delete(data_values, indexes_to_drop)

    nested_data = [column_getter(data_values, index) for index in range(0, 17)]
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

    columns = [column for column in df.loc[:, 'Garbage_Percent':]]
    df[columns] = df[columns].replace('\%', '', regex=True)

    non_numeric_cols = ['Player', 'Position', 'Team']
    numeric_cols = [column for column in df.columns.values if column not in non_numeric_cols]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

    yrs = [[year] * 50 for year in years]
    yrs = [year for sublist in yrs for year in sublist]
    df['Year'] = yrs

    return df


def index_retriever(list_object, offset):
    '''
    '''

    indexes_to_drop = []
    for index, value in enumerate(list_object):
        if value == 'League Benchmarks:':
            indexes_to_drop.append(index + offset)

    return indexes_to_drop


def column_getter(list_object, index):
    '''
    Returns a list of values based on index location. 
    '''

    values = list_object[index::17]

    return values


df = clutch_stats_retriever()


def plotter():
    '''
    Plots number of clutch shots taken against clutch EFG.
    '''

    df = clutch_stats_retriever()
    aggregations = {
        'Clutch': 'sum',
        'Clutch_EFG': 'mean',
    }
    df = df.groupby('Player').agg(aggregations).reset_index()

    conditions = [
        df['Player'] == 'LeBron James',
        df['Player'] == 'Kobe Bryant',
        df['Player'] == 'Kevin Durant',
        df['Player'] == 'Stephen Curry',
        df['Player'] == 'Michael Jordan',
        df['Player'] == 'Kyrie Irving',
        df['Player'] == 'Dirk Nowitzki',
        df['Player'] == 'Paul Pierce',
        ((df['Player'] != 'LeBron James') & 
         (df['Player'] != 'Kobe Bryant') &
         (df['Player'] != 'Kevin Durant') &
         (df['Player'] != 'Stephen Curry') &
         (df['Player'] != 'Michael Jordan') &
         (df['Player'] != 'Kyrie Irving') &
         (df['Player'] != 'Dirk Nowitzki') &
         (df['Player'] != 'Paul Pierce'))
    ]
    colors = [
        '#FFD300', 
        '#552583', 
        '#000000',
        '#006bb6',
        '#ce1141',
        '#24A0ED',
        '#00285e',
        '#008348',
        '#A9A9A9'
    ]
    df['Group'] = np.select(conditions, colors)

    m, b = np.polyfit(df['Clutch'], df['Clutch_EFG'], 1)

    fig, ax = plt.subplots(figsize=(10,10))
    
    plt.rcParams['font.family'] = 'arial'

    ax.scatter(x=df['Clutch'], y=df['Clutch_EFG'], color=df['Group'])
    ax.plot(df['Clutch'], m * df['Clutch'] + b, color='red', linestyle=':')

    ax.text(2200, 50.2, 'LeBron James')
    ax.text(2340, 43, 'Kobe Bryant')
    ax.text(1254, 49, 'Kevin Durant')
    ax.text(639, 55.2, 'Stephen Curry')
    ax.text(706, 52.8, 'Kyrie Irving')
    ax.text(1837, 51.5, 'Dirk Nowitzki')
    ax.text(1759, 46.2, 'Paul Pierce')

    ax.set_xlabel('Number of Clutch Shots Taken')
    ax.set_ylabel('Clutch EFG%')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()

    
df[df['Clutch'] > 1700]











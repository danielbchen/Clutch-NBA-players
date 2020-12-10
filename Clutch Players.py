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


data = {
    'Rank': data_values[0::17],
    ''
}



data_values[1::17]
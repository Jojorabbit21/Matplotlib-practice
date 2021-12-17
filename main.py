import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from dock import *

# Matplotlib Tutorial
# https://wikidocs.net/book/5011

# DPOY Prediction

path = './Data/'
pBase = pd.read_csv(path + 'player_Base.csv')
pBase = pBase.iloc[:, :28]
pBase.drop(['Unnamed: 0', 'PLAYER_ID', 'NICKNAME', 'TEAM_ID'], axis=1, inplace=True)

data = pBase[['PLAYER_NAME','BLK','STL']]
data = data.sort_values(['BLK','STL'],ascending=[False,False])
data = data[(data['BLK'] > 0) & (data['STL'] > 0)]
data.reset_index(drop=True, inplace=True)

plt.scatter(data['BLK'], data['STL'], s=10, c='coral')
plt.xlabel('Blocks per game')
plt.ylabel('Steals per game')

for i in range(0, 4):
  plt.annotate(data.loc[i, 'PLAYER_NAME'], (data.loc[i,'BLK'], data.loc[i,'STL'] + 0.1))

plt.show()
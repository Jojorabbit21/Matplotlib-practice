import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from dock import *

path = './Data/whoisbestshooter/'
curry_total = pd.read_csv(path+'curry.csv')
allen_total = pd.read_csv(path+'allen.csv')
miller_total = pd.read_csv(path+'miller.csv')
seasons_num = [len(curry_total), len(allen_total), len(miller_total)]
season = max(seasons_num)

pd.set_option('max_column', 20)

# 3P, 3P% 

index = ['S. Curry', 'R. Allen', 'R. Miller']
column = []
# data = []
# for a in range(3):
#   line = []
#   for b in range(season):
#     line.append(0)
#   data.append(line)
  
for i in range(13):
  column.append('S{}'.format(i+1)) 
#   try:
#     data[0][i] = curry_total.at[i,'3P%']
#   except: pass
#   try:
#     data[1][i] = allen_total.at[i,'3P%']
#   except: pass
#   try:
#     data[2][i] = miller_total.at[i,'3P%']
#   except: pass

# vmax = max(max(data))

# cmap = plt.get_cmap('Greens')
# sns.heatmap(data, annot=True, fmt='f', cmap=cmap, square=True, cbar=False, vmin=0.2, vmax=vmax)
# plt.title('3 Points Percent in Every Seasons')
# plt.yticks(np.arange(0,len(index)), labels=index)
# plt.xticks(np.arange(0,season), np.arange(1, season+1))
# plt.show()

# 3P/2P%

# True Shooting Percentage Formula
# -> PTS/(2*(FGA+0.44*FTA))

curry_3p = curry_total.loc[:13, '3P']
curry_2p = curry_total.loc[:13, '2P']
allen_3p = allen_total.loc[:12, '3P']
allen_2p = allen_total.loc[:13, '2P']
miller_3p = miller_total.loc[:12, '3P']
miller_2p = miller_total.loc[:13, '2P']

# fig = plt.figure(figsize=(len(column),len(curry_3p)))
# fig.set_facecolor('white')
# ax = fig.add_subplot()

# ax.plot(column, curry_3p, color='black', linestyle='--')
# plt.show()

bbox = dict( ## 텍스트 박스 스타일 지정
    boxstyle='square', # 박스 모양
    facecolor='white', # 박스 배경색
)

cplt = plt.plot(column, curry_3p, 'o-', label=index[0])
cplt_coord = cplt[0]
for coord in list(cplt_coord.get_xydata()):
  plt.text(coord[0], coord[1]+10, f"{int(coord[1])}", fontsize=10, ha='center', bbox=bbox)
aplt = plt.plot(column, allen_3p, 's--', label=index[1])
aplt_coord = aplt[0]
for coord in list(aplt_coord.get_xydata()):
  plt.text(coord[0], coord[1]+10, f"{int(coord[1])}", fontsize=10, ha='center', bbox=bbox)
mplt = plt.plot(column, miller_3p, 's-.', label=index[2])
mplt_coord = mplt[0]
for coord in list(mplt_coord.get_xydata()):
  plt.text(coord[0], coord[1]+10, f"{int(coord[1])}", fontsize=10, ha='center', bbox=bbox)
plt.xlabel('Seasons')
plt.ylabel('3-Pts-Made')
plt.legend()
plt.grid(True, linestyle='--')
plt.show()
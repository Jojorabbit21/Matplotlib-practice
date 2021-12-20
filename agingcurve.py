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

# Aging Curve Trajectory
# X = S1..S*
# Y = 3P, 3P%

index = ['S. Curry', 'R. Allen', 'R. Miller']
column = []
data = []
for a in range(3):
  line = []
  for b in range(season):
    line.append(0)
  data.append(line)

for i in range(season):
  column.append('S{}'.format(i+1)) 
  try:
    data[0][i] = curry_total.at[i,'3P%']
  except: pass
  try:
    data[1][i] = allen_total.at[i,'3P%']
  except: pass
  try:
    data[2][i] = miller_total.at[i,'3P%']
  except: pass
  
for li in range(3):
  for i in range(len(data[li])):
    try:
      if data[li][i] == 0:
        data[li].remove(0)
    except:
      pass
     
print(data) 
  
plt.plot(column, data[0])
plt.plot(column, data[1])
plt.plot(column, data[2])
plt.show()  



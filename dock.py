import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json as js
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# leaguedashteamstats => Team Stats
# leaguedashplayerstats => Player Stats

team_url = 'https://stats.nba.com/stats/leaguedashteamstats?' \
           'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' \
           'GameSegment=&LastNGames=0&LeagueID=00&Location=&' \
           'MeasureType={}&Month=0&OpponentTeamID=0&Outcome=&' \
           'PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' \
           'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' \
           'Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
           'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='
           
player_url = 'https://stats.nba.com/stats/leaguedashplayerstats?' \
            'College=&Conference=&Country=&DateFrom=&DateTo=&Division=&'\
            'DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&'\
            'LeagueID=00&Location=&MeasureType={}&Month=0&OpponentTeamID=0&'\
            'Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&'\
            'PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&'\
            'SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&'\
            'TwoWay=0&VsConference=&VsDivision=&Weight='
            
player_opp_url = 'https://stats.nba.com/stats/leagueplayerondetails?'\
            'College=&Conference=&Country=&DateFrom=&DateTo=&Division=&'\
            'DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&'\
            'LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&'\
            'Outcome=&PORound=0&PaceAdjust=N&PerMode=Per100Possessions&Period=0&PlayerExperience=&'\
            'PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&'\
            'ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='

MEASURE_TYPE = [
  'Base', 'Advanced', 'Misc', 'Scoring', 'Opponent', 'Defense'
]

            
player_def_url = 'https://stats.nba.com/stats/leaguedashptdefend?'\
                'College=&Conference=&Country=&DateFrom=&DateTo=&'\
                'DefenseCategory={}&Division=&DraftPick=&'\
                'DraftYear=&GameSegment=&Height=&LastNGames=0&'\
                'LeagueID=00&Location=&Month=0&OpponentTeamID=0&'\
                'Outcome=&PORound=0&PerMode=PerGame&Period=0&'\
                'PlayerExperience=&PlayerPosition=&Season=2021-22&'\
                'SeasonSegment=&SeasonType=Regular+Season&StarterBench=&'\
                'TeamID=0&VsConference=&VsDivision=&Weight='

DEFENSE_CATEGORY = [
  'Overall', '3+Pointers', '2+Pointers', 'Less+Than+6Ft', 'Less+Than+10Ft', 'Greater+Than+15Ft'
]

player_hustle_url = 'https://stats.nba.com/stats/leaguehustlestatsplayer?'\
                  'College=&Conference=&Country=&DateFrom=&DateTo=&Division=&'\
                  'DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&'\
                  'LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&'\
                  'PORound=0&PaceAdjust=N&PerMode=PerGame&PlayerExperience=&'\
                  'PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&'\
                  'SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&Weight='

games_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Dnt': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en',
    'origin': 'http://stats.nba.com',
    'Referer': 'https://github.com'
}

data_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1&Season=2019-20&SeasonType=Regular%20Season',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}

def get_stat(type=['team','player','playerdefense','playerhustle'], param=None):
  if type == 'team':
    if param != None:
      if param in MEASURE_TYPE:
        url = team_url.format(param)
      else:
        url = team_url.format(MEASURE_TYPE[0])
    else:
      url = team_url.format(MEASURE_TYPE[0])
  elif type == 'player':
    if param != None:
      if param == 'Opponent':
        url = player_opp_url
      else:
        if param in MEASURE_TYPE:
          url = player_url.format(param)
        else:
          url = player_url.format(MEASURE_TYPE[0])
    else:
      url = player_url.format(MEASURE_TYPE[0])
  elif type == 'playerdefense':
    if param != None:
      if param in DEFENSE_CATEGORY:
        url = player_def_url.format(param)
      else:
        url = player_def_url.format(DEFENSE_CATEGORY[0])
    else:
      url = player_url.format(DEFENSE_CATEGORY[0])
  elif type == 'playerhustle':
    url = player_hustle_url
  raw = get_json_data(url)
  df = to_data_frame(raw)
  filepath = './Data/{}.csv'.format(type+'_'+param)
  df.to_csv(filepath, mode='w')
  return df

def get_json_data(url):
    raw_data = requests.get(url, headers=data_headers)
    json = raw_data.json()
    with open('jr.json', 'w') as file:
      js.dump(json, file)
    return json.get('resultSets')
  
def to_data_frame(data):
    data_list = data[0]
    return pd.DataFrame(data=data_list.get('rowSet'), columns=data_list.get('headers'))

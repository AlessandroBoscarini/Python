#%%
#first thing first: import the main libraries!
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.cm import get_cmap
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import plotly.express as px
import pyautogui
import plotly.graph_objects as go
#%%
st.title("Milan")
# %%
seriea_df = pd.read_excel("C:/Users/ASUS/Desktop/serieA.xlsx")
seriea = seriea_df.drop(['time','comp','round','day','attendance', 'captain', 'dist', 'fk', 'pk', 'pkatt', 'poss_y', 'touches', 'def pen', 'mid 3rd', 'att pen', 'live', 'succ', 'att', '#pl', 'megs', 'carries', 'totdist', 'prgdist', 'prog', 'prog.1', '01-mar', 'cpa', 'dis', 'targ', 'rec'], axis = 1)
date_sorted = seriea.sort_values(by=['date'])
# %%
date_sorted['date'] = pd.to_datetime(date_sorted['date'], format='%Y %B, %d')
date_sorted['year'] = date_sorted['date'].dt.year
date_sorted["year"] = date_sorted["year"].astype(str)

# %%
def teams(arr, l):
  for element in arr:
    if element not in l:
      l.append(element)
  return l

a = date_sorted['team']
list_of_teams = []
teams(a, list_of_teams)
# %%
def win_by_year(l_teams, new_l_team, new_l_year, l_years, l_wins):
  for x in l_teams:
    for y in l_years:
      df = date_sorted[date_sorted['year']==y] #element
      dff = df[df['team']==x]
      if len(dff['result'].value_counts()) > 0:
        wins = dff['result'].value_counts()['W']
        l_wins.append(wins)
      else:
        l_wins.append(0)
      new_l_team.append(x)
      new_l_year.append(y)
        
      
      
  print(l_wins)
  print(new_l_year)
  print(new_l_team)


list_of_years = ['2017','2018','2019','2020','2021','2022']
list_of_wins = []
new_year = []
new_team = []
win_by_year(list_of_teams, new_team, new_year, list_of_years, list_of_wins)
# %%
seriea_df = pd.DataFrame(
  {
    'year':new_year,
    'Team':new_team,
    'wins':list_of_wins
  }
)
# %%
seriea_opt = seriea_df['Team'].unique().tolist()
team = st.multiselect("Which team would you like to see?", seriea_opt, ['Milan'])
seriea_df = seriea_df[seriea_df['Team'].isin(team)]
textauto = True
fig = px.bar(seriea_df, x='Team', y='wins', color = 'Team', color_discrete_map = {
  'Juventus':'black', 
  'Napoli':'deepskyblue',
  'Internazionale':'Blue',
  'Milan':'red',
  'Lazio':'lightskyblue',
  'Roma':'orange',
  'Atalanta':'navy',
  'Sampdoria':'dodgerblue',
  'Sassuolo':'darkgreen',
  'Fiorentina':'darkviolet',
  'Torino':'saddlebrown',
  'Udinese':'lightgray',
  'Bologna':'darkred',
  'Cagliari':'crimson',
  'Hellas Verona':'yellow',
  'Genoa':'firebrick',
  'Parma':'khaki',
  'SPAL':'skyblue',
  'Empoli':'cornflowerblue',
  'Spezia':'gray',
  'Crotone':'indianred',
  'Benevento':'darkorange',
  'Chievo':'lemonchiffon',
  'Lecce':'navajowhite',
  'Salernitana':'brown',
  'Brescia':'aliceblue',
  'Venezia':'forestgreen',
  'Frosinone':'darkkhaki'}, text_auto=textauto, animation_frame='year', animation_group='Team')
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig.update_yaxes(range=[0, 35])
st.write(fig)

# %%

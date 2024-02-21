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
  'Juventus':'white', 
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
df_mi_ju = date_sorted[(date_sorted['team']=='Milan') | (date_sorted['team']=='Juventus')]
# %%
def win_by_year(l_teams, new_l_team, new_l_year, l_years, l_wins):
  for x in l_teams:
    for y in l_years:
      df = date_sorted[date_sorted['year']==y] #element
      dff = df[df['team']==x]
      wins = dff['result'].value_counts()['W']
      l_wins.append(wins)
      new_l_team.append(x)
      new_l_year.append(y)
  print(l_wins, new_l_team, new_l_year)

list_of_teams_2 = ['Milan','Juventus']
list_of_years = ['2017','2018','2019','2020','2021','2022']
list_of_wins = []
new_team = []
new_year = []
win_by_year(list_of_teams_2, new_team, new_year, list_of_years, list_of_wins)
# %%
df = pd.DataFrame(
  {
    'year':new_year,
    'Team':new_team,
    'wins':list_of_wins
  }
)

# %%
textauto = True
fig = px.bar(df, x="year", y="wins", title = "Victories by Milan and Juventus from 2017 to 2022", barmode='group', text_auto=textauto, color = 'Team', color_discrete_map={'Milan':'red', 'Juventus':'white'})
fig.add_trace(go.Scatter(x=df['year'], y=df['wins'][0:6], line=dict(color='gold', width=4, dash='dot'), name='Milan_trace'))
st.write(fig)

# %%
milan = seriea[seriea['team']=='Milan']
# %%
cols = ['ga', 'poss_x', 'sot', 'def 3rd', 'att 3rd', 'succ%', 'mis', 'rec%' ]
x = milan[cols]
y = milan['result']

X_train_milan, X_test_milan, y_train_milan, y_test_milan = sklearn.model_selection.train_test_split(x, y, test_size = 0.25, random_state = 5)
print(X_train_milan.shape)
print(X_test_milan.shape)
print(y_train_milan.shape)
print(y_test_milan.shape)
# %%
fig, ax = plt.subplots(figsize=(10,6))
logit_model_1=sm.MNLogit(y_train_milan, sm.add_constant(X_train_milan))
result_1=logit_model_1.fit()
# %%
cols = ['ga', 'poss_x', 'sot', 'att 3rd', 'succ%']
x = seriea[cols]
y = seriea['result']
X_train_seriea, X_test_seriea, y_train_seriea, y_test_seriea = sklearn.model_selection.train_test_split(x, y, test_size = 0.25, random_state = 5)
logit_model_2=sm.MNLogit(y_train_seriea, sm.add_constant(X_train_seriea))
result_2=logit_model_2.fit() 
# %%
cols = ['ga', 'sot', 'att 3rd', 'succ%']
x = seriea[cols]
y = seriea['result']
X_train_seriea, X_test_seriea, y_train_seriea, y_test_seriea = sklearn.model_selection.train_test_split(x, y, test_size = 0.25, random_state = 5)
logit_model=sm.MNLogit(y_train_seriea, sm.add_constant(X_train_seriea))
result_3=logit_model.fit() 
# %%
col1, col2, col3 = st.columns(3)

with col1:
   button_1 = st.sidebar.button('First Model')

with col2:
  button_2 = st.sidebar.button('Second Model')

with col3:
  button_3 = st.sidebar.button('Final Model')
# %%
if button_1:
  st.header("Milan First Model")
  st.write(result_1.summary())
if button_2:
    st.header("Milan Second Model")
    st.write(result_2.summary())
if button_3:
    st.header("Milan Final Model")
    st.write(result_3.summary())

st.sidebar.button('Reset')
if button_1 == True:
  button_1 = False
elif button_2 == True:
  button_2 = False
elif button_3 == True:
  button_3 = False

# %%
milan_sorted = milan.sort_values(by=['date'])
# %%
milan_sorted['date'] = pd.to_datetime(milan_sorted['date'], format='%Y %B, %d')
milan_sorted['year'] = milan_sorted['date'].dt.year
milan_sorted["year"] = milan_sorted["year"].astype(str)  

# %%
milan_sorted = milan_sorted[['year', 'result', 'opponent', 'team']]
milan_sorted = milan_sorted[milan_sorted['result']=='L']
len(milan_sorted)

# %%
# %%
def teams_2(arr, l):
  for element in arr:
    if element not in l:
      l.append(element)
  return l

a = milan_sorted['opponent']
list_of_teams_3 = []
teams_2(a, list_of_teams_3)
# %%
def lose_by_year(l_opponents, l_years, l_lose, n_y, n_oppo):
  for x in l_opponents:
    for y in l_years:
      df = milan_sorted[milan_sorted['year']==y]           
      dff = df[df['opponent']==x]
      if len(dff['result'].value_counts()) <= 0:
        l_lose.append(0)  
      else:
        lose = dff['result'].value_counts()['L'] 
        l_lose.append(lose)       
      n_y.append(y)
      n_oppo.append(x)
  print(l_lose)
  print(n_y)
  print(n_oppo)
list_of_years = ['2017','2018','2019','2020','2021','2022']
list_of_lose = []
new_year = []
new_team = []
lose_by_year(list_of_teams_3, list_of_years, list_of_lose, new_year, new_team)

# %%
df_2 = pd.DataFrame({
  'year': new_year,
  'Team': new_team,
  'Losses': list_of_lose
})

# %%
df_2['Los'] = df_2.groupby(['Team'])['Losses'].cumsum()
# %%
textauto = True
fig_3 = px.bar(df_2, x='Team', y='Los', color = 'Team', title = 'Cumulative Losses from 2017 to 2022', color_discrete_map = {
  'Juventus':'white', 
  'Napoli':'deepskyblue',
  'Inter':'blue',
  'Lazio':'lightskyblue',
  'Roma':'orange',
  'Atalanta':'navy',
  'Sampdoria':'dodgerblue',
  'Sassuolo':'darkgreen',
  'Fiorentina':'darkviolet',
  'Torino':'saddlebrown',
  'Udinese':'lightgray',
  'Hellas Verona':'yellow',
  'Genoa':'firebrick',
  'Spezia':'gray',
  'Benevento':'darkorange'}, text_auto=textauto, animation_frame='year', animation_group='Team')
fig_3.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 4000
fig_3.update_yaxes(range=[0, 8])
fig_3.update_layout(xaxis={'categoryorder':'total descending'})
st.write(fig_3)
# %%
df = seriea[(seriea['team']=='Milan') | (seriea['team']=='Juventus')]
dff = df[(df['opponent']=='Juventus') | (df['opponent']=='Milan')]
df2 = dff.drop(dff[dff['result']=="D"].index)
df3 = df2.drop([832, 908, 1512, 1702])
# %%
def fun(list_var, l_teams, l, new_var):
  for x in l_teams:
    for y in list_var:
      print(x)
      if y == 'succ%' or y == 'poss_x':
        df = df3[df3['team']==x]
        m = df[y].mean()
        l.append(m)
        new_var.append(y)
      else:
        df = df3[df3['team']==x]
        s = sum(df[y])
        l.append(s)
        new_var.append(y)    


  print(l)
  print(new_var)

new_var = []
total = []
l_var = ['sot', 'att 3rd', 'xg', 'xga', 'poss_x']
l_teams = ['Milan','Juventus']
fun(l_var, l_teams, total, new_var)
# %%
vari = new_var[0:5]
opt_df = pd.DataFrame({
  'variables':vari,
  'Milan':total[0:5],
  'Juventus':total[5:11]
})
# %%
st.header("Milan-Juventus: focus on the variables")
variable = st.multiselect("Which variable would you like to see?", vari, ['sot'])
new_opt = opt_df[opt_df['variables'].isin(variable)]
textauto = True
fig = px.bar(new_opt, x='variable', y=['Milan','Juventus'], color_discrete_map = { 
  'Juventus':'white',
  'Milan':'red'}, text_auto=textauto)
fig.update_layout(xaxis_title="Teams", legend_title="Teams")
st.write(fig)

# %%

# %%
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
# %%
st.markdown("<h1 style='text-align: center; color: black;'>Final Project</h1>", unsafe_allow_html=True)
seriea_df = pd.read_excel("C:/Users/ASUS/Desktop/serieA.xlsx")
seriea_df.info()
seriea_df.describe()
st.text(" ")
#we can see that there are two columns with null values: attendance and dist, so before proceeding with the analysis we decide how to treat them.
#If we decide to use them we would need to figure out how to replace the null values,
#if on the other hand we consider these variables to be useless for our objective then we can decide simply to eliminate them
#attendance: is the total attendance in the stadium and for our goal it's useless
#dist: is the average distance of the team and even in this case we decide to remove it

# %%
seriea_noatt_nodist = seriea_df.drop(['attendance', 'dist'], axis = 1)
seriea_noatt_nodist.info()
#at this point we clean up the dataset a bit from the variables that we are not interested in

# %%
seriea = seriea_df.drop(['time','comp','round','day','attendance', 'captain', 'dist', 'fk', 'pk', 'pkatt', 'poss_y', 'touches', 'def pen', 'mid 3rd', 'att pen', 'live', 'succ', 'att', '#pl', 'megs', 'carries', 'totdist', 'prgdist', 'prog', 'prog.1', '01-mar', 'cpa', 'dis', 'targ', 'rec'], axis = 1)
seriea.info()
#The goal of our project is to find the variables that most influence winning.
#To begin, however, let us take a closer look at wins, draws and losses

# %%
def take_results(arr, l):
    for element in arr:
        l.append(element)
    return l

arr = seriea['result'].value_counts(ascending=False)
list_of_results = []
list_of_string_results = ['w', 'L', 'D']
take_results(arr, list_of_results)

# %%
fig , ax = plt.subplots(figsize=(15,10))
colors = ['gold','silver','peru']
x = list_of_string_results
y = list_of_results
plt.bar(x, y, color = colors)
plt.bar_label(plt.bar(x, y, color = colors), labels = y, padding = 1)
plt.xlabel('result')
plt.ylabel('count')
plt.title('Total Win, Lose and Draw')
plt.show()
st.write(fig)
#%%
def win(l_teams, l_wins):
  for element in l_teams:
    df_1 = seriea[seriea['result']=="W"]
    new_df = df_1[df_1['team']==element]
    wins = new_df['result'].value_counts()['W']
    l_wins.append(wins)
    print(str(element) + " ha vinto: " + str(wins) + " partite")

list_of_teams = ['Atalanta','Benevento','Bologna','Brescia','Cagliari','Chievo','Crotone','Empoli','Fiorentina','Frosinone','Genoa','Hellas Verona','Internazionale','Juventus','Lazio','Lecce','Milan','Napoli','Parma','Roma','Salernitana','Sampdoria','Sassuolo','SPAL','Spezia','Torino','Udinese','Venezia']
list_of_wins = []
win(list_of_teams, list_of_wins)
# %%
def list_abbr(l_teams, l):
  for element in l_teams:
    l.append(element[0:3])
list_of_3 = []
list_abbr(list_of_teams, list_of_3)
print(list_of_3)
# %%
lists = [list_of_teams, list_of_wins, list_of_3]
win_df = pd.concat([pd.Series(x) for x in lists], axis=1)
# %%
win_df.columns = ['team','wins', 'team3']
win_df_sorted = win_df.sort_values(by=['wins'], ascending=False)
# %%
fig, ax = plt.subplots(figsize=(15,7))
x = win_df_sorted['team3']
y = win_df_sorted['wins']
my_cmap = plt.get_cmap("plasma")
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
plt.axhline(y.mean(), color='red', linestyle='--', linewidth=1, label='Avg')
plt.bar(x, y, color=my_cmap(rescale(y)))
plt.bar_label(plt.bar(x, y, color=my_cmap(rescale(y))), labels=y, label_type='edge', padding=1)
plt.title('Victories by team')
plt.xlabel('teams')
plt.ylabel('wins')
plt.legend()
plt.show()
st.write(fig)

# %%
st.markdown("<h2 style='text-align: center; color: black;'>Model</h2>", unsafe_allow_html=True)
cols = ['ga', 'poss_x', 'sot', 'def 3rd', 'att 3rd', 'succ%', 'mis', 'rec%' ]
x = seriea[cols]
y = seriea['result']

X_train_seriea, X_test_seriea, y_train_seriea, y_test_seriea = sklearn.model_selection.train_test_split(x, y, test_size = 0.25, random_state = 5)
print(X_train_seriea.shape)
print(X_test_seriea.shape)
print(y_train_seriea.shape)
print(y_test_seriea.shape)
# %%
fig, ax = plt.subplots(figsize=(10,6))
logit_model_1=sm.MNLogit(y_train_seriea, sm.add_constant(X_train_seriea))
result_1=logit_model_1.fit()
# %%
#Let's check what variables are not significative...
#we see that poss_x and mis are not significative in both lose and win case so we remove it
cols = ['ga','sot', 'def 3rd', 'att 3rd', 'succ%', 'rec%' ]
x = seriea[cols]
y = seriea['result']
X_train_seriea, X_test_seriea, y_train_seriea, y_test_seriea = sklearn.model_selection.train_test_split(x, y, test_size = 0.25, random_state = 5)
logit_model_2=sm.MNLogit(y_train_seriea, sm.add_constant(X_train_seriea))
result_2=logit_model_2.fit()
# %%
#we see that def 3rd is not significative and we remove it
cols = ['ga', 'sot', 'att 3rd', 'succ%', 'rec%' ]
x = seriea[cols]
y = seriea['result']
X_train_seriea, X_test_seriea, y_train_seriea, y_test_seriea = sklearn.model_selection.train_test_split(x, y, test_size = 0.25, random_state = 5)
logit_model=sm.MNLogit(y_train_seriea, sm.add_constant(X_train_seriea))
result_3=logit_model.fit()


# %%
col1, col2, col3 = st.columns(3)

with col1:
   button_1 = st.button('Full Model')

with col2:
  button_2 = st.button('Second Model')

with col3:
  button_3 = st.button('Final Model')
# %%
if button_1:
  st.write(result_1.summary())
if button_2:
    st.write(result_2.summary())
if button_3:
    st.write(result_3.summary())
 
st.button('Reset')
if button_1 == True:
  button_1 = False
elif button_2 == True:
  button_2 = False
elif button_3 == True:
  button_3 = False

# %%
def sum_gf(list_of_variables, col_y):
  for element in list_of_variables:
    new_seriea = seriea[seriea['team']==element]
    col_y.append(round(sum(new_seriea['gf'])))
  print(col_y)
list_of_gf = []
sum_gf(list_of_teams, list_of_gf)

def sum_xg(list_of_variables, col_y):
  for element in list_of_variables:
    new_seriea = seriea[seriea['team']==element]
    col_y.append(round(sum(new_seriea['xg'])))
  print(col_y)
list_of_xg = []
sum_xg(list_of_teams, list_of_xg)

def sum_ga(list_of_variables, col_y):
  for element in list_of_variables:
    new_seriea = seriea[seriea['team']==element]
    col_y.append(round(sum(new_seriea['ga'])))
  print(col_y)
list_of_ga = []
sum_ga(list_of_teams, list_of_ga)

def sum_xga(list_of_variables, col_y):
  for element in list_of_variables:
    new_seriea = seriea[seriea['team']==element]
    col_y.append(round(sum(new_seriea['xga'])))
  print(col_y)
list_of_xga = []
sum_xga(list_of_teams, list_of_xga)
# %%
data = {
    'team': list_of_teams,
    'gf': list_of_gf,
    'xg': list_of_xg,
    'ga': list_of_ga,
    'xga': list_of_xga
}
df = pd.DataFrame(data)
# %%
list_of_var = ['gf','xg','ga','xga']

sel_team = st.selectbox('**Select team**', df.team)
fil_df = df[df.team == sel_team]  # filter

# Build a new df based from filter.
new_df = pd.melt(fil_df, id_vars=['team'], var_name="feature",
                 value_vars=['gf', 'xg', 'ga', 'xga'])

logy = True  # to make small values visible
textauto = True  # to write plot label
title = f'team name: {sel_team}'
fig = px.bar(new_df, x='feature', y='value',
             height=300, log_y=logy, text_auto=textauto,
             title=title)
with st.expander('Goals: Expectations Vs. Reality', expanded=True):
    st.plotly_chart(fig, use_container_width=True)
# %%

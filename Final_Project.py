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
# %%
st.title('Hello please work!')
seriea_df = pd.read_excel("C:/Users/ASUS/Desktop/serieA.xlsx")
seriea_df.info()
seriea_df.describe()
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
fig , ax = plt.subplots(figsize=(6,5))
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
juve_df = seriea[seriea['team']=='Juventus']
column_x = ['gf',	'ga',	'xg',	'xga',	'poss_x',	'sh',	'sot',	'def 3rd',	'att 3rd',	'succ%',	'mis',	'rec%']
column_y = []
def sum_col_juve(list_of_variables, col_y):
  for element in list_of_variables:
    col_y.append(round(sum(juve_df[element])))
  print(col_y)
sum_col_juve(column_x, column_y)

# %%
fig, ax = plt.subplots(figsize=(6,6))
x = column_x[0],column_x[2]
x_1 = column_x[1],column_x[3]
new_x = x + x_1
y = column_y[0],column_y[2]
y_1 = column_y[1],column_y[3]
new_y = y + y_1
my_cmap = plt.get_cmap("plasma")
plt.bar(new_x, new_y, color = ['navy','mediumblue','lightskyblue','cornflowerblue' ])
plt.bar_label(plt.bar(new_x, new_y, color = ['navy','mediumblue','lightskyblue','cornflowerblue' ]), labels=new_y, label_type='edge', padding=1)
plt.title('Juventus Goals: Expectations Vs. Reality')
plt.xlabel('statistics')
plt.ylabel('count')
plt.show()
st.write(fig)

# %%
st.header('Model')
cols = ['ga', 'poss_x', 'sot', 'def 3rd', 'att 3rd', 'succ%', 'mis', 'rec%' ]
x = seriea[cols]
y = seriea['result']

X_train_seriea, X_test_seriea, y_train_seriea, y_test_seriea = sklearn.model_selection.train_test_split(x, y, test_size = 0.25, random_state = 5)
print(X_train_seriea.shape)
print(X_test_seriea.shape)
print(y_train_seriea.shape)
print(y_test_seriea.shape)
# %%

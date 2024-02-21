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
st.markdown("<h1 style='text-align: center; color: white;'>Final Project</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
  from PIL import Image
  image = Image.open("C:/Users/ASUS/Desktop/pep.png")
  st.image(image, output_format="PNG")  

with col2:
  st.write(" ")
  st.write(" ")
  st.write(" ")
  st.write(" ")
  st.write(" ")
  st.write(" ")
  st.write(" ")
  st.write('*"Football is the only sport you can loose by playing better, that’s why it’s so attractive to people."* Joseph Guardiola')

col1, col2, col3 = st.columns(3)
with col1:
  st.markdown(
"""
**Following Guardiola's quote it is possible to say that:**
- there is a sort of randomness in the result
- score-determing events are rare if not absent
- in football it can be a single event that decides the outcome (1-0, a single action determines the result), in basketball there are about 100 baskets and in tennis hundreds of points
"""
)

with col2: 
  st.write(" ")
  st.write(" ")
  st.write(" ")
  st.write(" ")  
  button = st.button('Example')
with col3:
  if button:
    from PIL import Image
    image = Image.open("C:/Users/ASUS/Desktop/celticbarca.png")
    new_image = image.resize((1000, 800))
    st.image(new_image, output_format="PNG")
st.sidebar.success('Select a page')
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
button = st.button("So the question is ... ")
if button:
  st.write("**Are there any factors that are often present when there is a win?**")
seriea = seriea_df.drop(['time','comp','round','day','attendance', 'captain', 'dist', 'fk', 'pk', 'pkatt', 'poss_y', 'touches', 'def pen', 'mid 3rd', 'att pen', 'live', 'succ', 'att', '#pl', 'megs', 'carries', 'totdist', 'prgdist', 'prog', 'prog.1', '01-mar', 'cpa', 'dis', 'targ', 'rec'], axis = 1)
seriea.info()
st.header("The Dataset")
seriea
#The goal of our project is to find the variables that most influence winning.
#To begin, however, let us take a closer look at wins, draws and losses

# %%
def take_results(arr, l):
    for element in arr:
        l.append(element)
    return l

arr = seriea['result'].value_counts(ascending=False)
list_of_results = []
list_of_string_results = ['W', 'L', 'D']
take_results(arr, list_of_results)

# %%
data = {
  'result': list_of_string_results,
  'count': list_of_results
}
df = pd.DataFrame(data)
# %%
textauto = True
logy = True
fig = px.bar(df, x = 'result', y = 'count', title = 'Total Wins, Losses and Draws', log_y=logy, color = 'result' , color_discrete_sequence=["gold", "silver", "peru"] ,text_auto=textauto)
st.header("Exploring the dataset")
st.write(fig)
# %%
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
textauto = True
dff = win_df_sorted[['team3', 'wins']].copy()
data_2 = dff.rename(columns={"team3": "teams", "wins": "victories"})
#colors = ['black','deepskyblue', 'mediumblue', 'red', 'lightskyblue', 'darkorange','navy','dodgerblue','green','blueviolet','maroon','dimgrey','crimson','orangered','yellow','firebrick','gold','royalblue','cornflowerblue','black','crimson','orange','yellow','chocolate','sienna','mediumblue','darkgreen','khaki']
fig_2 = px.bar(data_2, x = 'teams', y = 'victories', title = 'Victories by team', text_auto=textauto, color = 'victories', color_continuous_scale=px.colors.sequential.Plasma)
fig_2.add_hline(data_2['victories'].mean(), line_width=1.5, line_dash="dot", line_color="red")
st.write(fig_2)
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
st.header('Goals: Expectations Vs. Reality')
list_of_var = ['gf','xg','ga','xga']
sel_team = st.selectbox('**Select team**', df.team)
n_df = df[df.team == sel_team]  # filter

# Build a new df based from filter.
new_df = pd.melt(n_df, id_vars=['team'], var_name="feature",
                 value_vars=['gf', 'xg', 'ga', 'xga'])

logy = True  # to make small values visible
textauto = True  # to write plot label
title = f'team name: {sel_team}'
colors = ['darkblue']
fig = px.bar(new_df, x='feature', y='value',
             height=300, log_y=logy, text_auto=textauto,
             title=title, color = 'team',color_discrete_map = {
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
  'Frosinone':'darkkhaki'})
fig.update_layout(showlegend=False)
with st.expander('', expanded=True):
    st.plotly_chart(fig, use_container_width=True)



# %%

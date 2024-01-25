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
#%%
st.title("Model")
# %%
seriea_df = pd.read_excel("C:/Users/ASUS/Desktop/serieA.xlsx")
seriea = seriea_df.drop(['time','comp','round','day','attendance', 'captain', 'dist', 'fk', 'pk', 'pkatt', 'poss_y', 'touches', 'def pen', 'mid 3rd', 'att pen', 'live', 'succ', 'att', '#pl', 'megs', 'carries', 'totdist', 'prgdist', 'prog', 'prog.1', '01-mar', 'cpa', 'dis', 'targ', 'rec'], axis = 1)
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

#%%
#first thing first: import the main libraries!
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sklearn
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
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
st.header("The multinomial logisitic regression")
st.markdown(
"""
- the multinomial logistic regression is used when the dependent variable is categorical and contains more than two values (result: "W", "L", "D")
- result is the dependent variable
- starting from the whole model we look for the most significative variables

"""
)

# %%
fig, ax = plt.subplots(figsize=(10,6))
logit_model_1=sm.MNLogit(y_train_seriea, sm.add_constant(X_train_seriea))
result_1=logit_model_1.fit()
# %%
#Let's check what variables are not significative...
#we see that poss_x and mis are not significative in both lose and win case so we remove them
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
   button_1 = st.sidebar.button('Full Model')

with col2:
  button_2 = st.sidebar.button('Second Model')

with col3:
  button_3 = st.sidebar.button('Final Model')
# %%
if button_1:
  st.write(result_1.summary())
  st.write(" ")
  st.markdown(
"""
**Considerations:**
- poss_x and mis are not significative in both lose and win case
- pseudo R-squared it's used for logistic models, but it's different from ρ2
- a model with values of pseudo R-squared between 0.2 and 0.4 represent excellent fit (0.36 in this case, so it's considered a good model)

"""
)
if button_2:
  st.write(result_2.summary())
  st.write(" ")
  st.markdown(
"""
**Considerations:**
- def 3rd is not significative, while all the other variables are significative
"""
)
           
if button_3:
  st.write(result_3.summary())
  st.write(" ")
  st.write("All variables are significative!")
# %%
mod = LogisticRegression(random_state=0, multi_class='multinomial', penalty=None, solver='newton-cg').fit(X_train_seriea, y_train_seriea)
preds = mod.predict(X_test_seriea)
params = mod.get_params()
confmtrx = np.array(confusion_matrix(y_test_seriea, preds))
df_confusion = pd.DataFrame(confmtrx, index=['Draw','Lose', 'Win'], columns=['predicted_Draw', 'predicted_Lose', 'predicted_Win'])
from PIL import Image
image = Image.open('c:/Users/ASUS/Desktop/acc_dark-transformed.png')
# %%
col1, col2 = st.columns(2)

with col1:
   button_1 = st.sidebar.button('Confusion Matrix')

with col2:
  button_2 = st.sidebar.button('Classification Report')

if button_1:
  st.markdown(
"""
**For testing classification is used the confusion matrix**
- by looking the diagonal it is possible to see if the values are classified correctly
"""
)
  st.header("Confusion Matrix")
  st.write(df_confusion)

if button_2:
  st.header("Classification Report")
  st.image(image)
  st.markdown(
"""
**Considerations:**
- the accuracy score is good: 0.7
- the win variable is well classified with a good precision score
"""
)
# %%
st.sidebar.button('Reset')
if button_1 == True:
  button_1 = False
elif button_2 == True:
  button_2 = False
elif button_3 == True:
  button_3 = False
# %%

# -*- coding: utf-8 -*-
"""Prediction of Vehicle Carbon Dioxide Emissions by Statistical Learning Models

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EvVwMOcCkJDLBQQYO7dlWNybEXyf-hH7

# CO2 Emission EDA & Data Processing & Machine Learning
## Group 1 Project 1

# Importing Libraries and Dataset
"""

# Importing libraries
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings("ignore")

from sklearn.metrics import mean_squared_error, r2_score
import sklearn.metrics as skm
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split, cross_val_score, cross_val_predict
from sklearn.neighbors import LocalOutlierFactor, KNeighborsRegressor
from sklearn import preprocessing

import xgboost as xgb
import graphviz
pip install prettytable
from prettytable import PrettyTable

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 320)

#  Importing dataset
df = pd.read_csv('CO2 Emissions_Canada.csv')

"""# Exploratory Data Analysis"""

print(df.shape)
print(df.columns)
print(df.head())
print(df.info())
print(df.isnull().values.any())

# Show missing data
def missing_data(data):
    total = data.isnull().sum().sort_values(ascending = False)
    percent = (data.isnull().sum()/data.isnull().count()*100).sort_values(ascending = False)
    return pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data(df)

"""## Data Visualization"""

# Vehicle unique make
df["Make"].unique()

# Top 25 companies
df_Make=df['Make'].value_counts().reset_index().rename(columns={'index':'Make','Make':'Count'})[0:25]
df_Make
fig = go.Figure(go.Bar(
    x=df_Make['Make'],y=df_Make['Count'],
    marker={'color': df_Make['Count'],
    'colorscale': 'Viridis'},
    text=df_Make['Count'],
    textposition = "outside",
))
fig.update_layout(title_text='Top 25 Companies',xaxis_title="Company ",yaxis_title="Number Of Vehicles ",title_x=0.5)
fig.show()

# Top 10 Ford Models
df_ford=df[df["Make"]=="FORD"]
df_ford_model=df_ford["Model"].value_counts().reset_index().rename(columns={'index':'Model','Model':'Count'})[0:10]
fig = go.Figure(go.Bar(
    x=df_ford_model['Model'],y=df_ford_model['Count'],
    marker={'color': df_ford_model['Count'],
    'colorscale': 'Viridis'},
    text=df_ford_model['Count'],
    textposition = "outside",
))
fig.update_layout(title_text='Top 10 Ford Models',xaxis_title="Model ",yaxis_title="Number Of Vehicles ",title_x=0.5)
fig.show()

# Top 20 Models
df_Model=df['Model'].value_counts().reset_index().rename(columns={'index':'Model','Model':'Count'})[0:20]

fig = go.Figure(go.Bar(
    x=df_Model['Model'],y=df_Model['Count'],
    marker={'color': df_Model['Count'],
    'colorscale': 'Viridis'},
    text=df_Model['Count'],
    textposition = "outside",
))
fig.update_layout(title_text='Top 20 Models',xaxis_title="Model ",yaxis_title="Number Of Vehicles ",title_x=0.5)
fig.show()

# Vehicle Class
df_Vehicle_Class=df['Vehicle Class'].value_counts().reset_index().rename(columns={'index':'Vehicle_Class','Vehicle Class':'Count'})
fig = go.Figure(go.Bar(
    x=df_Vehicle_Class['Vehicle_Class'],y=df_Vehicle_Class['Count'],
    marker={'color': df_Vehicle_Class['Count'],
    'colorscale': 'Viridis'},
    text=df_Vehicle_Class['Count'],
    textposition = "outside",
))
fig.update_layout(title_text=' Vehicle Class',xaxis_title="Vehicle Class",yaxis_title="Number Of Vehicles ",title_x=0.5)
fig.show()

# Engine Size Histogram
fig = px.histogram(df, x="Engine Size(L)", marginal="box", hover_data=df.columns)
fig.show()

# Engine Size Scatter Plot
fig = px.scatter(df, x="Engine Size(L)", y="CO2 Emissions(g/km)")
fig.update_layout(title_text='CO2 Emissions(g/km) vs Engine Size ',xaxis_title=" Engine Size (L)",yaxis_title="CO2 Emissions(g/km)",title_x=0.5)
fig.show()

# Cylinders
fig = px.histogram(df, x="Cylinders")
fig.update_layout(title_text='Distribution Of Cylinders  ',xaxis_title=" Cylinders ",yaxis_title="Number Of Vehicles ",title_x=0.5)
fig.show()

# Extract Gears from Transmission
df["Gears"]= df['Transmission'].str[-1]

df['Transmission']=df['Transmission'].str[0:-1]
df.head()

# Transmission Pie Chart
df_Transmission=df['Transmission'].value_counts().reset_index().rename(columns={'index':'Transmission','Transmission':'Count'})
df_Transmission
fig = px.pie(df_Transmission, values='Count', names='Transmission')

fig.update_traces(hoverinfo='label+percent', textinfo='value+percent', textfont_size=12,insidetextorientation='radial')
fig.update_layout(title="Transmission Distribution",title_x=0.5)
fig.show()

# Transmission Bar Chart
df_Transmission=df['Transmission'].value_counts().reset_index().rename(columns={'index':'Transmission','Transmission':'Count'})

fig = go.Figure(go.Bar(
    x=df_Transmission['Transmission'],y=df_Transmission['Count'],
    marker={'color': df_Transmission['Count'],
    'colorscale': 'Viridis'},
    text=df_Transmission['Count'],
    textposition = "outside",
))
fig.update_layout(title_text='Transmission Distribution ',xaxis_title="Transmission ",yaxis_title="Number Of Vehicles ",title_x=0.5)
fig.show()

# Gears
df_Gears=df['Gears'].value_counts().reset_index().rename(columns={'index':'Gears','Gears':'Count'})
df_Gears
fig = px.pie(df_Gears, values='Count', names='Gears')

fig.update_traces(hoverinfo='label+percent', textinfo='value+percent', textfont_size=12,insidetextorientation='radial')
fig.update_layout(title="Gears Distribution",title_x=0.5)
fig.show()

# Fuel Type
df_Fuel_Type=df['Fuel Type'].value_counts().reset_index().rename(columns={'index':'Fuel_Type','Fuel Type':'Count'})

fig = go.Figure(go.Bar(
    x=df_Fuel_Type['Fuel_Type'],y=df_Fuel_Type['Count'],
    marker={'color': df_Fuel_Type['Count'],
    'colorscale': 'Viridis'},
    text=df_Fuel_Type['Count'],
    textposition = "outside",
))
fig.update_layout(title_text='Fuel Type Distribution ',xaxis_title="Fuel Type  ",yaxis_title="Number Of Vehicles ",title_x=0.5)
fig.show()

# Normalized Fuel Consumption City
fig = go.Figure(data=[go.Histogram(x=df["Fuel Consumption City (L/100 km)"], histnorm='probability')])
fig.update_layout(title_text='Normalized Fuel Consumption City  ',xaxis_title="Fuel Consumption",yaxis_title="Ratio",title_x=0.5)
fig.show()

# Fuel Consumption City Box Plot
fig = go.Figure()
fig.add_trace(go.Box(
    y=df["Fuel Consumption City (L/100 km)"],
    name='Fuel Consumption City',
    marker_color='royalblue',
    boxmean='sd' # represent mean and standard deviation
))
fig.update_layout(title_text='Fuel Consumption City',yaxis_title=" L / 100 km ",title_x=0.5)
fig.show()

# Fuel Consumption City Violin Plot
fig = go.Figure(data=go.Violin(y=df["Fuel Consumption City (L/100 km)"],
                               box_visible=True,
                               line_color='black',
                               meanline_visible=True,
                               fillcolor='lightseagreen', opacity=0.6,
                               x0='Fuel Consumption City'))

fig.update_layout(yaxis_zeroline=False)
fig.show()

# Normalized Fuel Consumption Highways
fig = go.Figure(data=[go.Histogram(x=df["Fuel Consumption Hwy (L/100 km)"], histnorm='probability')])
fig.update_layout(title_text='Normalized Fuel Consumption Highways  ',xaxis_title="Fuel Consumption",yaxis_title="Ratio",title_x=0.5)
fig.show()

# Fuel Consumption Highways Box Plot
fig = go.Figure()
fig.add_trace(go.Box(
    y=df["Fuel Consumption Hwy (L/100 km)"],
    name='Fuel Consumption Hwy',
    marker_color='royalblue',
    boxmean='sd' # represent mean and standard deviation
))
fig.update_layout(title_text='Fuel Consumption Highways ',yaxis_title=" L / 100 km ",title_x=0.5)
fig.show()

# Fuel Consumption Highways Violin Plot
fig = go.Figure(data=go.Violin(y=df["Fuel Consumption Hwy (L/100 km)"],
                               box_visible=True,
                               line_color='black',
                               meanline_visible=True,
                               fillcolor='lightseagreen', opacity=0.6,
                               x0='Fuel Consumption Highways '))

fig.update_layout(yaxis_zeroline=False)
fig.show()

# Normalized Fuel Consumption Combined
fig = go.Figure(data=[go.Histogram(x=df["Fuel Consumption Comb (L/100 km)"], histnorm='probability')])
fig.update_layout(title_text='Normalized Fuel Consumption Combined  ',xaxis_title="Fuel Consumption",yaxis_title="Ratio",title_x=0.5)
fig.show()

# Fuel Consumption Combined Box Plot
fig = go.Figure()
fig.add_trace(go.Box(
    y=df["Fuel Consumption Comb (L/100 km)"],
    name='Fuel Consumption Comb ',
    marker_color='royalblue',
    boxmean='sd' # represent mean and standard deviation
))
fig.update_layout(title_text='The Combined Fuel Consumption',yaxis_title=" L / 100 km ",title_x=0.5)
fig.show()

# Fuel Consumption Combined Violin Plot
fig = go.Figure(data=go.Violin(y=df["Fuel Consumption Comb (L/100 km)"],
                               box_visible=True,
                               line_color='black',
                               meanline_visible=True,
                               fillcolor='lightseagreen', opacity=0.6,
                               x0='Fuel Combined Fuel Consumption'))

fig.update_layout(yaxis_zeroline=False)
fig.show()

# Normalized Fuel Consumption Combined mpg
fig = go.Figure(data=[go.Histogram(x=df["Fuel Consumption Comb (mpg)"], histnorm='probability')])
fig.update_layout(title_text='Normalized Fuel Consumption Combined  Mile Per Gallon ',xaxis_title="Fuel Consumption",yaxis_title="Ratio",title_x=0.5)
fig.show()

# Fuel Consumption Combined mpg Box Plot
fig = go.Figure()
fig.add_trace(go.Box(
    y=df["Fuel Consumption Comb (mpg)"],
    name='Fuel Consumption Comb ',
    marker_color='royalblue',
    boxmean='sd' # represent mean and standard deviation
))
fig.update_layout(title_text='The Combined Fuel Mile Per Gallon',yaxis_title="Mpg",title_x=0.5)
fig.show()

# Fuel Consumption Combined mpg Violin Plot
fig = go.Figure(data=go.Violin(y=df["Fuel Consumption Comb (mpg)"],
                               box_visible=True,
                               line_color='black',
                               meanline_visible=True,
                               fillcolor='lightseagreen', opacity=0.6,
                               x0='Fuel Combined Fuel mile per gallon'))

fig.update_layout(yaxis_zeroline=False,yaxis_title="Mpg",title_x=0.5)
fig.show()

# Normalized CO2 Emissions Histogram
fig = go.Figure(data=[go.Histogram(x=df["CO2 Emissions(g/km)"], histnorm='probability')])
fig.update_layout(title_text='Normalized Carbon Dioxide Emissions ',xaxis_title="CO2 Emissions",yaxis_title="Ratio",title_x=0.5)
fig.show()

# CO2 Emissions Box Plot
fig = go.Figure()
fig.add_trace(go.Box(
    y=df["CO2 Emissions(g/km)"],
    name='CO2 Emissions ',
    marker_color='royalblue',
    boxmean='sd' # represent mean and standard deviation
))
fig.update_layout(title_text='CO2 Emissions',yaxis_title="Quantity",title_x=0.5)
fig.show()

# CO2 Emissions Violin Plot
fig = go.Figure(data=go.Violin(y=df["CO2 Emissions(g/km)"],
                               box_visible=True,
                               line_color='black',
                               meanline_visible=True,
                               fillcolor='lightseagreen', opacity=0.6,
                               x0='CO2 Emissions'))

fig.update_layout(yaxis_zeroline=False,yaxis_title="Quantity",title_x=0.5)
fig.show()

# Correlation Matrix
print("Correlation Matrix")
plt.rcParams['figure.figsize']=(8,6)
sns.heatmap(df.corr(),cmap='coolwarm',linewidths=.5,fmt=".2f",annot = True);

"""# Data Processing"""

# Remove some features
df.drop(['Make','Model','Vehicle Class','Fuel Consumption City (L/100 km)','Fuel Consumption Hwy (L/100 km)','Transmission','Fuel Consumption Comb (mpg)'],inplace=True,axis=1)
df.head()
df_N = df[df["Fuel Type"]=="N"]
indexs = df_N.index
df_N
for i in indexs:
    df.drop(i, axis = 0,inplace = True)
df[df["Fuel Type"]=="N"]
dums = pd.get_dummies(df['Fuel Type'],prefix="Fuel_Type",drop_first=True)
print(dums[0:15])
frames = [df, dums]
result = pd.concat(frames,axis=1)
print(result)

result.drop(['Fuel Type'],inplace=True,axis=1)
print(result.head())

X = result.drop(['CO2 Emissions(g/km)'], axis= 1)
y = result["CO2 Emissions(g/km)"]

# Finding Outliers
clf = LocalOutlierFactor(n_neighbors = 20, contamination = 0.1)
df_out = result.copy()
clf.fit_predict(df_out)
df_scores = clf.negative_outlier_factor_
np.sort(df_scores)[0:25]
threshold_value = np.sort(df_scores)[24]
Outlier_df = df_out[df_scores < threshold_value]
indexs = Outlier_df.index

# Remove Outliers
for i in indexs:
    result.drop(i, axis = 0,inplace = True)
result.info()

# Normalization
X = (X - np.min(X)) / (np.max(X) - np.min(X)).values
X["Engine Size(L)"] = X["Engine Size(L)"].map(lambda x:round(x,2))
X["Cylinders"] = X["Cylinders"].map(lambda x:round(x,2))
X["Fuel Consumption Comb (L/100 km)"] = X["Fuel Consumption Comb (L/100 km)"].map(lambda x:round(x,2))

# Splitting training data and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4011)

print("X_train", X_train.shape)
print("y_train",y_train.shape)
print("X_test",X_test.shape)
print("y_test",y_test.shape)

"""# Linear Regression"""

# function to get cross validation scores
def get_cv_scores(model):
    scores = cross_val_score(model,
                             X_train,
                             y_train,
                             cv=10,
                             scoring='r2')

    print('CV Mean: ', np.mean(scores))
    print('STD: ', np.std(scores))
    print('\n')

# Train model
lr = LinearRegression().fit(X_train, y_train)
y_pred = lr.predict(X_test)
# get cross val scores
print("result for linear regression: ")
get_cv_scores(lr)

from sklearn.linear_model import Ridge
# Train model with default alpha=1
ridge = Ridge(alpha=1).fit(X_train, y_train)
# get cross val scores
print("result for ridge regression: ")
get_cv_scores(ridge)

# find optimal alpha with grid search
alpha = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
param_grid = dict(alpha=alpha)
grid = GridSearchCV(estimator=ridge, param_grid=param_grid, scoring='r2', verbose=1, n_jobs=-1)
grid_result = grid.fit(X_train, y_train)
print("result for ridge regression after tuning: ")
print('Best Score: ', grid_result.best_score_)
print('Best Params: ', grid_result.best_params_)
print('\n')

from sklearn.linear_model import Lasso
# Train model with default alpha=1
lasso = Lasso(alpha=1).fit(X_train, y_train)
# get cross val scores
print("result for Lasso regression: ")
get_cv_scores(lasso)

alpha = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
param_grid = dict(alpha=alpha)
grid = GridSearchCV(estimator=lasso, param_grid=param_grid, scoring='r2', verbose=1, n_jobs=-1)
grid_result = grid.fit(X_train, y_train)
print("result for Lasso regression after tuning: ")
print('Best Score: ', grid_result.best_score_)
print('Best Params: ', grid_result.best_params_)

# rmse of linear regression
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE of linear regression: %f" % (rmse_lr))
# mape of KNN
mape_lr = skm.mean_absolute_error(y_test, y_pred)
print("MAPE of linear regression: %f" % (mape_lr))
# mae of knn
mae_lr = skm.mean_absolute_percentage_error(y_test, y_pred)*100
print("MAE of linear regression: %f" % (mae_lr))

"""# KNN"""

# fitting model
knn_model = KNeighborsRegressor().fit(X_train, y_train)
y_pred = knn_model.predict(X_test)
np.sqrt(mean_squared_error(y_test, y_pred))

# rmse of KNN
rmse_knn = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE of KNN: %f" % (rmse_knn))

# mape of KNN
mape_knn = skm.mean_absolute_error(y_test, y_pred)
print("MAPE of KNN: %f" % (mape_knn))

# mae of knn
mae_knn = skm.mean_absolute_percentage_error(y_test, y_pred)*100
print("MAE of KNN: %f" % (mae_knn))

# train set model score
knn_model.score(X_train, y_train)

# test set model score
knn_model.score(X_test, y_test)

"""### Cross Validation"""

# initialize a machine learning model
model = knn_model()

# implement cross_val_score with the model, X, y, scoring='neg_mean_squared_error', and the number of folds, cv=10, as input
scores = cross_val_score(model, X, y, scoring='neg_mean_squared_error', cv=10)

# find the RMSE by taking the square root of the negative scores
rmse = np.sqrt(-scores)

# display the results
print('Reg rmse:', np.round(rmse, 2))

print('RMSE mean: %0.2f' % (rmse.mean()))

# finding best k
knn_params = {'n_neighbors': np.arange(1,50,1)}
knn = KNeighborsRegressor()
knn_cv_model = GridSearchCV(knn, knn_params, cv = 10)
knn_cv_model.fit(X_train, y_train)
knn_cv_model.best_params_["n_neighbors"]

# fitting best k
knn_tuned = KNeighborsRegressor(n_neighbors = knn_cv_model.best_params_["n_neighbors"])
knn_tuned.fit(X_train, y_train)

# rmse of tuned knn
rmse_tuned_knn = np.sqrt(mean_squared_error(y_test, knn_tuned.predict(X_test)))
print("RMSE of tuned KNN: %f" % (rmse_tuned_knn))

# tuned knn test set model score
knn_tuned.score(X_test, y_test)

# mape of tuned knn
mape_tuned_knn = skm.mean_absolute_percentage_error(y_test, knn_tuned.predict(X_test))*100
print("MAPE of tuned KNN: %f" % (mape_tuned_knn))

# mae of tuned knn
mae_tuned_knn = skm.mean_absolute_error(y_test, knn_tuned.predict(X_test))
print("MAE of tuned KNN: %f" % (mae_tuned_knn))

# bagging of tuned knn
bagged_knn = KNeighborsRegressor(
    n_neighbors=knn_cv_model.best_params_["n_neighbors"]
)
bagging_model = BaggingRegressor(bagged_knn, n_estimators=100)
bagging_model.fit(X_test, y_test)
bagging_test_preds = bagging_model.predict(X_test)
np.sqrt(mean_squared_error(y_test, bagging_test_preds))

# rmse of bagging of tuned knn
rmse_bagging_tuned_knn = np.sqrt(mean_squared_error(y_test, bagging_test_preds))
print("RMSE of bagging of tuned KNN: %f" % (rmse_bagging_tuned_knn))

# mape of bagging of tuned knn
mape_bagging_tuned_knn = skm.mean_absolute_percentage_error(y_test, bagging_test_preds)*100
print("MAPE of bagging of tuned KNN: %f" % (mape_bagging_tuned_knn))

# mae of bagging of tuned knn
mae_bagging_tuned_knn = skm.mean_absolute_error(y_test, bagging_test_preds)
print("MAE of bagging of tuned KNN: %f" % (mae_bagging_tuned_knn))

#bagging test set model score
bagging_model.score(X_test, y_test)

# comparison of 3 knn
knn = [rmse_knn, mape_knn, mae_knn]
tuned_knn = [rmse_tuned_knn, mape_tuned_knn, mae_tuned_knn]
bagging_tuned_knn = [rmse_bagging_tuned_knn, mape_bagging_tuned_knn, mae_bagging_tuned_knn]

frames = [knn, tuned_knn, bagging_tuned_knn]
table = pd.DataFrame(data=frames)
table = table.T
table = table.rename(columns={0:'KNN', 1:'tuned KNN', 2:'bagging tuned KNN'})
table = table.rename(mapper={0:'RMSE', 1:'MAPE', 2:'MAE'})
print(table)

"""# XGBoost"""

# convert data to optimized DMatrix constructor
data_dmatrix = xgb.DMatrix(data=X, label=y)

# initialize a machine learning model
xg_reg = xgb.XGBRegressor(random_state=4011)

# fit the model on the training set
xg_reg.fit(X_train,y_train)

# make predictions for the test set
preds = xg_reg.predict(X_test)

# compare predictions with test set
rmse = skm.mean_squared_error(y_test, preds, squared=False)
print("RMSE: %f" % (rmse))

"""### Cross Validation"""

# initialize a machine learning model
model = xgb.XGBRegressor()

# implement cross_val_score with the model, X, y, scoring='neg_mean_squared_error', and the number of folds, cv=10, as input
scores = cross_val_score(model, X, y, scoring='neg_mean_squared_error', cv=10)

# find the RMSE by taking the square root of the negative scores
rmse = np.sqrt(-scores)

# display the results
print('Reg rmse:', np.round(rmse, 2))

print('RMSE mean: %0.2f' % (rmse.mean()))

"""### Hyperparameter Tuning"""

# possible parameters we want to optimize
params = {
    'max_depth':[3,4,5,6,7,8,9,10],
    'learning_rate':[0.01,0.05,0.1],
    'n_estimators':[100,300,500,1000],
    'subsample': np.arange(0.5, 1.0, 0.1),
    'colsample_bytree': np.arange(0.4, 1.0, 0.1),
    'colsample_bylevel': np.arange(0.4, 1.0, 0.1),
}

# initialize a gradient boosting model
gb = xgb.XGBRegressor(random_state=4011)

# initialize RandomizedSearchCV with various inputs
gb_cv = RandomizedSearchCV(estimator=gb,
                           param_distributions=params,
                           scoring='neg_mean_squared_error',
                           n_iter=100,
                           cv=5,
                           n_jobs=-1,
                           random_state=4011)

# fit the model on the training set and obtain the best parameters and scores
gb_cv.fit(X_train,y_train)

# print("Best Parameters:",gb_cv.best_params_)
# print("Train Score:",gb_cv.best_score_)
# print("Test Score:",gb_cv.score(X_test,y_test))

#rand_reg.fit(X_train, y_train)

best_model = gb_cv.best_estimator_

best_params = gb_cv.best_params_

print("Best params:", best_params)

best_score = np.sqrt(-gb_cv.best_score_)

print("Training score: {:.3f}".format(best_score))

y_pred = best_model.predict(X_test)

rmse_test = skm.mean_squared_error(y_test, y_pred)**0.5

print('Test set score: {:.3f}'.format(rmse_test))

# optimised model with tuned hyperparameters
xg_reg = xgb.XGBRegressor(subsample=0.9, n_estimators=1000, max_depth=8, learning_rate=0.01,
                          colsample_bytree=0.9, colsample_bylevel=0.6, random_state=4011)

xg_reg.fit(X_train,y_train)

preds = xg_reg.predict(X_test)

xgb_rmse = skm.mean_squared_error(y_test, preds, squared=False)
print("RMSE: %f" % (xgb_rmse))

xgb_mape = skm.mean_absolute_percentage_error(y_test, preds) * 100
print("MAPE: %f" % (xgb_mape))

xgb_mae = skm.mean_absolute_error(y_test, preds)
print("MAE: %f" % (xgb_mae))

"""### Boosting Trees and Feature Importance Visualization"""

params = {'subsample': 0.9, 'max_depth': 8, 'learning_rate': 0.01, 'colsample_bytree': 0.9, 'colsample_bylevel': 0.6}
xg_reg = xgb.train(params=params, dtrain=data_dmatrix, num_boost_round=1000)

xgb.plot_tree(xg_reg, num_trees=999)
fig = plt.gcf()
fig.set_size_inches(50, 100)
fig.savefig('tree.png', dpi=300)

xgb.plot_importance(xg_reg)
fig = plt.gcf()
fig.set_size_inches(50, 20)
fig.savefig('feature_importance.png', dpi=300)

"""# Random Forest"""

# Random Forest
rf_model = RandomForestRegressor(random_state = 42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
rf_rmse=np.sqrt(mean_squared_error(y_test, y_pred))
# RMSE of tuned random forest
print("RMSE before tuning:", rf_rmse)

# MAPE of tuned random forest
mape_tuned_rf = skm.mean_absolute_percentage_error(y_test, rf_model.predict(X_test))*100
print("MAPE before tuning: %f" % (mape_tuned_rf))

# MAE of tuned random forest
mae = skm.mean_absolute_error(y_test, y_pred)
print("MAE before tuning: %f" % (mae))

# Finding the best Random Forest parameters
rf_params = {'max_depth': list(range(1,20)), 'max_features': [3,5,7,9], 'n_estimators' : [50,75,100,125]}
rf_model = RandomForestRegressor(random_state = 42)
rf_cv_model = GridSearchCV(rf_model, rf_params, cv = 10, n_jobs = -1, verbose = 2)
rf_cv_model.fit(X_train, y_train)
print("rf best params:", rf_cv_model.best_params_)

# Apply the best Random Forest parameters
# {'max_depth': 12, 'max_features': 5, 'n_estimators': 75}
rf_tuned = RandomForestRegressor(max_depth  = 12, max_features = 5, n_estimators =75, random_state = 42)
rf_tuned.fit(X_train, y_train)
y_pred = rf_tuned.predict(X_test)
print("RMSE after tuned:", np.sqrt(mean_squared_error(y_test, y_pred)))

# Plot variables importance
Importance = pd.DataFrame({"Importance": rf_tuned.feature_importances_*100}, index = X_train.columns)
Importance.sort_values(by = "Importance", axis = 0, ascending = True).plot(kind ="barh", color = "r")
plt.xlabel("Variable Significance Levels")
plt.show()

# MAPE of tuned random forest
mape_tuned_rf = skm.mean_absolute_percentage_error(y_test, rf_tuned.predict(X_test))*100
print("MAPE after tuned: %f" % (mape_tuned_rf))

# MAE of tuned random forest
mae = skm.mean_absolute_error(y_test, y_pred)
print("MAE after tuned: %f" % (mae))

"""# Model Comparison"""

myTable = PrettyTable(["Algorithm", "RMSE", "MAE", "MAPE"])
myTable.add_row(["LR", lr_rmse, lr_mae, lr_mape])
myTable.add_row(["KNN", rmse_bagging_tuned_knn, mape_bagging_tuned_knn, mae_bagging_tuned_knn])
myTable.add_row(["XGBoost", xgb_rmse, xgb_mae, xgb_mape])
myTable.add_row(["Random Forest", rf_rmse, rf_mae, rf_tuned_mape])

print(myTable)

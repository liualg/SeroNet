import pandas as pd 
import numpy as np
import sklearn
import plotly
import datetime as dt
from tqdm import tqdm

import plotly.express as px

dataset = pd.read_csv('/Users/liualg/Downloads/Wargo Sample deliveries data - 1 month (1).xlsx - deliveries.csv.csv')
# dataset = dataset.replace('')

dataset.describe()

datadrop = dataset.copy()
datadrop = datadrop.dropna()
datadrop.describe()

datadrop['percent_discount'] = datadrop['Order total']/datadrop['Amount of discount']

datadrop['Driver ID'].value_counts()[:5]

datadrop['hour_ordered'] = [(dt.datetime.strptime(i.split(' ')[1], '%H:%M:%S')- dt.datetime(1900, 1, 1)).total_seconds()//3600 for i in datadrop['Customer placed order datetime']]
datadrop['seconds_ordered'] = [(dt.datetime.strptime(i.split(' ')[1], '%H:%M:%S')- dt.datetime(1900, 1, 1)).total_seconds() for i in datadrop['Customer placed order datetime']]

from sklearn.preprocessing import LabelEncoder
datadrop['order_day'] = [i.split(' ')[0] for i in datadrop['Customer placed order datetime']]


labesEnco = LabelEncoder()
datadrop.loc[:,'Delivery Region']  = labesEnco.fit_transform(datadrop.loc[:,'Delivery Region'])
datadrop.loc[:,'Is ASAP'] = labesEnco.fit_transform(datadrop.loc[:,'Is ASAP'])
datadrop.loc[:,'order_day'] = labesEnco.fit_transform(datadrop.loc[:,'order_day'])
datadrop['percent_discount'] = datadrop['percent_discount'].replace(np.inf, 0)
datadrop

corrMatrix = datadrop.corr()
px.imshow(corrMatrix, text_auto=True)

orderPlaced = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Customer placed order datetime']]
restaurantOrder = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Placed order with restaurant datetime']]
driverArrived = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Driver at restaurant datetime']]
delivered = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Delivered to consumer datetime']]

order_delta = [t2-t1 for t1, t2, in zip(orderPlaced, restaurantOrder)] #server speed
driver_delta = [t2-t1 for t1, t2, in zip(orderPlaced, driverArrived)] #server speed
deliver_delta = [t2-t1 for t1, t2, in zip(orderPlaced, delivered)] #restaurent speed
driver_speed = [t2-t1 for t1, t2, in zip(driverArrived, delivered)] #driver speed


datadrop['order_delta'] = [i.total_seconds() for i in order_delta]
datadrop['driver_delta'] = [i.total_seconds() for i in driver_delta]
datadrop['deliver_delta'] = [i.total_seconds() for i in deliver_delta]
datadrop['driver_speed'] = [i.total_seconds() for i in driver_speed]

datadrop

# corrMatrix = datadrop.corr()
# px.imshow(corrMatrix, text_auto=True)

px.histogram([i.split(' ')[0] for i in datadrop['Customer placed order datetime']]).update_xaxes(categoryorder="total descending")

# number of orders in a day 
day_summary = datadrop.groupby(['order_day']).mean()
day_summary = day_summary.iloc[:, 5:]
px.imshow(day_summary.corr(), text_auto=True)

datadrop['percent_tip'] = datadrop['Amount of tip']/datadrop['Order total']

corrMatrix = datadrop.corr()
px.imshow(corrMatrix, text_auto=True)

px.scatter(datadrop, x = 'seconds_ordered', y = 'Order total', color='Restaurant ID')


35500/3600

# orderPlaced = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Customer placed order datetime']]
# restaurantOrder = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Placed order with restaurant datetime']]
# driverArrived = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Driver at restaurant datetime']]
# delivered = [dt.datetime.strptime(date, "%d %H:%M:%S") for date in datadrop['Delivered to consumer datetime']]

# order_delta = [t2-t1 for t1, t2, in zip(orderPlaced, restaurantOrder)] #server speed
# driver_delta = [t2-t1 for t1, t2, in zip(orderPlaced, driverArrived)] #server speed
# deliver_delta = [t2-t1 for t1, t2, in zip(orderPlaced, delivered)] #restaurent speed
# driver_speed = [t2-t1 for t1, t2, in zip(driverArrived, delivered)] #driver speed

# # px.scatter(order_delta)

# # for i in tqdm(range(len(dataset['Placed order with restaurant datetime']))):
# #     if pd.isna(dataset['Placed order with restaurant datetime'][i]):
# #         dataset.iloc[i, 1] = (dt.datetime.strptime(
# #             dataset.iloc[i, 1], "%d %H:%M:%S") + np.mean(order_delta)).time()
        
# #     if pd.isna(dataset['Driver at restaurant datetime'][i]):
# #         dataset.iloc[i, 2] = (dt.datetime.strptime(
# #             dataset.iloc[i, 2], "%d %H:%M:%S") + np.mean(driver_delta)).time()
  
# #     if pd.isna(dataset['Delivered to consumer datetime'][i]):
# #         dataset.iloc[i, 3] = (dt.datetime.strptime(
# #             dataset.iloc[i, 3], "%d %H:%M:%S") + np.mean(driver_speed)).time()


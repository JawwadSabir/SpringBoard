# These are your tasks for this mini project:
#
# 1. Collect data from the Frankfurt Stock Exchange, for the ticker AFX_X,
#    for the whole year 2017 (keep in mind that the date format is YYYY-MM-DD).
# 2. Convert the returned JSON object into a Python dictionary.
# 3. Calculate what the highest and lowest opening prices were for the stock in this period.
# 4. What was the largest change in any one day (based on High and Low price)?
# 5. What was the largest change between any two days (based on Closing Price)?
# 6. What was the average daily trading volume during this year?
# 7. (Optional) What was the median trading volume during this year.
#    (Note: you may need to implement your own function for calculating the median.)


import json
import requests
import datetime
from matplotlib import pyplot as plt
from matplotlib.dates import drange
import os

key = os.environ.get('api_key')
plt.style.use('fivethirtyeight')

# my API key for the Quandl (free API)
API_key = key

# ============== TASK 1 ==============
# get the data from the website

# In my case I want to get data of Frankfurt Stock Exchange
# for the ticker AFX_X, for the whole year 2017

url = 'https://www.quandl.com/api/v3/datasets/FSE/AFX_X.json'

params = dict(api_key=API_key, start_date='2017-01-01', end_date='2017-12-31')

r = requests.get(url, params=params)
json_obj = r.json()

# separate the useful data from the json object
columnNames = json_obj['dataset']['column_names']
data_obj = json_obj['dataset']['data']

# ============== TASK 2 ==============
# convert the json object into the dictionary format
# zipping the relevant data together and converting it into a dictionary
dt = dict(zip(columnNames, zip(*data_obj)))

# ============== TASK 3 ==============
# Calculate what the highest and lowest opening prices were for the stock in this period.
date_x = dt['Date']

# replacing the missing values with the value at previous index
# to plot the graph without None values
open_price = [dt['Open'][dt['Open'].index(v) - 1] if v is None else v for v in dt['Open']]

highest_price = max(float(price) for price in open_price)
lowest_price = min(float(price) for price in open_price)

print("highest opening price for the year 2017 is  ", highest_price)
print("lowest opening price for the year 2017 is  ", lowest_price)


# ============== TASK 4 ==============
# Largest change in one day based on high and low prices
data_length = len(dt['Date'])
high_price = dt['High']
low_price = dt['Low']


def largest_change_oneDay(arr1, arr2):
    diff = 0
    for i in range(len(arr1)):
        temp = arr1[i] - arr2[i]
        if temp > diff:
            diff = temp
    return round(diff, 2)


print("Largest change in one day is: ", largest_change_oneDay(high_price, low_price))

# ============== TASK 5 ==============
# largest change between any two days (based on Closing Price)
closing_price = dt['Close']


def largest_change_twoDays(arr):
    lc = 0
    for i in range(1, len(arr)):
        if arr[i] is not None:
            temp = abs((arr[i]) - (arr[i - 1]))
            if temp > lc:
                lc = temp
    return round(lc, 2)


print("largest change between any two days is: ", largest_change_twoDays(closing_price))

# ============== TASK 6 ==============
# average daily trading volume during this year

trading_volume = dt['Traded Volume']
average_trading_volume = sum(trading_volume) / len(trading_volume)

print("average daily trading volume during this year is: ", round(average_trading_volume, 2))


# ============== TASK 7 ==============
# median trading volume for the year
def median_cal(arr):
    m = int(len(arr) / 2)
    # if even no of elements in array take the average of middle two
    if len(arr) % 2 == 0:
        med = (arr[m] + arr[m + 1]) / 2
    else:
        med = arr[m]
    return med


print("median trading volume for the year is: ", median_cal(trading_volume))

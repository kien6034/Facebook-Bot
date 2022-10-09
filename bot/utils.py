import pandas as pd 
import datetime, sys 
import bot.config as config
import math 


def extract_relative_date_to_timestamp(rd):
    time_stamp = int(datetime.datetime.now().timestamp())
    relative_time_to_current = None 
    try:
        data = rd.split(" ")
    except:
        # No comment has been made -> Treat as urgent  
        relative_time_to_current= 0
        exact_timestamp = time_stamp - relative_time_to_current
        exact_date_time = datetime.datetime.fromtimestamp(exact_timestamp)
        return exact_timestamp, exact_date_time


    amount = int(data[0])
    time_interval = data[1]

    if time_interval == "phút":
        relative_time_to_current = config.MINUTE_IN_TIME_STAMP * amount 
    elif time_interval == "giờ":
        relative_time_to_current = config.HOUR_IN_TIME_STAMP * amount 
    elif time_interval == "ngày":
        relative_time_to_current = config.DAY_IN_TIME_STAMP * amount 
    elif time_interval == "tuần":
        relative_time_to_current = config.WEEK_IN_TIME_STAMP * amount 
    elif time_interval == "tháng":
        relative_time_to_current = config.MONTH_IN_TIME_STAMP * amount
    else:
        # post after a year is considered as unvaluable 
        relative_time_to_current = config.YEAR_IN_TIME_STAMP * 1 

    exact_timestamp = time_stamp - relative_time_to_current
    exact_date_time = datetime.datetime.fromtimestamp(exact_timestamp)
    return exact_timestamp, exact_date_time



def inversed_sigmoid(current_value, threshold):
    #https://datascience.stackexchange.com/questions/22639/how-to-determine-threshold-in-sigmoid-function
    x = threshold - current_value 
    
    try:
        return 1 / (1 + math.exp(-x))
    except:
        # handle if X is too large 
        return 0


def sigmoid(current_value, threshold):
    #https://datascience.stackexchange.com/questions/22639/how-to-determine-threshold-in-sigmoid-function
    x = current_value - threshold
    
    try:
        return 1 / (1 + math.exp(-x))
    except:
        # handle if X is too large 
        return 0


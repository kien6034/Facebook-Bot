import pandas as pd 
import datetime, sys 


def extract_relative_date_to_timestamp(rd):
    time_stamp = int(datetime.datetime.now().timestamp())

    MINUTE_IN_TIME_STAMP =60
    HOUR_IN_TIME_STAMP = MINUTE_IN_TIME_STAMP * 60 
    DAY_IN_TIME_STAMP = HOUR_IN_TIME_STAMP * 24 
    WEEK_IN_TIME_STAMP = DAY_IN_TIME_STAMP * 7 
    MONTH_IN_TIME_STAMP = WEEK_IN_TIME_STAMP * 4
    YEAR_IN_TIME_STAMP = MONTH_IN_TIME_STAMP * 12

    try:
        data = rd.split(" ")
    except:
        # No comment has been made -> Treat as urgent  
        relative_time_to_current= 0

    relative_time_to_current = None 

    amount = int(data[0])
    time_interval = data[1]
    if time_interval == "phút":
        relative_time_to_current = MINUTE_IN_TIME_STAMP * amount 
    elif time_interval == "giờ":
        relative_time_to_current = HOUR_IN_TIME_STAMP * amount 
    elif time_interval == "ngày":
        relative_time_to_current = DAY_IN_TIME_STAMP * amount 
    elif time_interval == "tuần":
        relative_time_to_current = WEEK_IN_TIME_STAMP * amount 
    elif time_interval == "tháng":
        relative_time_to_current = MONTH_IN_TIME_STAMP * amount
    else:
        # post after a year is considered as unvaluable 
        relative_time_to_current = YEAR_IN_TIME_STAMP * 1 

    exact_timestamp = time_stamp - relative_time_to_current
    exact_date_time = datetime.datetime.fromtimestamp(exact_timestamp)
    return exact_timestamp, exact_date_time





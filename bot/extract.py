from numpy import NAN
import pandas as pd 
import datetime, sys 



time_stamp = int(datetime.datetime.now().timestamp())

sys.exit()


df= pd.read_csv("data.csv")
relative_dates = df.relative_date

for rd in relative_dates:
    try:
        data = rd.split(" ")
    except:
        continue

    if data[1] == "phút":
        print("Phút+", data[0])
    elif data[1] == "giờ":
        print("Giờ+" ,data[0])
    elif data[1] == "ngày":
        print("Ngày+" ,data[0])
    else:
        continue



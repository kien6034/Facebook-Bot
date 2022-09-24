import pandas as pd 
import bot.config as config 
import datetime, sys 
import bot.utils as utils

"""
    Data format:
    author,content,href,exact_timestamp,exact_date_time,relative_date
"""

class Thinker:
    def __init__(self) -> None:
        self.data = self.read_data_from_csv()


    def read_data_from_csv(self) -> pd.DataFrame:
        return pd.read_csv("data.csv")


    def run(self):
        for index, row in self.data.iterrows():
            
            self.analyze_data(row)
    
    def analyze_data(self, row):
        
        rate= self._evaluate_posting_date(row.exact_timestamp)
        print(row.relative_date)
        print(rate)
        print("------------------------------\n\n")
        return

    
    def _evaluate_posting_date(self, post_timestamp):
        # Propose rating method: Rate the important of the date with the value of 0 -> 1 from  WEEK back to current date 
        if pd.isna(post_timestamp):
            return 0 

        # Define the zero threshold     
        post_timestamp = int(post_timestamp)
        cur_timestamp = int(datetime.datetime.now().timestamp())

        relative_timestamp = int((cur_timestamp - post_timestamp)/config.HOUR_IN_TIME_STAMP)

        # For post over a week, value should be zero. For post at threshold, which is 2 days, value is 1/2 
        threshold = int(config.WEEK_IN_TIME_STAMP / 3.5 /config.HOUR_IN_TIME_STAMP)

        # using SIGMOID function to evaluate 
        rate = utils.sigmoid(relative_timestamp, threshold)
        return rate 
        
        

    
    def _evaluate_content(self, content):
        # Scanning the keyword 
        # Positive key word:
        # Negative key word 
        print(content)
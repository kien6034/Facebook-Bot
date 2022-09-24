import pandas as pd 


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
        
        self._evaluate_posting_date(row.exact_timestamp)
        print("------------------------------\n\n")
        return

    
    def _evaluate_posting_date(self, post_timestamp):
        # Propose rating method: Rate the important of the date with the value of 0 -> 1 from 2 WEEKS back to current date 
        # Using log -> more close to date, more important 
        print(post_timestamp)

    
    def _evaluate_content(self, content):
        # Scanning the keyword 
        # Positive key word:
        # Negative key word 
        print(content)
import gspread 
import json 
import pandas as pd 

class CsvHandler:
    def __init__(self) -> None:
        self.data = self.read_data_from_csv("data.csv")
        self.new = self.read_data_from_csv("new.csv")
     
    def read_data_from_csv(self, file_name) -> pd.DataFrame:
        data = pd.read_csv(file_name)
      
        return data 

    def check_if_key_existed(self, key): 
        return key in self.data.index

    def update_csv_data(self):
        new = pd.concat([self.data, self.new], ignore_index=True).drop_duplicates(subset=["key"])
        new.to_csv("data.csv", index=False)
    

    
    
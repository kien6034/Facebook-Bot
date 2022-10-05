from operator import index
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

    
    def check_if_key_existed(self, key): 
        self.data.set_index("key", inplace=True)


        print(self.data.head())
        return key in self.data.index


    def run(self):
        for index, row in self.data.iterrows():
            self.analyze_data(row)
    
    def analyze_data(self, row):
        
        rate= self._evaluate_posting_date(row.exact_timestamp)
        pr, nr = self._evaluate_content(row.content)
        print(row.content)
        print("---\n")
        print(f"Positive - Negative: {pr} | {nr}")
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

    
    def _evaluate_content(self, content: str):
 
        try:
            list_of_words = content.split(" ")
            pr, nr = self._get_content_rate(list_of_words)
            return pr, nr
            
        except:
            return -100000000, 100000000
    

    def _get_content_rate(self, list_of_words):
        positive_key_words = [
            {
                "keyword": {
                    "view biển", "sát biển", "chill", "chiu"
                },
                "rate": 100
            },
            {
                "keyword": {
                    "homestay", "khách sạn", "ks", "view"
                    "cần tìm", "cần", "tư vấn", "dự định", "hỏi", "tìm", "muốn", "tham khảo",
                    "rẻ", "nghỉ dưỡng", "cảm ơn"
                },
                "rate": 10
            },
            {
                "keyword": {
                    "chào", "cho", "đi"
                },
                "rate": 5
            }
        ]

        negative_key_word = [
            {
                "keyword": {
                    "top", "trải nghiệm", "pass"
                },
                "rate": -100
            },
            {
                "keyword": {
                    "nhận", "em nhận",
                    "nhanh nhanh", "review", "khách"
                },
                "rate": -10
            },
            {
                "keyword": {
                    "thời tiết",
                    "mua hàng",
                },
                "rate": -5
            },
            {
                "keyword": {
                    "xem thêm", "giá sỉ"
                },
                "rate": -10000
            }
        ]

        pr =  0
        p_rated_key_word = set()
        nr = 0
        n_rated_key_word = set()
        for idx, _ in enumerate(list_of_words):
            
            word1 =  list_of_words[idx].lower()
            word2 = None 
            if idx  < (len(list_of_words) - 1):
                word2 = word1 + " " + list_of_words[idx+1].lower()

            for pw in positive_key_words:
                rate = pw["rate"]
                keyword = pw["keyword"]

                if word1 in keyword and word1 not in p_rated_key_word:
                    p_rated_key_word.add(word1)
                    pr += rate 
                if word2 in keyword and word2 not in p_rated_key_word:
                    p_rated_key_word.add(word2)
                    pr += rate 
            

            for nw in negative_key_word:
                rate = nw["rate"]
                keyword = nw["keyword"]

                if word1 in keyword and word1 not in n_rated_key_word:
                    n_rated_key_word.add(word1)
                    nr += rate 
                if word2 in keyword and word2 not in n_rated_key_word:
                    n_rated_key_word.add(word2)
                    nr += rate 
        
        return pr, nr
    
    
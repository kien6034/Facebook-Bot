from distutils.log import error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import sys, os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

LOAD_POSTS_AFTER  = 3 

class Crawler: 
    def __init__(self) -> None:
       self.browser = None 
       self.group = None 
       self.posts = []
       self.__connect__()
    
    def __connect__(self):
        try:
            s = Service("./chromedriver/chromedriver")
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications" : 2}
            chrome_options.add_experimental_option("prefs",prefs)
            self.browser = webdriver.Chrome(service=s, options=chrome_options)
        except error:
            print(f"Can't get the browser instance: {error}")
            sys.exit(1)

    def login(self):
        self.browser.get("https://facebook.com")
        try:
            username = os.environ.get("FB_USERNAME")
            password = os.environ.get("FB_PASSWORD")

            txtUser = self.browser.find_element(by=By.ID, value="email")
            txtUser.send_keys(username)
            txtPass = self.browser.find_element(by=By.ID, value="pass")
            txtPass.send_keys(password)
            txtPass.send_keys(Keys.ENTER)
            sleep(3)
        except error:
            print(f"Can't login with error: {error}")
            sys.exit(1)

    
    def go_to_group(self, group_url):
        self.browser.get(group_url)
        self.group = self.browser.find_element(by=By.TAG_NAME, value="html")
        self.group.send_keys(Keys.END)
        sleep(2)

        

    
    def get_group_posts(self, page_loads = 5):
        self.posts = self.group.find_elements(by=By.CSS_SELECTOR, value="div.g4tp4svg.mfclru0v.om3e55n1.p8bdhjjv")
        print(f"{len(self.posts)} posts found \n")

        i = 0 
        while True:
            # Get posts every 2 page load 
            
            self.group.send_keys(Keys.END)
            i += 1
            sleep(2)
            posts = self.group.find_elements(by=By.CSS_SELECTOR, value="div.g4tp4svg.mfclru0v.om3e55n1.p8bdhjjv")

            for post in posts:
                self.analyze_post(post)
          
            if i >= page_loads:
                break
        

    def analyze_post(self, post):
        sections = post.find_elements(by= By.CSS_SELECTOR, value=".jroqu855.nthtkgg5")
        name = sections[0]
        date = sections[1]
        #TODO: get the date 

        content = post.find_elements(by= By.CSS_SELECTOR, value=".m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.gh25dzvf")
        print(name.text)
        if len(content) > 1: 
            print(content[1].text)
        else:
            print(content[0].text)

        print("---------------------------------------- \n \n") 
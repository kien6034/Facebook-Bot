from distutils.log import error
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
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
       self.posts = pd.DataFrame()

       self.tests = {}
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
                print(self.tests)
                break
        

    def analyze_post(self, post: WebElement):
        sections = post.find_elements(by= By.CSS_SELECTOR, value=".jroqu855.nthtkgg5")
        header_section = sections[0]
        date = sections[1]
        #TODO: get the date 

        content_section = post.find_elements(by= By.CSS_SELECTOR, value=".m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.gh25dzvf")

        author_name = header_section.text 
        post_content = None 

        post_content1 = None 
        post_content0 = content_section[0].text
        if len(content_section)> 1:
            post_content1 = content_section[1].text

        if post_content0 != "":
            post_content = post_content0
        else:
            post_content = post_content1
        
        if post_content != None:
            post_content.replace("\n", " ")
      
        key = author_name + post_content0[0:2]

        self.tests[key] = {
            "author": author_name,
            "content": post_content,
        }
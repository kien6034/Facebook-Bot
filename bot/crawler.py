from distutils.log import error
from turtle import pos
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import sys, os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

class Crawler: 
    def __init__(self) -> None:
       self.browser = None 
       self.group = None 
       self.posts = pd.DataFrame()

       self.data = {}
       self.action = None 
       self.__connect__()
    
    def __connect__(self):
        try:
            s = Service("./chromedriver/chromedriver")
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications" : 2}
            chrome_options.add_experimental_option("prefs",prefs)
            #chrome_options.add_argument("--headless")  # Chrome browser won't physically open on your machine 
            #chrome_options.add_argument("--no-sandbox")  # Chrome browser won't physically open on your machine 

            self.browser = webdriver.Chrome(service=s, options=chrome_options)
            self.action = ActionChains(self.browser)
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
        sleep(2)
        self.group.send_keys(Keys.END)
        sleep(2)

        

    
    def get_group_posts(self, page_loads = 5):
        i = 0 
        while True:
            # Get posts every 2 page load 
            
            self.group.send_keys(Keys.END)
            i += 1
            sleep(2)
            self.group = self.browser.find_element(by=By.TAG_NAME, value="html")
            posts = self.group.find_elements(by=By.CSS_SELECTOR, value="div.g4tp4svg.mfclru0v.om3e55n1.p8bdhjjv")
            for post in posts:
                self.analyze_post(post)
                print("---------------\n\n")
            
            if i >= page_loads:
                self.get_df_posts()

                break
        
    
    def get_df_posts(self):
        data = []

        for post in self.data:
            data.append(self.data[post])

        self.posts= pd.DataFrame(data)

        self.posts.to_csv("data.csv")
       

    def analyze_post(self, post: WebElement):
        sections = post.find_elements(by= By.CSS_SELECTOR, value=".jroqu855.nthtkgg5")
        try:
            header_section = sections[0]
            date_section = sections[1]
        except: 
            print("Cannot get the required sections")
        
        # Get author name 
        author_name = header_section.text 
        print(f"Getting post for: {author_name}")

        # Get contents 
        key, post_content = self.extract_content(author_name, post_content)
        if key in self.data:
            return 

        # Get href 
        href = self.extract_href(date_section)

         
        # Commnets 
        relative_date= None 
        try:
            comment_sections = post.find_element(by=By.CSS_SELECTOR, value=".k0kqjr44.laatuukc")
            comments_dates = comment_sections.find_elements(by= By.CSS_SELECTOR, value =".qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq.cxfqmxzd.rtxb060y.gh55jysx")
            relative_date=  comments_dates[0].text
        except:
            print("Cannot detect the comments")
        # ---end comments 

        
        self.data[key] = {
            "author": author_name,
            "content": post_content,
            "href": href,
            "relative_date": relative_date
        }



    def extract_href(self, date_section: WebElement):
        post_date_panel = date_section.find_element(by=By.CSS_SELECTOR, value=".qi72231t.nu7423ey.n3hqoq4p")
        try:
            self.action.move_to_element(post_date_panel).perform()
            sleep(1)
            href= post_date_panel.get_attribute("href")
            return href.split("?__")[0]
        except:
            print("Cannot detect date panel")

        return None     


    
    def extract_content(self, author_name, post: WebElement):
        content_section = post.find_elements(by= By.CSS_SELECTOR, value=".m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.gh25dzvf")
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
            post_content.replace('\n', " ")
        key = author_name + post_content0[0:2]

        return (key, post_content)
    

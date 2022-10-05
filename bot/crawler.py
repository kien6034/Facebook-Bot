from distutils.log import error
from turtle import pos
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import sys, os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
from bot.utils import extract_relative_date_to_timestamp
import bot.config as config

class Crawler: 
    def __init__(self) -> None:
       self.browser = None 
       self.group = None 
       self.group_name = None
       self.posts = pd.DataFrame()

       self.data = {}
       self.action = None 
       self.__connect__()
    
    def __connect__(self):
        try:
            s = Service("./bot/chromedriver/chromedriver")
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
        self.group_name = group_url
        sleep(2)
        self.group.send_keys(Keys.END)
        sleep(2)

    
    def get_group_posts(self, page_loads = 1):
        i = 0 
        while True:
            # Get posts every 2 page load 
            
            self.group.send_keys(Keys.END)
            i += 1
            sleep(2)
            self.group = self.browser.find_element(by=By.TAG_NAME, value="html")
            posts = self.group.find_elements(by=By.CSS_SELECTOR, value=".x1ja2u2z.xh8yej3.x1n2onr6.x1yztbdb")
            
            print(f"Find: {len(posts)}")
            for post in posts:
                self.analyze_post(post)
                
            
            if i >= page_loads:
                self.get_df_posts()
                break
        
    
    def get_df_posts(self):
        data = []
        for post_key in self.data:
            post_data = self.data[post_key]
            post_data["key"] = post_key
            data.append(self.data[post_key])

        self.posts= pd.DataFrame(data)
        self.posts.set_index(["key"], drop=False, inplace=True)
        self.posts.to_csv("data.csv")
       

    def analyze_post(self, post: WebElement):
        author_name, href, relative_date, exact_timestamp, exact_date_time  = self.extract_header(post)
        
        # Get contents 
        key, post_content = self.extract_content(author_name, post)
        if key in self.data:
            return 

        print(f"Analyze post of: {author_name}")
        print("---------------\n\n")
        
        self.data[key] = {
            "group": self.group_name,
            "author": author_name,
            "content": post_content,
            "href": href,
            "exact_timestamp": exact_timestamp,
            "exact_date_time": exact_date_time,
            "relative_date": relative_date
        }

  
    def quit(self):
        print("\n\n-------------------------> Closing the browser")
        self.browser.quit()

    
    def extract_content(self, author_name, post: WebElement):
        content_section = post.find_elements(by= By.CSS_SELECTOR, value=".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs")
        post_content = None 
        post_content1 = None 
        post_content0 = None

        try:
            post_content0 = content_section[0].text

            if len(content_section)> 1:
                post_content1 = content_section[1].text
            if post_content0 != "":
                post_content = post_content0
            else:
                post_content = post_content1
            if post_content != None:
                post_content.replace('\n', " ")
        except:
            pass 

       
        key = self._gen_key(author_name, post_content)
        
        return (key, post_content)
    

    def extract_header(self, post:WebElement): 
        author_name = None 
        href=  None 
        relative_date = None 
        exact_timestamp = None 
        exact_date_time = None 

        sections = post.find_elements(by= By.CSS_SELECTOR, value=".xu06os2.x1ok221b")
        try:
            header_section = sections[0]
            date_section = sections[1]

             # Get author name 
            author_name = header_section.text 
        except: 
            print("extract_header: Cannot get the header section")
        
        href = self._extract_href(date_section)

        try:
            comment_sections = post.find_element(by=By.CSS_SELECTOR, value=".x1jx94hy.x12nagc")
            relative_date, exact_timestamp, exact_date_time = self._extract_relative_date(comment_sections)
        except:
            print("extract_header: Cannot detect the comment section")

        return author_name, href, relative_date, exact_timestamp, exact_date_time 

    
    def _extract_relative_date(self, comment_sections: WebElement):
        
        relative_date = None 
        try:
            comments_dates = comment_sections.find_elements(by= By.CSS_SELECTOR, value =".x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xi81zsa.x1fcty0u")
            relative_date =  comments_dates[0].text 
        except:
            print("_extract_relative_date: Cannot get the comment dates")

        exact_timestamp, exact_date_time = extract_relative_date_to_timestamp(relative_date)
        return relative_date, exact_timestamp, exact_date_time
    
    def _extract_href(self, date_section: WebElement):
        try:
            post_date_panel = date_section.find_element(by=By.CSS_SELECTOR, value=".x193iq5w.xeuugli.x13faqbe.x1vvkbs")
            self.action.move_to_element(post_date_panel).perform()
            sleep(1)
            href= post_date_panel.get_attribute("href")
            return href
            
        except:
            return None 


    def _gen_key(self, author_name, post_content):
        try: 
            return author_name + "__" + post_content[0:2]
        except:
            return "" 


    def go_to_post(self, url):
        self.browser.get(url) 

    def _upload_image(self):
        sections = self.browser.find_elements(by=By.CSS_SELECTOR, value=".x1mnrxsn.x1w0mnb.x1rg5ohu")
        upload_section = sections[2]
        image_input = upload_section.find_element(by=By.TAG_NAME, value="input")
        image_input.send_keys(config.IMAGE_PATH)


    def comment(self):
        text_box = self.browser.find_element(by=By.XPATH, value='//div[@aria-label="Viết bình luận"]')
        self._upload_image()
        text_box.send_keys(" a 😃😃 This is a comment from bot ")
        sleep(2)
        text_box.click()
        sleep(1)
        elm = text_box.find_element(by=By.XPATH,value='//span[@data-lexical-text="true"]' )
        elm.send_keys(Keys.ENTER)

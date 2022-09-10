from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import sys, os
from dotenv import load_dotenv
load_dotenv()

s = Service("./chromedriver/chromedriver")
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)


browser = webdriver.Chrome(service=s, options=chrome_options)
browser.get("https://facebook.com")



# Logging in 
username = os.environ.get("FB_USERNAME")
password = os.environ.get("FB_PASSWORD")

txtUser = browser.find_element(by=By.ID, value="email")
txtUser.send_keys(username)
txtPass = browser.find_element(by=By.ID, value="pass")
txtPass.send_keys(password)
txtPass.send_keys(Keys.ENTER)

sleep(3)

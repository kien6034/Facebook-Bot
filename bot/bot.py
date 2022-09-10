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
# Go to pages 
browser.get("https://www.facebook.com/groups/GhienPhuQuoc")
elm = browser.find_element(by=By.TAG_NAME, value="html")

# Scroll down 
elm.send_keys(Keys.END)
sleep(1)
elm.send_keys(Keys.END)
sleep(3)


posts = elm.find_elements(by=By.CSS_SELECTOR, value="div.g4tp4svg.mfclru0v.om3e55n1.p8bdhjjv")
print(f"{len(posts)} posts found \n")

for post in posts:
    
    header = post.find_element(by=By.CLASS_NAME, value="cgu29s5g")
    sections = post.find_elements(by= By.CSS_SELECTOR, value=".jroqu855.nthtkgg5")
    name = sections[0]
    date = sections[1]

    content = post.find_elements(by= By.CSS_SELECTOR, value=".m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.gh25dzvf")
    if len(content) > 1: 
        print(content[1].text)
    else:
        print(content[0].text)
  

    # time_panels =  header.find_elements(by= By.CLASS_NAME, value="f7rl1if4")
    # for time in time_panels:
    #     print("..")
    #     print(time.text)

    # print(name.text)
   
    # content = post.find_element(by=By.TAG_NAME, value="span")
    # print(content.text)
    #m8h3af8h l7ghb35v kjdc1dyq kmwttqpk gh25dzvf
    #print(header.text)

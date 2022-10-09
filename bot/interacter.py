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

from bot.crawler import Crawler
load_dotenv()
from bot.utils import extract_relative_date_to_timestamp
import bot.config as config

class Interacter: 
    def __init__(self, crawler:Crawler, data: pd.DataFrame) -> None:
       self.browser = crawler.browser 
       self.data = data
      
    
    def run(self):
        pass
   


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

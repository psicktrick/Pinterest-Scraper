from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time, random, socket, unicodedata
import string, copy, os
import pandas as pd
import requests
import os
import requests
import urllib.request
import copy
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import threading
from urllib.parse import urlparse
import sqlite3
from sqlalchemy import create_engine
import json

sqlite_file = '/home/psicktrick/PycharmProjects/Web_Scraper/venv/' + 'src/scraping.db'

def download(myinput, image_folder):
    for src, i in zip(myinput, list(range(1, len(myinput) + 1))):
        image_name = src.split("/")[-1]
        print('%s' % i + '/' + str(len(myinput)))
        if not os.path.isfile(image_folder + '/' + image_name):
            try:
                result = requests.get(src, allow_redirects=True)
                open(image_folder + '/' + image_name, 'wb').write(result.content)
            except:
                continue


def randdelay(a, b):
    time.sleep(random.uniform(a, b))


class Pinterest_Helper(object):

    def __init__(self, login, pw, browser):
        self.browser = browser
        self.browser.get("https://www.pinterest.com")
        emailElem = self.browser.find_element_by_name('id')
        emailElem.send_keys(login)
        passwordElem = self.browser.find_element_by_name('password')
        passwordElem.send_keys(pw)
        passwordElem.send_keys(Keys.RETURN)
        randdelay(2, 4)

    def runme(self, url, n, limit=500, max_retries=30):
        final_results = []
        previmages = []
        tries = 0

        try:
            self.browser.get(url)
            while limit > 0:
                try:
                    results = []
                    images = self.browser.find_elements_by_tag_name("img")
                    
                    if images == previmages:
                        tries += 1
                        print("{}/30 retries".format(tries))
                    else:
                        tries = 0
                    if tries > max_retries:
                        print("Maximum tries exceeded")
                        conn = sqlite3.connect(sqlite_file)
                        c = conn.cursor()
                        c.execute("UPDATE scraping SET Done = 1 WHERE url = {}".format(json.dumps(url)))
                        conn.commit()
                        conn.close()
                        self.browser.quit()
                        return final_results
                    for i in images:
                        src = i.get_attribute("src")
                        if src:
                            if src.find("/236x/") != -1:
                                src = src.replace("/236x/", "/736x/")
                        results.append(src)
                    previmages = copy.copy(images)
                    final_results = list(set(final_results + results))
                    print(len(final_results))
                    if len(final_results) >= n:
                        print('Successful')
                        conn = sqlite3.connect(sqlite_file)
                        c = conn.cursor()
                        c.execute("UPDATE scraping SET Done = 1 WHERE url = {}".format(json.dumps(url)))
                        conn.commit()
                        conn.close()
                        self.browser.quit()
                        break
                    dummy = self.browser.find_element_by_tag_name('a')
                    dummy.send_keys(Keys.END)

                    randdelay(1, 2)
                    limit -= 1
                except (StaleElementReferenceException):
                    print("StaleElementReferenceException")
                    limit -= 1
        except KeyboardInterrupt:
            return final_results
        return final_results

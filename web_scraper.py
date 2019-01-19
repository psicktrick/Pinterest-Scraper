import os
from selenium import webdriver
from urllib import parse
from pinterest_scraper import scraper as sp
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

sqlite_file = '/home/psicktrick/PycharmProjects/Web_Scraper/venv' + '/src/scraping.db'
ex_path = "/home/psicktrick/PycharmProjects/Web_Scraper/venv/"
conn = sqlite3.connect(sqlite_file)
df = pd.read_sql_query("SELECT * FROM scraping", conn)
conn.close()

for i in list(range(len(df))):
    if df.loc[i,:]['Done'] == 0:
        folder_name = df.loc[i,:]['Search term']
        url = df.loc[i,:]['url']
        print(url)
        n = df.loc[i,:]['Number']
        print(n)
        image_folder = "/home/psicktrick/PycharmProjects/Web_Scraper/venv/" + "src/scraping_2.0/" + folder_name
        if not (os.path.isdir(image_folder)):
            os.mkdir(image_folder)
        if  len(os.listdir(image_folder)) < (n+1000):
            chrome = webdriver.Chrome(executable_path=ex_path + "chromedriver")
            ph = sp.Pinterest_Helper('poojarysaurabh932@gmail.com', 'iwalrtootihek', chrome)
            images = ph.runme(url,n)
            sp.download(images, image_folder)

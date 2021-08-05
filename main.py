#_*_coding: utf-8_*_

import os, unittest, time, datetime, asyncio
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from pyrogram import Client, filters

API_ID = os.osenviron.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = Client('bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I am a bot to scrape youtube channel videos urls, just send me a youtube channel link to start scraping")

@bot.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def link_handler(bot, message):
    url = f"{message.text}" if not "dl" in message.text
    channelid = url.split('/')[4]
    #driver=webdriver.Firefox()
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
    driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver", options=chrome_options)
    driver.get(url)
    time.sleep(5)
    dt=datetime.datetime.now().strftime("%Y%m%d%H%M")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    lastheight = 0

    while True:
	    if lastheight == height:
		    break
	    lastheight = height
	    driver.execute_script("window.scrollTo(0, " + str(height) + ");")
	    time.sleep(2)
	    height = driver.execute_script("return document.documentElement.scrollHeight")

    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
	    print(i.get_attribute('href'))
            link = (i.get_attribute('href'))
	    f = open(message.text+'.list', 'a+')
	    f.write(link + '\n')
    f.close
	    result = i.get_attribute('href')
            await message.reply(f"{result}", quote=True)
    

async def dl(bot, message, result):
    if "dl" in message.text:
         input = f"{result}"



bot.run()


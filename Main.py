﻿from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
from time import sleep,localtime,time,asctime



mainUrl = "https://course.fcu.edu.tw"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.maximize_window()

# 帳號及密碼
username = 'd0409861'
password = ''

# 選課代號
classIDs = ['2865']

# 確定要搶課嗎？
grabbed = True


def login():
    browser.get(mainUrl)
    
    checkCode = 0
    cookies = browser.get_cookies()
    
    for cookie in cookies:
        if cookie['name'] == 'CheckCode':
            checkCode = cookie['value']
    
    print('驗證碼:', checkCode)

    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_UserName"]').send_keys(username)
    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_Password"]').send_keys(password)
    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_vcode"]').send_keys(checkCode)
    browser.find_element_by_xpath(
        '//*[@id="ctl00_Login1_LoginButton"]').click()

    print('登入成功')
def grabClass():
	browser.find_element_by_xpath(
    '//*[@id="ctl00_MainContent_TabContainer1_tabSelected_gvToAdd"]/tbody/tr[2]/td[1]/input').click()
	print('選課成功')


def grab():
	while True:
		if browser.current_url != mainUrl:
			break
	while classIDs :
		for classID in classIDs:
			# select
			browser.find_element_by_xpath(
				'//*[@id="ctl00_MainContent_TabContainer1_tabSelected_Label3"]').click()

			# input class ID
			browser.find_element_by_xpath(
				'//*[@id="ctl00_MainContent_TabContainer1_tabSelected_tbSubID"]').send_keys(classID)
			browser.find_element_by_xpath(
				'//*[@id="ctl00_MainContent_TabContainer1_tabSelected_gvToAdd"]/tbody/tr[2]/td[8]/input').click()

			# alert
			sleep(1)
			alert = browser.switch_to_alert()

			alertInfo = alert.text
			currentValue = int(alertInfo[10:13].strip())
			openValue = int(alertInfo[14:18].strip())
			alert.accept()
			print(asctime(localtime(time())))
			print('課程代碼:', classID)
			print('剩餘名額:', currentValue)
			print('開放名額:', openValue)
			print('\n')

			if(currentValue > 0 and grabbed):
				grabClass()
				classIDs.remove(classID)

			browser.get(browser.current_url)
	sleep(5)	
if __name__ == "__main__":
    login()
    grab()
    browser.close()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re
from dateutil import parser

driver = webdriver.Chrome()
driver.get("https://vtop.vit.ac.in/student/")
username = driver.find_element_by_name("regno")
username.clear()
username.send_keys("")
password = driver.find_element_by_name("passwd")
password.clear()
password.send_keys("")
driver.execute_script(open("./autoCaptcha.js").read())#for running javascripts on given page
password.send_keys(Keys.RETURN)
driver.get("https://vtop.vit.ac.in/student/grade.asp?sem=FS")
html = driver.page_source
soup = BeautifulSoup(html,"html.parser")
soup = soup.table
table_body = soup.find('tbody')
rows = table_body.find_all('tr')
cols = rows[0].find_all('td')
if str(cols[1].text).strip().lower()!="grade details not available":
	f = open('result.html', 'w', encoding="cp737", errors="surrogateescape")
	f.write(str(html.encode('cp737'),'cp737'))
	f.close()
else:
	print('result not declared yet')
driver.get("https://vtop.vit.ac.in/student/stud_logout.asp")
driver.close()

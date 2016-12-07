from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re
from dateutil import parser

driver = webdriver.Chrome()
driver.get("http://www.campusinteraction.com/login")
username = driver.find_element_by_name("userName")
username.clear()
username.send_keys("") #enter your username
password = driver.find_element_by_name("password")
password.clear()
password.send_keys("")		#enter your password
password.send_keys(Keys.RETURN)
driver.implicitly_wait(5)
driver.get("http://www.campusinteraction.com/viewStudentAllJobs.action?jobFetchLimit=0&isViewAllJobs=true")
#Scrapping
html = driver.page_source
soup = BeautifulSoup(html,"html.parser")
soup=soup.table
conn = sqlite3.connect('campus.sqlite')
cur = conn.cursor()
jobtype=soup.findAll('a')
jtype=list()
cname=list()
cday=list()
applyday=list()
salary=list()
count=1
datacount=1
for x in jobtype:
    if x is None:
        continue
    somestring=str(x.string).lower().strip()
    if somestring=="open" or somestring=="tba" or somestring=="closed":
        continue
    if count%2==0:
        cname.append(somestring)
    else:
        jtype.append(somestring)
    count+=1
count-=1
print('count:'+str(count/2))
count=1
datacount=1
ans=soup.find_all('span',{'class':'item'})
for element in ans:
	if count%4==2:
		strchk=str(element.get_text().replace(' ','').replace('\n',' ').replace('Salary:','').strip().lower().replace('rs.','').replace('rs','').replace(',',''))
		if re.search('permonth',strchk):
			strchk=re.sub('\D','', (strchk[0:6]))
			monthly=int(strchk)*12
			salary.append(monthly)
		else:
			salary.append(strchk)            
		datacount+=1
	elif count%4==1:
		try:
			ans=str(element.get_text().replace('Campus Date :','').rstrip().lstrip().replace('\n','')[0:26].rstrip().lstrip())        
			cday.append(parser.parse(ans).strftime('%Y-%m-%d'))
		except:
			cday.append("NULL")
	elif count%4==3:
		try:
			ans=str(element.get_text().replace('Apply Before Date :','').rstrip().lstrip().replace('\n','')[0:26].rstrip().lstrip())        
			applyday.append(parser.parse(ans).strftime('%Y-%m-%d'))
		except:
			applyday.append("NULL")
	count+=1
print('count:'+str(datacount))
for i in range(0,datacount-1):
    cur.execute('''INSERT OR IGNORE INTO company (name,type,salary,campusdate,applydate) VALUES ( ?,?,?,?,? )''', ( cname[i],jtype[i],salary[i],cday[i],applyday[i], ) )
conn.commit()
driver.execute_script("dologout()")
driver.implicitly_wait(5)
driver.close()

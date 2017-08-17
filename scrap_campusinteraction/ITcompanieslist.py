from selenium import webdriver
from selenium.webdriver.common.by import By
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
username.send_keys("") #username
password = driver.find_element_by_name("password")
password.clear()
password.send_keys("")#password
password.send_keys(Keys.RETURN)
driver.implicitly_wait(5)
driver.get("http://www.campusinteraction.com/viewStudentAllJobs.action?jobFetchLimit=0&isViewAllJobs=true")
#Scrapping
html = driver.page_source
soup = BeautifulSoup(html,"html.parser")
soup=soup.table
conn = sqlite3.connect('campus.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS `company` ( `name` TEXT , `type` TEXT, `salary` TEXT, `campusdate` DATE,`applydate` DATE, `selected` text, `shortlisted` text )''')
jobtype=soup.findAll('a')
jtype=list()
jlink=list()
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
        jlink.append(x['href'])
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

eligible=list()
i=0
selectedstudents={}
shortlistedstudents={}
print(len(jlink))
for ele in jlink:
    driver.get("http://www.campusinteraction.com/"+ele)
    flag=0
    for line in driver.find_elements_by_xpath("//label[@class='jobProfileDetail']//li"):
        if line.text.strip()=="B.Tech - All Branches are eligible" or line.text.strip()=="B.Tech-Information Technology":
            html = driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            for link in soup.findAll('a'):
                if link.has_attr("href"):
                    matchobjselect=re.match(".*showCandidate\.action\?status=S&jobId.*",link['href'])
                    matchobjshortlist = re.match(".*showCandidate\.action\?status=SL&jobId.*", link['href'])
                    if matchobjselect:
                        selectedstudents[cname[i]]=link.text.strip()
                    if matchobjshortlist:
                        shortlistedstudents[cname[i]]=link.text.strip()
            print(str(i)+' '+line.text+' '+cname[i])
            eligible.append(1)
            flag=1
            break
    if flag==0:
        eligible.append(0)
    i += 1
print(str(len(eligible)))

for i in range(0,datacount-1):
    if eligible[i]==1:
        selects=0
        shortlist=0
        if cname[i] in selectedstudents:
            selects=selectedstudents[cname[i]]
        if cname[i] in shortlistedstudents:
            shortlist=shortlistedstudents[cname[i]]
        cur.execute('''INSERT OR IGNORE INTO company (name,type,salary,campusdate,applydate,selected,shortlisted) VALUES ( ?,?,?,?,?,?,? )''', ( cname[i],jtype[i],salary[i],cday[i],applyday[i],selects,shortlist ) )
conn.commit()
driver.execute_script("dologout()")
driver.implicitly_wait(5)
driver.close()

import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from bs4 import BeautifulSoup



getusername=input('Enter username:')
getpassword=input('Enter Password:')
submissionurl='https://leetcode.com/submissions/'
loginurl='https://leetcode.com/accounts/login/'

#login
driver=webdriver.Chrome()
driver.get(loginurl)
username=driver.find_element_by_id('id_login')
username.send_keys(getusername)
password=driver.find_element_by_id('id_password')
password.send_keys(getpassword)
password.send_keys(Keys.RETURN)
solutions=list()
problem=1

#Writing index file
fileindex=open('index.md','w')
fileindex.write('**S.No.**  | **Problem Name**\n---|:---:\n')
def updateindex(problemlink,filename):
    fileindex.write(str(problem)+' | ['+filename+']('+problemlink+')\n')

#Writing solution source code in file
def getcpp(problemlink,solutionlink,filename):
    global problem
    driver.get(solutionlink)
    html = driver.page_source
    codesoup = BeautifulSoup(html, "html.parser")
    filext=codesoup.find('span',{'id':'result_language'}).text.strip().lower()
    result=codesoup.find('div', {'class':'ace_content'}).text.replace('  ','\n').replace(': ',':\n').replace('; ',';\n').replace('{','{\n').replace(') ',')\n').replace('} ','}\n')
    f=open(filename+'.'+filext,'w')
    f.write('//'+problemlink+'\n'+result)
    updateindex(problemlink,filename)
    problem+=1
    f.close()

#navigating pages
pageno=1
while(True):
    driver.get(submissionurl+'/'+str(pageno)+'/')
    pageno+=1
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    try:
        soup=soup.table.tbody
    except Exception:
        break

    for tr in soup.find_all('tr'):
        tds=tr.find_all('td')
        if tds[2].text.strip().lower()=='accepted' and tds[1].text.strip().lower() not in solutions :
            solutions.append(tds[1].text.strip().lower())
            problemlink='https://leetcode.com'+tds[1].find('a', href=True)['href']
            solutionlink='https://leetcode.com'+tds[2].find('a', href=True)['href']
            getcpp(problemlink,solutionlink,solutions[-1])

#formatting source files
os.system(' astyle  --style=allman *.cpp ')
driver.get('https://leetcode.com/accounts/logout/')
fileindex.close()
driver.close()
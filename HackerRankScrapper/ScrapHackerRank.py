from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#credentials used to log in
USERNAME = input("Enter your username:")
PASSWORD = input("Enter your password:")
# The URL used to login
HACKERRANK_LOGIN_URL = 'https://hackerrank.com/login'
#corresponding file extension to that Language
extension={"C++":".cpp","C++14":".cpp","Python 2":".py","Python 3":".py","Java 7":".java","Java 8":".java","C":".c","C#":".cs","JavaScript":".js","Oracle":".sql"}
#corresponding single line comment type in that Language
comment={"C++":"//","C++14":"//","Python 2":"#","Python 3":"#","Java 7":"//","Java 8":"//","C":"//","C#":"//","JavaScript":"//","Oracle":"//"}

#class to store each accepted solution details
class Solutions:
	#constructor
    def __init__(self, problemname,problemlink,solutionlink,language):
        self.problemname=problemname
        self.problemlink=problemlink
        self.solutionlink=solutionlink
        self.language=language

#Get firefox driver
driver = webdriver.Firefox()
#Open Hackerrank login page
driver.get(HACKERRANK_LOGIN_URL)
#get username element from page
usernameField = driver.find_element_by_css_selector('form#legacy-login input[id="login"]')
#get password element from page
passwordField = driver.find_element_by_css_selector('form#legacy-login input[id="password"]')
#enter username in input
usernameField.send_keys(USERNAME)
#enter password in input
passwordField.send_keys(PASSWORD)
#press enter
passwordField.send_keys(Keys.RETURN)
#wait to load page properly
driver.implicitly_wait(25)

#Writing index file
fileindex=open('index.md','w')
fileindex.write('**S.No.**  | **Problem Name**\n---|:---:\n')

#Method to write each entry in index file
def updateindex(problemno,problemlink,filename):
    fileindex.write(str(problemno)+' | ['+filename+']('+problemlink+')\n')

#Method to write scrapped code into file
def getfiles(filename,problemlink,solutionlink,fileext):
    #open solution page
    driver.get(solutionlink)
    data=""
    #Wait till code editor container loads properly
    WebDriverWait(driver, 100).until( EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror-lines")))
    #reading code line by line from code editor container
    for line in driver.find_element_by_class_name("CodeMirror-lines").text.split("\n"):
        #skipping line numbers and concatinating each line into a single string
        if not line.strip().isdigit():
            data+=line+"\n"
    #filtering filename ,creating and opening file in write mode
    f = open(filename.replace("\"","").replace("/","").replace("\\","").replace(":","").replace("?","").replace("*","").replace("<","").replace(">","").replace("|","")
             + extension[fileext.strip()], 'w')
    #writing data into file
    f.write(comment[fileext.strip()]+problemlink+'\n'+data)
    f.close()
#list to store accepted Solution into objects
mysubmissions=[]
pageno=1
while(True):
    #Open submissions page
    driver.get("https://www.hackerrank.com/submissions/all/page/" + str(pageno))
    #get submissions div container conataing containers of each submissions
    submissionlist=driver.find_elements_by_class_name("submissions_item")
    #if it is empty loop will exit
    if not submissionlist:
        break
    #traversing to each row and fetching data
    for row in submissionlist:
        problemname=row.find_element_by_class_name("root") #gets html element <a> containing problem name
        problemlink=problemname.get_attribute('href') #gets problem link from its attribute
        problemname=problemname.text #gets problem name
        language = row.find_element_by_class_name("small").text  # gets language like Java or C++ or C++14
        status = row.find_element_by_class_name("span3")  # get status like Accepted, Wrong Answeretc
        solution = row.find_element_by_class_name("view-results")  # gets html element <a> containing solution
        solutionlink=solution.get_attribute('href') #gets solution link from its attribute
        #Checking if status isaccepted and if it is not there in list
        if status.text=="Accepted" and  not any(x.problemname == problemname for x in mysubmissions)  :
            mysubmissions.append(Solutions(problemname,problemlink,solutionlink,language)) #creating Solutions object and adding into list
    pageno+=1 #updating page number to go to next page
#initializing problem number
problemno=1
#Opening each solution page for element in list and scrapping code and updating index file
for element in mysubmissions:
    getfiles(element.problemname,element.problemlink,element.solutionlink,element.language)
    updateindex(problemno, element.problemlink, element.problemname)
    problemno+=1
#closing file streamof index file
fileindex.close()
#closes firefox
driver.quit()
# getReviews.py

# S
# Type
# Text
# Size
# # 4 KB (3,733 bytes)
# # Storage used
# 0 bytesOwned by University of Moratuwa
# Location
# Scraping
# Owner
# U.W.C.S. GUNASEKARA
# Modified
# Oct 9, 2020 by U.W.C.S. GUNASEKARA
# Opened
# 10:36 AM by me
# Created
# Oct 9, 2020
# Add a description
# Viewers can download
#!/usr/bin/env python
# coding: utf-8

# In[176]:

import time
import requests
import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

maxcount = 30
filename = ""
TIMEOUT = 5

driver = webdriver.Chrome("chromedriver.exe")

# In[177]:


def writecsv(c1,c2,c3,c4,c5,c6,c7,c8):
    with open(filename, mode='a',newline='') as f:
        #keys = ['name', 'age', 'job', 'city']
        writer = csv.writer(f)
        writer.writerow([str(c1),str(c2),str(c3),str(c4),str(c5),str(c6),str(c7),str(c8)])
         
       
        


# In[178]:


def getattributes(review):
    try:
        name = review.find(class_="ui_header_link _1r_My98y").parent.get_text() if review.find(class_="ui_header_link _1r_My98y").parent else ""
        userUrl = review.find(class_="ui_header_link _1r_My98y").parent.find('a',href=True)['href']
        city = review.find(class_="default _3J15flPT small").get_text() if review.find(class_="default _3J15flPT small") else ""
        contribution = review.find(class_="_3fPsSAYi").get_text() if review.find(class_="_3fPsSAYi") else ""
        reviewTitle = review.find("div", attrs={"data-test-target":"review-title"}).get_text() if review.find("div", attrs={"data-test-target":"review-title"}) else ""
        reviewUrl = review.find("div", attrs={"data-test-target":"review-title"}).find('a',href=True)['href']
        reviewDetail = review.find(class_="cPQsENeY").get_text() if review.find(class_="cPQsENeY") else ""
        exDate = review.find(class_="_34Xs-BQm").get_text() if review.find(class_="_34Xs-BQm") else ""
        # rate = review.find(class_="ui_bubble_rating bubble_50").get_text() if review.find(class_="ui_bubble_rating bubble_50") else ""
        
        writecsv(name,userUrl,city,contribution,reviewTitle,reviewUrl,reviewDetail,exDate)
        
    except :
        print('error')


# In[179]:


def getreviesGivenpageUrl(URL):    
    driver.get(URL)
    
    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//*[@class='_3maEfNCR']"))
        WebDriverWait(driver, TIMEOUT*5).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    
    time.sleep(TIMEOUT)
    view_more = driver.find_element_by_xpath("//*[@class='_3maEfNCR']");
    view_more.click()
    
    time.sleep(TIMEOUT)
    html_content = driver.page_source
    html = BeautifulSoup(html_content, 'html.parser')
    body = html.find('body')   
    
    searchreview=body.find("input", attrs={"placeholder":"Search reviews"}).parent
    review = searchreview
    for el in range(5):
        try:
            getattributes(review.find_next_sibling('div'))
            review = review.find_next_sibling('div')
        except:
            print('review not found')
            break


# In[180]:


def getallReviewsBymainUrl(URL):
    #get the name of place for csv file name
    global filename 
    filename = re.search('(.*)Reviews-(.*).html', URL).group(2)+'.csv'
    print('start to fill '+filename)

    #open csv file and add titles
    with open(filename, mode='w') as f:
            writer = csv.writer(f)
            writer.writerow([str('user name'),str('user Url'),str('city'),str('Contribution'),str('review Title'),str('review Url'),str('Review Details'),str('expe date')])



    #get count, could be maximum
    page = requests.get(URL)
    html = BeautifulSoup(page.content, 'html.parser')
    count = html.find('body').find_all(class_="pageNum cx_brand_refresh_phase2")[-1].get_text()

    #change maximum end count
    endcount = int(maxcount) if int(count) > int(maxcount) else int(count) 

    #get and save reviews in csv file
    for i in range(1,endcount):
        getreviesGivenpageUrl(URL.replace('Reviews','Reviews-or'+str(i*5)))
        print('save reviews in page = ',str(i))

    #finished reviews and saved all
    print('finished' + filename)
    print()


# In[181]:
# read url csv
# with open('test_urls.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')

#     URLs = []

#     for urls in readCSV:
#         urlarray = urls[0]

#         URLs.append(urlarray)

#     print(URLs)

URLs = [
    '',
    '',
    ''
]
for url in URLs:
    getallReviewsBymainUrl(url)
        
print()       
print('program is end, Thank you.')
driver.quit()






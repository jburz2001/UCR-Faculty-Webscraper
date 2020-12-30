import requests    #here just in case
from bs4 import BeautifulSoup    #web scrapes


from selenium import webdriver    #engine that navigates Chrome
from selenium.webdriver.common.keys import Keys    #enables button presses and clicks
import time    #enables delays

from selenium.webdriver.common.by import By    #the following enable webdriver to check if button clickable
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

import numpy as np    #here just in case
import pandas as pd    #dataframe





PATH = "C:\Program Files (x86)\chromedriver.exe"    #path to webdriver executable
wd = webdriver.Chrome(PATH)

wd.get("https://profiles.ucr.edu/app/home/search;name=;org=Physics%20and%20Astronomy;title=;phone=;affiliation=Faculty")    #opens initial page
wait=WebDriverWait(wd, 10)    #enables wd waiting
time.sleep(1)    #delays program so that innerHTML can load
        
body = wd.find_element_by_tag_name('body')
bodyInner = body.get_attribute('innerHTML')    #scrapes JS-generated HTMl from <body>

soup = BeautifulSoup(bodyInner)
searchResults = soup.find(id='searchResults')
row = searchResults.div.div.div.contents[2]    #navigates down #searchresults DOM to find "row" where each person is a "col" of data

people = row.find_all('div', {'class':'column'})    #sorts each person of webpage into list
numPeople = len(people)

columnTitles = ['Name', 'Position', 'Department', 'Research Areas', 'Location', 'Phone Number', 'Email']
df = pd.DataFrame({
    'Name':['!'], 
    'Position':['!'],
    'Department':['!'], 
    'Research Areas':['!'], 
    'Location':['!'], 
    'Phone Number':['!'], 
    'Email':['!'], 
    #'URL':['!']
})    #defines default df to be appended to

for person in people:    #iterates through all people on page

    testDict = {
        'Name':'', 
        'Position':'',
        'Department':'', 
        'Research Areas':'', 
        'Location':'', 
        'Phone Number':'', 
        'Email':'', 
        #'URL':''
    }    #creates container for person data

    testDict['Name'] = person.h5.text    # Name <- text in the first h5

    positionList = person.find('ul', {'class':'border-separated-list'}).find_all('li')
    positions = ''
    i = 0
    for position in positionList:    #iterates through list of positions and concatenates the str's
        if (i != len(positionList) - 1):
            positions = positions + position.text + ', '
        else:
            positions = positions + position.text
        i += 1
    testDict['Position'] = positions

    otherContentRegions = person.find_all('div', {'class': 'content-detail'})    #locates collection of Dept, Location, Phone, and Email

    testDict['Department'] = otherContentRegions[0].span.text    #dept <- text of first element in otherContentRegions

    try:    #try to concatenate research areas into single str
        researchAreas = person.find('ul', {'class':'comma-separated'}).find_all('li')
        areas = ''
        k = 0
        for area in researchAreas:
            if (k != len(researchAreas) - 1):
                areas = areas + str(area.text) + ', '
            else:
                areas = areas + str(area.text)
            k += 1
        testDict['Research Areas'] = areas

    except AttributeError:    #research <- NOT STATED if it cannot be found
        testDict['Research Areas'] = 'NOT STATED'


    try:    #try to include location, phone, and email into df
        testDict['Location'] = otherContentRegions[1].span.text
        testDict['Phone Number'] = otherContentRegions[2].span.text
        testDict['Email'] = otherContentRegions[3].span.text

    except IndexError:    #if not all that data is present, populate df differently
        if (len(otherContentRegions) == 4):
            testDict['Location'] = 'NOT STATED'
            testDict['Phone Number'] = otherContentRegions[1].span.text
            testDict['Email'] = otherContentRegions[2].span.text
            
        elif (len(otherContentRegions) == 3):
            testDict['Location'] = 'NOT STATED'
            testDict['Phone Number'] = otherContentRegions[1].span.text            
            testDict['Email'] = otherContentRegions[2].span.text
            
        elif (len(otherContentRegions) == 2):
            testDict['Location'] = 'NOT STATED'
            testDict['Phone Number'] = 'NOT STATED'            
            testDict['Email'] = otherContentRegions[1].span.text

    testDf = pd.DataFrame({
        'Name':[testDict['Name']], 
        'Position':[testDict['Position']],
        'Department':[testDict['Department']], 
        'Research Areas':[testDict['Research Areas']], 
        'Location':[testDict['Location']], 
        'Phone Number':[testDict['Phone Number']], 
        'Email':[testDict['Email']], 
        #'URL':[testDict['URL']]
    })    #populate temporary df

    df = df.append(testDf, ignore_index=True)    #append temporary df to permanent df


while True:    #while Next page button is clickable
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next page']"))).click()    #click <a> to get to next page
        time.sleep(1)
        wait=WebDriverWait(wd, 10)
        
        body = wd.find_element_by_tag_name('body')
        bodyInner = body.get_attribute('innerHTML')

        soup = BeautifulSoup(bodyInner)
        searchResults = soup.find(id='searchResults')
        row = searchResults.div.div.div.contents[2]


        people = row.find_all('div', {'class':'column'})
        numPeople = len(people)
        
        for person in people:    #web scrape people data like before

            testDict = {
                'Name':'', 
                'Position':'',
                'Department':'', 
                'Research Areas':'', 
                'Location':'', 
                'Phone Number':'', 
                'Email':'', 
                #'URL':''
            }

            testDict['Name'] = person.h5.text

            positionList = person.find('ul', {'class':'border-separated-list'}).find_all('li')
            positions = ''
            i = 0
            for position in positionList:
                if (i != len(positionList) - 1):
                    positions = positions + position.text + ', '
                else:
                    positions = positions + position.text
                i += 1
            testDict['Position'] = positions

            otherContentRegions = person.find_all('div', {'class': 'content-detail'})

            testDict['Department'] = otherContentRegions[0].span.text

            try:
                researchAreas = person.find('ul', {'class':'comma-separated'}).find_all('li')
                areas = ''
                k = 0
                for area in researchAreas:
                    if (k != len(researchAreas) - 1):
                        areas = areas + str(area.text) + ', '
                    else:
                        areas = areas + str(area.text)
                    k += 1
                testDict['Research Areas'] = areas

            except AttributeError:
                testDict['Research Areas'] = 'NOT STATED'


            try:
                testDict['Location'] = otherContentRegions[1].span.text
                testDict['Phone Number'] = otherContentRegions[2].span.text
                testDict['Email'] = otherContentRegions[3].span.text

            except IndexError:
                if (len(otherContentRegions) == 4):
                    testDict['Location'] = 'NOT STATED'
                    testDict['Phone Number'] = otherContentRegions[1].span.text
                    testDict['Email'] = otherContentRegions[2].span.text
                elif (len(otherContentRegions) == 3):
                    testDict['Location'] = 'NOT STATED'
                    testDict['Phone Number'] = otherContentRegions[1].span.text            
                    testDict['Email'] = otherContentRegions[2].span.text
                elif (len(otherContentRegions) == 2):
                    testDict['Location'] = 'NOT STATED'
                    testDict['Phone Number'] = 'NOT STATED'            
                    testDict['Email'] = otherContentRegions[1].span.text

            testDf = pd.DataFrame({
                'Name':[testDict['Name']], 
                'Position':[testDict['Position']],
                'Department':[testDict['Department']], 
                'Research Areas':[testDict['Research Areas']], 
                'Location':[testDict['Location']], 
                'Phone Number':[testDict['Phone Number']], 
                'Email':[testDict['Email']], 
                #'URL':[testDict['URL']]
            })

            df = df.append(testDf, ignore_index=True)
                
    except:    #quit Chrome and break loop when <a> cannot be clicked
        wd.quit() 
        break

df = df.iloc[1:]   #remove row of '!' from permanent df
print('Done')


display(df)
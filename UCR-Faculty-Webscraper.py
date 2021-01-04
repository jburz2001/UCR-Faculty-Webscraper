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

import nltk






"""
FUNCTIONS
"""

def getSoupAtCurrUrl():
    body = wd.find_element_by_tag_name('body')
    bodyInner = body.get_attribute('innerHTML')
    soup = BeautifulSoup(bodyInner)

    return soup

#Currently returns last person
def returnPersonDf(person):
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


    return testDf


"""
PROGRAM
"""

PATH = "C:\Program Files (x86)\chromedriver.exe"    #path to webdriver executable
wd = webdriver.Chrome(PATH)
url = 'https://profiles.ucr.edu/app/home/search;name=;org=Physics%20and%20Astronomy;title=;phone=;affiliation=Faculty'

wd.get(url)    #opens initial page
wait = WebDriverWait(wd, 10)    #enables wd waiting
time.sleep(1)    #delays program so that innerHTML can load

soup = getSoupAtCurrUrl()

searchResults = soup.find(id='searchResults')
row = searchResults.div.div.div.contents[2]    #navigates down #searchresults DOM to find "row" where each person is a "col" of data

people = row.find_all('div', {'class':'column'})    #sorts each person of webpage into list

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

for person in people:
    testDf = returnPersonDf(person)
    df = df.append(testDf, ignore_index=True)    #append temporary df to permanent df


while True:    #while Next page button is clickable
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next page']"))).click()    #click <a> to get to next page
        time.sleep(1)
        
        soup = getSoupAtCurrUrl()
        searchResults = soup.find(id='searchResults')
        row = searchResults.div.div.div.contents[2]


        people = row.find_all('div', {'class':'column'})
        
        for person in people:
            testDf = returnPersonDf(person)
            df = df.append(testDf, ignore_index=True)    #append temporary df to permanent df
                
    except:    #quit Chrome and break loop when <a> cannot be clicked
        wd.quit() 
        break

df = df.iloc[1:]   #remove row of '!' from permanent df
print('Done')



dfCopy = df.copy()
display(dfCopy)



import random
import nltk
from nltk.corpus import names
from nltk.tokenize import SpaceTokenizer


#nltk.download()

tk = SpaceTokenizer()



def gender_features(word):
    return {'last_letter':word[-1]}

# preparing a list of examples and corresponding class labels. 
labeled_names = (
    [(name, 'male') for name in names.words('male.txt')] +
    [(name, 'female') for name in names.words('female.txt')]
    ) 
  
random.shuffle(labeled_names) 
  
# we use the feature extractor to process the names data. 
featuresets = [
    (gender_features(n), gender) for (n, gender) in labeled_names
    ] 
  
# Divide the resulting list of feature 
# sets into a training set and a test set. 
train_set = featuresets[2000:] 
test_set = featuresets[:2000] 
  
# The training set is used to  
# train a new "naive Bayes" classifier. 
classifier = nltk.NaiveBayesClassifier.train(train_set) 
  
print(classifier.classify(gender_features('Sandra'))) 
  
# output should be 'male' 
#print(nltk.classify.accuracy(classifier, train_set)) 
  
# it shows accurancy of our classifier and  
# train_set. which must be more than 99 %  

#classifier.show_most_informative_features(10) 

numF, numM = 0, 0
genderVal = 0
for fullName in dfCopy['Name']:
    tokFullName = tk.tokenize(fullName)
    if (classifier.classify(gender_features(tokFullName[0])) == 'female'):
        numF += 1
        genderVal -= 1
    else:
        numM += 1
        genderVal += 1
        
tempGDict = {'Department':[dfCopy['Department'].iloc[0]], 'Females':[numF], 'Males':[numM], 'Gender Value':[genderVal], 'Gender Ratio':[numF/numM]}
tempGDf = pd.DataFrame.from_dict(tempGDict)
display(tempGDf)

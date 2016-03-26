# internal libraries
import os

# external libraries
from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

def getCards(inputUrl):
    cardDict = {}
    cardDict['questions'] = []
    cardDict['answers'] = []
    # set up beautiful soup
    r = requests.get(inputUrl)
    soup = BeautifulSoup(r.content, "html.parser")

    # pull term data
    termTag = soup.find_all("span",{"class": "TermText qWord lang-en"})
    for item in termTag:
        cardDict['questions'].append(item.text)

    defTag = soup.find_all("span",{"class": "TermText qDef lang-en"})
    for item in defTag:
        cardDict['answers'].append(item.text)

    possibleAnswers = 0
    for x in xrange(0,len(cardDict['questions'])):
        if int(fuzz.token_set_ratio(inputQuestion.lower(), cardDict['questions'][x].lower())) > 90:
            print("\n")
            print(cardDict['questions'][x])
            print(cardDict['answers'][x])
            possibleAnswers += 1
    if possibleAnswers == 0:
        print("\nNo possible answers found.")
        return {}
    else:
        return cardDict

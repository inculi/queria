# internal libraries
import os

# external libraries
from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

def getURLs(searchString,answerAmount):
    if answerAmount == 0:
        urls = []
        for url in search(searchString + " site:quizlet.com", stop=3):
            if len(urls) < 3: # The top three should suffice.
                print(url)
                urls.append(url)
            else:
                break
        return urls
    else:
        urls = []
        for url in search(searchString + " -filetype:pdf -filetype:docx -filetype:doc -filetype:pptx -filetype:ppt -site:youtube.com -site:wikipedia.org -site:books.google.com -site:vimeo.com", stop=20):
            # Wikipedia returns multiple options under their links, each to a
            # different section of the same page... We only need one of these links.
            if "en.wikipedia.org/wiki/" or "#" or "://books.google.com/books" or "www.youtube.com/" or "vimeo.com/" not in url:
                urls.append(url)
        return urls

def parsePage(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    pageContent = soup.find_all("p") # find the text of the page

    for paragraph in pageContent:
        paragraphText = paragraph.text.replace("\n","")
        # print(paragraphText)
        # print fuzz.token_set_ratio(inputQuestion, paragraphText)
        if int(fuzz.token_set_ratio(inputQuestion.lower(), paragraphText.lower())) > 50:
            # print paragraphText
            paragraphTexts.append(paragraphText)

def getCards(inputUrl):
    questions = []
    answers = []
    # set up beautiful soup
    r = requests.get(inputUrl)
    soup = BeautifulSoup(r.content, "html.parser")

    # pull term data
    termTag = soup.find_all("span",{"class": "TermText qWord lang-en"})
    for item in termTag:
        questions.append(item.text)

    defTag = soup.find_all("span",{"class": "TermText qDef lang-en"})
    for item in defTag:
        answers.append(item.text)

    possibleAnswers = 0
    for x in xrange(0,len(questions)):
        if int(fuzz.token_set_ratio(inputQuestion.lower(), questions[x].lower())) > 90:
            print("\n")
            print(questions[x])
            print(answers[x])
            possibleAnswers += 1
    if possibleAnswers == 0:
        print("\nNo possible answers found.")

def getMassCards(inputUrl,currentQuestion):
    questions = []
    answers = []
    # set up beautiful soup
    r = requests.get(inputUrl)
    soup = BeautifulSoup(r.content, "html.parser")

    # pull term data
    termTag = soup.find_all("span",{"class": "TermText qWord lang-en"})
    for item in termTag:
        questions.append(item.text)

    defTag = soup.find_all("span",{"class": "TermText qDef lang-en"})
    for item in defTag:
        answers.append(item.text)

    possibleAnswers = 0
    for x in xrange(0,len(questions)):
        if int(fuzz.token_set_ratio(currentQuestion.lower(), questions[x].lower())) > 90:
            print("Found an answer for \"" + str(questions[x])[:10] + "...\"")
            answerFile.write(questions[x]+"\n\n")
            answerFile.write(answers[x])
            possibleAnswers += 1

# ============================   MAIN FUNCTION   ===============================

questionFile = open("questions.txt","r")
answerFile = open("answers.txt",'w')

inputQuestions = [question.replace("\n","") for question in questionFile]
print inputQuestions # verify for debugging

questionFile.close() # I not longer need the file, as I imported all of them
                     # into a list already...

relevantUrls = [] # create a list to store relevant urls.

# begin the search.
print("\nSearching...")
for question in inputQuestions:
    # get the 3 quizlet links for the question
    for item in getURLs(question,0):
        relevantUrls.append(item)

relevantUrls = list(set(relevantUrls)) # remove the duplicates, as we don't need
                                       # to visit the same page mult. times.

print("\nNow that we have the links, we can answer the questions...")
for question in inputQuestions:
    print(question)
    for url in relevantUrls:
        getMassCards(url,question)

# ==========================   END MAIN FUNCTION   =============================

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
            import subprocess
            command = "wc -l answers.txt | awk '{print $1}'"
            output = int(str(subprocess.check_output(command, shell=True)).replace("\n",""))
            if output is not 0:
                print("Output is not Zero!!!")
                answerFile.write("\n"+questions[x]+"\n")
                answerFile.write(answers[x])
                possibleAnswers += 1
            else:
                answerFile.write(questions[x]+"\n")
                answerFile.write(answers[x])
                possibleAnswers += 1

try:
    questionFile = open("questions.txt","r")
    answerFile = open("answers.txt",'w')
except:
    print("You do not have files:\n - questions.txt\n - answers.txt\nin your directory. Making them now...")
    os.system("rm *.txt; touch answers.txt questions.txt")
    print("Go back and add questions to questions.txt, please.\nExiting now...")
    exit()

# open the question and answer files
# questionFile = open("questions.txt","r")
# answerFile = open("answers.txt",'w')

# place the questions into a list
inputQuestions = [question.replace("\n","") for question in questionFile]

# verify for debugging
print inputQuestions

# begin the search.
relevantUrls = []
print("\nSearching...")
for question in inputQuestions:
    # get the 3 quizlet links for the question
    for item in getURLs(question,0):
        relevantUrls.append(item)

relevantUrls = list(set(relevantUrls)) # remove the duplicates

for question in inputQuestions:
    print(question)
    for url in relevantUrls:
        getMassCards(url,question)

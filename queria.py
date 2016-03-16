# external libraries
from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

def getURLs(searchString):
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
        for url in search(searchString + " -filetype:pdf -filetype:docx -filetype:doc -filetype:pptx -filetype:ppt", stop=20):
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
            print questions[x]
            print answers[x]
            possibleAnswers += 1
    if possibleAnswers == 0:
        print("No possible answers found.")

# =========================   BEGIN MAIN FUNCTION   ============================
# ==========================   PRIMARY VARIABLES   =============================
# VARIABLES FOR THE PURPOSE OF DEBUGGING...

# inputQuestion = "The majority of cases heard by federal courts begin in"
# answerAmount = 5
# answers = ["district courts", "state courts", "municipal courts", "appellate courts", "circuit courts"]

# NORMALLY USED VARIABLES...

inputQuestion = raw_input("What is your question?\n > ")
answerAmount = int(raw_input("How many possible answers do you know?\n > "))

if answerAmount == 0:
    print("\nSearching...")
    urls = getURLs(inputQuestion)

    for url in urls:
        getCards(url)

else:
    answers = []
    for x in xrange(0,answerAmount):
        answers.append(raw_input("Please input answer " + str(x+1) + "\n > "))
    # ========================   END PRIMARY VARIABLES   ===========================

    print("\nSearching...")
    searchURLs = getURLs(inputQuestion)

    paragraphTexts = []

    for url in searchURLs:
        print(url)
        parsePage(url)
    print("\n") # make some room

    scores = [0] * answerAmount

    for x in xrange(0,len(answers)):
        for paragraph in paragraphTexts:
            scores[x] += paragraph.lower().count(answers[x].lower())

    print("Scores:")
    for x in xrange(0,len(answers)):
        print answers[x]
        print scores[x]
        print("\n")
# ==========================   END MAIN FUNCTION   =============================

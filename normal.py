from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein
from queria import *

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
    urls = getURLs(inputQuestion,answerAmount)

    for url in urls:
        getCards(url)

else:
    answers = []
    for x in xrange(0,answerAmount):
        answers.append(raw_input("Please input answer " + str(x+1) + "\n > "))
    # ========================   END PRIMARY VARIABLES   ===========================

    print("\nSearching...")
    searchURLs = getURLs(inputQuestion,answerAmount)

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

# external libraries
from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

def getURLs(searchString):
    urls = []
    for url in search(searchString + " -filetype:pdf -filetype:docx -filetype:doc -filetype:pptx -filetype:ppt", stop=20):
        # Wikipedia returns multiple options under their links, each to a
        # different section of the same page... We only need one of these links.
        if "en.wikipedia.org/wiki/" and "#" and "://books.google.com/books" and "www.youtube.com/" and "vimeo.com/" not in url:
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
        if int(fuzz.token_set_ratio(inputQuestion, paragraphText)) > 50:
            # print paragraphText
            paragraphTexts.append(paragraphText)

# =========================   BEGIN MAIN FUNCTION   ============================
# inputQuestion = "The majority of cases heard by federal courts begin in"
# answerAmount = 4
# answers = ["district courts", "state courts", "municipal courts", "appellate courts", "circuit courts"]
inputQuestion = raw_input("What is your question?\n > ")
answerAmount = int(raw_input("How many possible answers do you know?\n > "))

answers = []
for x in xrange(0,answerAmount):
    answers.append(raw_input("Please input answer " + str(x+1) + "\n > "))

# print(answers)

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

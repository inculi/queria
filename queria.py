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
        if "en.wikipedia.org/wiki/" and "#" not in url:
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
inputQuestion = "The majority of cases heard by federal courts begin in"
answerAmount = 4
answers = ["district courts", "state courts", "municipal courts", "appellate courts", "circuit courts"]
searchURLs = getURLs(inputQuestion)

paragraphTexts = []

for url in searchURLs:
    print(url)
    parsePage(url)
print("\n") # make some room

scores = [0,0,0,0,0]

for x in xrange(0,len(answers)):
    for paragraph in paragraphTexts:
        scores[x] += paragraph.count(answers[x])

print("Scores:")
for x in xrange(0,len(answers)):
    print answers[x]
    print scores[x]
    print("\n")
# ==========================   END MAIN FUNCTION   =============================

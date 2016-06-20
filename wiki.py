# internal libraries
import os

# external libraries
import requests
from bs4 import BeautifulSoup

import wikipedia
from google import search

import Levenshtein
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

import nltk
nltk.data.path.append("/Volumes/Archive/Software/Programming Dependencies/nltk_data/")


def printAll(myList):
    for item in myList:
        print item

def wikiSearch(searchString):
    urls = []
    for url in search(searchString + " site:wikipedia.org", stop=10):
        # we only want three urls.
        # 'relevant' wikipedia sub-urls have '?sa=X&ved=' in them... filter that
        if (len(urls) < 3) and ("?sa=X&ved=" not in url):
            urls.append(url)

    urls.reverse() # order the links according to how they appear in google
    return urls

### TOPIC FINDING

def findTopic(url):
    # for wikipedia urls
    if 'wikipedia.org/wiki/' in url:
        # I cut the 'https://en.' out of this, as google occasionally links wiki
        # articles from their 'simple' subdomain, causing the topics to be
        # returned as NoneType.
        topic = url.rsplit("wikipedia.org/wiki/",1)[1]

        # filter out misc. characters from its url.
        topic = topic.replace("_"," ").lower()
        return topic
    else:
        print("""This is not an article from wikipedia, or it is under a\
         strange subdomain.""")

def findModeTopic(inputList):
    """
    Given a list of url titles, we are to find the reoccuring theme between
    all of the titles.

    Example input:
        - List of cities in Sweden,
        - Stockholm,
        - History of Stockholm
    Example output:
        - Stockholm
    """
    # Create a list of lists to hold each topic.
    wordList = []
    sentenceWords = [] # a list of words tokenized by space

    for topic in inputList:
        for item in [str(text.lower()) for text in topic.split(" ")]:
            sentenceWords.append(item)
    # print(sentenceWords)

    """
    Now that we have a list of the words that are in the colleciton of titles,
    all that we need to is find the word(s) that are repeated the most...

    This can be done by using the count() function on a list.
    """

    wordCounts = {i:sentenceWords.count(i) for i in sentenceWords}
    # print(wordCounts)

    """
    Now that we have a dictionary with a list of the word counts for all the
    titles, we can printout the sorted list by occurrence...
    """
    for x in xrange(0,len(wordCounts)):
        # .get is used as a key in order to find the max value, as otherwise
        # the alphabetically largest item name is returned...
        topWord = max(wordCounts, key=wordCounts.get)
        print(topWord + " : " + str(wordCounts[topWord]))
        del wordCounts[topWord]

### ARTICLE READING
def readArticle(url,inputQuestion):
    """
    I want this to read the article and return a dictionary of the following
    elements:
        - relevant sentences (according to my question)
        - relevant articles (according to the hyperlinks in the sentences)
        - accuracy rating (according to the returned token set ratios)
            - I don't think an average will suffice for this part.
    """
    # download the page and store its filtered content
    topic = url.rsplit("wikipedia.org/wiki/",1)[1]
    pageText = wikipedia.WikipediaPage(topic).content

    # break the page into sentences for sifting through.
    pageSentences = nltk.sent_tokenize(pageText)
    relevantSents = [] # a dictionary which shall store the sentence and score
    for item in pageSentences:
        score = int(fuzz.token_set_ratio(inputQuestion.lower(), item.lower()))
        if score > 80:
            relevantSents.append((item, score))

    if relevantSents != []:
        # for item in relevantSents:
        #     print item
        print("Using " + url)
        return relevantSents
    else:
        print("There are no relevant sentences above the 80% threshold.")
        return []

def answerQuestion(questionString):
    urls = wikiSearch(questionString)
    paragraph = u'' # the paragraph we are going to build with the data
    sentences = []

    for url in urls:
        tempSents = readArticle(url,questionString)
        tempSents.sort(reverse=True)
        if len(tempSents) != 0:
            for item in tempSents:
                sentences.append(item[0])

    for sentence in sentences:
        paragraph += sentence + " "

    print("\n") # make some room
    print(paragraph)

# ============================   MAIN FUNCTION   ===============================
if __name__ == "main":
    print("Ready for some debugging, eh?")
elif __name__ == "wiki":
    inputQuestion = raw_input("\n What is your question?\n\n > ")
    print("\nSearching...")
    answerQuestion(inputQuestion)
# ==========================   END MAIN FUNCTION   =============================



# ==============================   DEBUGGING   =================================
# ============================   END DEBUGGING   ===============================

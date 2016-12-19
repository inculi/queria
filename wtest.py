# internal libraries
import os
import re

# external libraries
from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

"""We'll do some basic string matching between wikipedia's normal page for an
article along with their "simple.wikipedia" page to see some of the differences.

As of now, it seems that the main difficulty is in the complexity of wikipedia's
formatting... Or, rather, the fickleness of its user-editors when choosing a
formatting style. I figure the best way to have it scrape 2-3 paragraphs
initially, and then shorten these down to a proper, usable length whether that
be by removing all of the list-like elements and ridiculous bullet points or just

"""
class wurl:
    @staticmethod
    def simple(urlSuffix):
        return "https://simple.wikipedia.org" + urlSuffix

    @staticmethod
    def normal(urlSuffix):
        return "https://en.wikipedia.org" + urlSuffix

def scrapeWiki(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    articleurls = [str(item.get('href')) for item in soup.find_all("a")]
    return articleurls

def scrapeParagraph(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # remove tables and disambiguiation notices.
    try:
        soup.find("div", attrs={"class":"hatnote"}).extract()
    except:
        pass
    try:
        soup.find("table").extract()
    except:
        pass

    pIndex = 0
    body_tag = soup.select("div#mw-content-text > p")
    if len(body_tag) == 0:
        print("DNE: " + url) # Page does not exist.
        return ""
    for p in body_tag:
        if len(p.contents) <= 1:
            """
            paragraphs/sent will be full of content, and will have multiple
            words/word objects wrapped in <b>,<i>,<s>, etc.
            Abnormal <p>'s will only have one <span> full of unorganized content
            Thus, their content length will be <=1.
            """
            # print("WARNING: LITTLE CONTENT FOR:")
            # print(p.text)
        if p.next_element.name == u'span':
            """
            Check for abnormal <span>s at the beginning. Etymology may mess this
            up, but hopefully it won't matter that much.
            """
            # print("WARNING: STRANGE FORMATTING FOR:")
            # print(p.text)
        elif ((len(p.contents) <= 1) and (p.next_element.name == u'span')) == False:
            # we have now find a paragraph that works. Let's clean it up and
            # return it to the user.
            # print(u"\nWe chose to go with: " + p.text[0:60]+"...\n")
            if pIndex is not 0:
                print("Using <p> #"+str(pIndex+1)+" for "+url)

            paragraph = removeBrackets(p.text)
            return paragraph
        pIndex += 1
    # if it made it to down here, the page data is messed
    print("DATA ERROR: " + url) # up or there is an error
    return ""

def removeBrackets(paragraph):
    re1='.*?'	# Non-greedy match on filler
    re2='(\\[.*?\\])'	# Square Braces 1
    rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
    m = rg.search(paragraph)
    while m:
        sbraces1=m.group(1)
        paragraph = paragraph.replace(sbraces1,"")
        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(paragraph)
    return paragraph

def crawlWiki():
    articles = []
    for x in xrange(0,10):
        url = "https://simple.wikipedia.org/wiki/Template:Did_you_know/Archives/" + str(x+1)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        a_tag = soup.select("div#mw-content-text ul li a")

        for item in a_tag:
            pageUrl = item.get('href')
            if pageUrl[0:6] == "/wiki/":
                if ("/wiki/File:" not in pageUrl) and ("/wiki/Special:" not in pageUrl):
                    print pageUrl
                    articles.append(pageUrl)

    return articles

# ============================   MAIN FUNCTION   ===============================
articles = list(set([page.replace("\n","") for page in open("articles.txt","r")]))
for page in articles[0:30]:
    print wurl.normal(page)
    paragraph = scrapeParagraph(wurl.normal(page))
    print paragraph
    print("Length: " + str(len(paragraph)))
    print("-----------------------------------")
    print wurl.simple(page)
    paragraph = scrapeParagraph(wurl.simple(page))
    print paragraph
    print("Length: " + str(len(paragraph)))
    print("\n========================\n")
# ==========================   END MAIN FUNCTION   =============================

# ==============================   DEBUGGING   =================================
# print scrapeParagraph("https://en.wikipedia.org/wiki/Overseas_Regions_of_France")
# ============================   END DEBUGGING   ===============================

# =================================   MISC   ===================================
# crawl wiki for article titles. save them to disk for debugging efficiency.
# articles = [page.replace("\n","") for page in open("articles.txt","r")]
# ===============================   END MISC   =================================
















#

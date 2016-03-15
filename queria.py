# external libraries
from bs4 import BeautifulSoup
from google import search
import fuzzywuzzy
import requests

def getURLs(searchString):
    urls = []
    for url in search(searchString, stop=20):
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
        print paragraph.text.replace("\n","")
        print("\n") # break them up a little bit.

# =========================   BEGIN MAIN FUNCTION   ============================
searchURLs = getURLs("dung beetle")

for url in searchURLs:
    print(url)
    # parsePage(url)
# ==========================   END MAIN FUNCTION   =============================

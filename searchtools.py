import sys
from google import search

urls = []

def getURLs(searchString):
    for url in search(searchString, stop=20):
        urls.append(url)
    return urls

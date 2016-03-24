from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

myList = ['a','b','a']
print myList
print set(myList)
print myList
list(set(myList))
myList = list(set(myList))
print myList

# Queria
A faster way to find the answers to your web searches. When you make a search on google, you are given thousands of results to read from. With Queria, these pages are quickly parsed and the answer to your question is given directly.  

### Multiple Choice Questions
If you input possible answers to your question, the likelihood of each answer is given to you. The first twenty search results from google are parsed, and your questions is searched in each paragraph using token set ratios. Your provided answers will be searched for within paragraphs deemed relevant to your question. The higher the count of occurences for each answer, the more likely that answer is correct.

### Free Response Questions
Your question is searched specifically within the realm of quizlet. Only the first three pages are parsed for this type of question. Within these quizlets, only question cards with 90% similarity (to your question) are displayed.

## Dependencies
- The [Google](https://pypi.python.org/pypi/google#downloads) package for python.
- [BeautifulSoup](https://pypi.python.org/pypi/beautifulsoup4)
- [python-levenshtein](https://pypi.python.org/pypi/python-Levenshtein)
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
- [requests](http://docs.python-requests.org/en/master/)

## Installation
`$ pip install google`  
`$ pip install beautifulsoup4`  
`$ pip install requests`  
`$ pip install fuzzywuzzy`  
`$ pip install python-levenshtein`  

That's it.

## Coming Soon
As of right now, the Free Response section is powered only with quizlet. This means that if a quizlet doesn't have the answer to your question, you're out of luck. In the future, I plan on accessing wikipedia articles, finding relevant passages within them, and then summarizing those passages.  

Also, I plan on experimenting putting your search phrase into quotes when searching google (thus searching for the exact phrase), and then also parsing the pages within those results.

Both of these things would add quite a few dependencies, though (the summarization would require about 2 more packages and page parsing would require nltk with at least 3 of its corpora). We shall see what I decide on...
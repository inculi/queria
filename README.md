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
It is easiest to begin with the pip installations.  
`pip install beautifulsoup4`  
`pip install requests`  
`pip install fuzzywuzzy`  
`pip install python-levenshtein`  

[Download](https://pypi.python.org/pypi/google#downloads) the google package for python.

That's it.
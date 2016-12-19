# internal libraries
import os
import pprint

# external libraries
from google import search
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

debugMode = True

def dprint(string):
    if debugMode == True:
        print string

def printAll(myList):
    for item in myList:
        print item

class parse:
    @staticmethod
    def parsePage(url, searchString):
        """
        Returns paragraphs in a given page containing a token_set_ratio above
        50 for a given searchString.

        :param url: the url you wish to visit.
        :param searchString: the string you wish to search the page for.
        :output: a list of strings (the paragraphs).
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        paragraphTexts = []

        pageContent = soup.find_all("p") # find the text of the page
        for paragraph in pageContent:
            paragraphText = paragraph.text.replace("\n","")
            # print(paragraphText)
            # print fuzz.token_set_ratio(inputQuestion, paragraphText)
            if int(fuzz.token_set_ratio(searchString.lower(), paragraphText.lower())) > 50:
                # print paragraphText
                paragraphTexts.append(paragraphText)

        return paragraphTexts

class quizlet:
    class CardSet:
        def __init__(self, *url, **data):
            """
            :param url: the url of the quizlet you wish to access. It is of type
                string, however I also want to make it of type list so that I can
                either index multiple quizlets at the same time, or be able to store
                all the urls of the involved quizlets when I combine multiple
                CardSet objects.

            :param data: An optional argument, mainly used when combining multiple
                card sets. It is used in these scenarios, as I don't want to have to
                redownload set data just when I am combining 2 CardSets. In these
                cases, you will also notice that urls aren't a necessity, though
                you can feel free to add them (read: you should add them).
            """
            if url:
                self.url = url[0] # Url is being seen as a tuple. Convert it for use.
            else:
                # Url does not exist. Do nothing, as it was loaded in with data{}.
                pass

            try:
                # Try loading in the data given with the data parameter. If it's not
                #   there, don't worry about it.
                data = data['data']
            except KeyError:
                data = {}

            if ('answers' in data):
                # Load the data we have. I'm going to assume if we have answers,
                #   we have all the other data. Since we have the data, we don't
                #   need to access the quizlet url makeSet() or makeCards()
                self.questions = data['questions']
                self.answers = data['answers']
                self.cards = data['cards']
                try:
                    self.url = data['url'] # this most likely will always be a list.
                except:
                    self.url = []
            else:
                # This is the code that will normally execute when giving the class
                #   a url to create a quizlet object from.
                if type(url) == tuple:
                    self.url = url[0]
                if type(self.url) == str:
                    # We want to be able to create a CardSet out of either a single
                    #   quizlet url, or a list of them. Treating them all as lists makes
                    #   this part easier.
                    self.url = [self.url]

                # initialize some lists we are going to populate with data.
                self.questions = []
                self.answers = []
                self.cards = []

                # populate the lists with data.
                self.makeSet() # gets questions and answers from quizlet
                self.makeCards() # puts the Q&A's as tuples in self.cards

            # used in iteration.
            self.i = 0 # starting iteration index.
            self.n = len(self.cards) # index to stop iterating at (the end).

        def __iter__(self):
            return self

        def next(self):
            # for item in myCardSet:
            #   print item
            #
            # this returns the cards in the CardSet.
            if self.i == 0:
                self.updateIter()

            if self.i < self.n:
                i = self.i
                self.i += 1
                return self.cards[i]
            else:
                raise StopIteration()

        def __add__(self, other):
            if not isinstance(other, CardSet):
                other = CardSet(other)

            data = {'questions' : self.questions + other.questions,
                    'answers' : self.answers + other.answers,
                    'cards' : self.cards + other.cards,
                    'url': self.url + other.url}

            return CardSet(data=data)

        def updateIter(self):
            """
            Sometimes, before iterating, I do some stuff to affect the length of
                self.cards (like removing duplicates). However, this changes self.n,
                creating IndexErrors. This function will be called when it first
                starts iterating, that way it will self.n will always be correct.
            """
            self.n = len(self.cards) # index to stop iterating at (the end).

        def makeSet(self):
            """
            Uses bs4+requests to grab card data from the quizlet url(s) in
            self.url

            If I have to update anything over the coming years, it's going to be
            the soup.select() stuff that quizlet changes in the DOM.
            Worst case scenario, they start adding more obscure JS stuff, and I have
            to use Selenium+PhantomJS instead of requests.

            :output: it modifies self.questions and self.answers with the data from
                the quizlet set.
            """
            for pageUrl in self.url:
                r = requests.get(pageUrl)
                soup = BeautifulSoup(r.content, "html.parser")
                test_tag = soup.select("span.TermText")

                index = 1
                for item in test_tag:
                    if index%2 == 0:
                        # even indexes are answers.
                        self.answers.append(item.text)
                    else:
                        # odd indexes are questions.
                        self.questions.append(item.text)
                    index += 1 # increment for the next pass.

        def makeCards(self):
            for x in xrange(0,len(self.questions)):
                self.cards.append((self.questions[x],self.answers[x]))
                

class wiki:
    @staticmethod
    def wikiSearch(searchString):
        """
        Return a list of wikipedia articles, such that they aren't ones
        linked to chapter markers of an article. We only want links to the full
        article.

        :param searchString: the string we wish to search google for.
        :output: a list of 3 urls.
        """
        urls = []
        for url in search(searchString + " site:wikipedia.org", stop=10):
            # we only want three urls.
            # 'relevant' wikipedia sub-urls have '?sa=X&ved=' in them... filter that
            if (len(urls) < 3) and ("?sa=X&ved=" not in url):
                urls.append(url)

        urls.reverse() # order the links according to how they appear in google
        return urls

    ### TOPIC FINDING
    @staticmethod
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

    @staticmethod
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
    @staticmethod
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
        try:
            topic = topic.replace("%E2%80%93","-")
            pageText = wikipedia.WikipediaPage(topic).content
        except KeyError:
            print("There was an error loading the url, having to do with Unicode.")
            import re
            re1='((?:[a-z][a-z0-9_]*))'	# Variable Name 1

            rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
            m = rg.search(topic)
            if m:
                topic=m.group(1).replace("_"," ")
            print(u"Topic is now " + topic)
            print wikipedia.search(topic)
            pageText = wikipedia.WikipediaPage(topic).content

        # break the page into sentences for sifting through.
        import nltk
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

    @staticmethod
    def answerQuestion(questionString):
        urls = wiki.wikiSearch(questionString)
        paragraph = u'' # the paragraph we are going to build with the data
        sentences = []

        for url in urls:
            tempSents = wiki.readArticle(url,questionString)
            tempSents.sort(reverse=True)
            if len(tempSents) != 0:
                for item in tempSents:
                    sentences.append(item[0])

        for sentence in sentences:
            paragraph += sentence + " "

        print("\n") # make some room
        print(paragraph)

class goog:
    @staticmethod
    def getGoogleURLs(searchString):
        urls = []
        for url in search(searchString +
        """ -filetype:pdf \
    -filetype:docx \
    -filetype:doc \
    -filetype:pptx \
    -filetype:ppt \
    -site:youtube.com \
    -site:wikipedia.org \
    -site:books.google.com \
    -site:vimeo.com""", stop=20):
            # eventually, I want to be able to include the wikipedia urls, but I
            # will have to clean them up first so that I do not also include the
            # duplicate articles.
            urls.append(url)
        # return urls[0:answerAmount]
        return urls

    @staticmethod
    def getQuizletURLs(searchString):
        urls = []
        for url in search(searchString + " site:quizlet.com", stop=3):
            if len(urls) < 3: # The top three should suffice.
                print(url)
                urls.append(url)
            else:
                break
        return urls

class answer:
    @staticmethod
    def answerMC():
        inputQuestion = raw_input("What is your question?\n > ")
        answerAmount = int(raw_input("How many possible answers do you know?\n > "))
        answers = []
        for x in xrange(0,answerAmount):
            answers.append(raw_input("Please input answer " + str(x+1) + "\n > "))
        # ========================   END PRIMARY VARIABLES   ===========================

        print("\nSearching...")
        searchURLs = goog.getGoogleURLs(inputQuestion)

        paragraphTexts = []

        for url in searchURLs:
            print(url)
            data = parse.parsePage(url, inputQuestion)
            for item in data:
                paragraphTexts.append(item) # save the relevant paragraphs

        print("\n") # make some room

        scores = [0] * answerAmount

        paragraphTexts = list(set(paragraphTexts))
        for x in xrange(0,len(answers)):
            for paragraph in paragraphTexts:
                scores[x] += paragraph.lower().count(answers[x].lower())

        print("Scores:")
        for x in xrange(0,len(answers)):
            print answers[x]
            print scores[x]
            print("\n")

    @staticmethod
    def answerFree():
        inputQuestion = raw_input("\n What is your question?\n\n > ")
        print("\n Searching...")
        urls = goog.getQuizletURLs(inputQuestion)
        dprint(urls)
        print("") # make some room.

        cardData = quizlet.CardSet(urls)
        cardData.cards = list(set(cardData.cards)) # remove duplicates

        # We have to look through ALL of the cards we have on file.
        possibleAnswers = 0
        for card in cardData:
            # Scan the card data for questions similar to ours.
            # card[0] = question.
            # card[1] = answer.
            if int(fuzz.token_set_ratio(inputQuestion.lower().replace("?",""), card[0].lower())) > 90:
                print(card[1])
                # in debugging mode, print the definition which the
                # fuzzy string matching liked.
                dprint(card[0])
                possibleAnswers += 1
        if possibleAnswers == 0:
            print("\nNo possible answers found.")

    @staticmethod
    def answerImport():
        questionFile = open("questions.txt","r")
        answerFile = open("answers.txt",'w')

        inputQuestions = [question.replace("\n","") for question in questionFile]
        print inputQuestions # verify for debugging

        questionFile.close() # I not longer need the file, as I imported all of them
                             # into a list already...

        relevantUrls = [] # create a list to store relevant urls.

        # begin the search.
        print("\nSearching...")
        for question in inputQuestions:
            # get the 3 quizlet links for the question
            for item in goog.getQuizletURLs(question):
                relevantUrls.append(item)

        relevantUrls = list(set(relevantUrls)) # remove the duplicates, as we don't need
                                               # to visit the same page mult. times.

        # Download and store the cards from all the quizlet links
        cardData = quizlet.CardSet(relevantUrls)

        cardData.cards = list(set(cardData.cards)) # remove duplicates

        # Iterate through our questions, scanning our card collection each time for
        # relevant answers. Write the answers to the appropriate file.
        for question in inputQuestions:
            print("Searching: " + str(question)[:10])
            # If there aren't any answers for a question, I will have to write that
            # in the answers file.
            possibleAnswers = 0

            # We have to look through all of the cards we have on file.
            for card in cardData:
                # Scan the card data for questions similar to ours.
                # card[0] = question.
                # card[1] = answer.
                if int(fuzz.token_set_ratio(question.lower(), card[0].lower())) > 90:
                    print("Found an answer for \"" + str(question)[:10] + "...\"")
                    if possibleAnswers < 1:
                        answerFile.write("\n === "+question+" === \n")
                    answerFile.write("\n"+card[0]+"\n")
                    answerFile.write(card[1]+"\n")
                    possibleAnswers += 1

            if possibleAnswers == 0:
                print("\nNo possible answers found.")
                answerFile.write("\nNo possible answers found.")

# =========================   BEGIN MAIN FUNCTION   ============================
if __name__ == "__main__":
    print("""                       _
      __ _ _   _  ___ _ __(_) __ _
     / _` | | | |/ _ \ '__| |/ _` |
    | (_| | |_| |  __/ |  | | (_| |
     \__, |\__,_|\___|_|  |_|\__,_|
        |_|
    """)
    questionOption = int(raw_input(""" OPTIONS:
     --------
     1. Multiple Choice
     2. Free Response
     3. Import Questions
     4. Exit

     > """))

    if questionOption == 1:
        answer.answerMC()
    elif questionOption == 2:
    #     subquestionOption = int(raw_input("""\n SEARCH WITH:
    #  -----------
    #  1. Quizlet
    #  2. Wikipedia\n\n > """))
    #     if subquestionOption == 1:
        answer.answerFree()
    elif questionOption == 3:
        answer.answerImport()
    else:
        print("\nThank you for using queria! :)\n")
        exit()
# ==========================   END MAIN FUNCTION   =============================

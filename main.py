class TextProcessor:
    def __init__(self, text):
        # this function makes all objects have a text input and a list.
        self.text = text
        self.stopWordsList = []

    def setStopWords(self, stopWords):
        ''' set stop words as recieved in the parameters '''
        ## CODE HERE ##
        # this function assigns the stopWords input as stopWordsList
        self.stopWordsList = stopWords

    def getStopWords(self):
        ''' return stop words '''
        ## CODE HERE ##
        # this function returrns the stopWordsList
        return self.stopWordsList

    def getUniqWords(self):
        ''' return unique words in a document corpus '''
        ## CODE HERE ##
        # this function splits the given text input string, then it appends the words in the string into a list.
        list = []
        words = self.text.split()
        for word in words:
            if word not in list:
                list.append(word)
        return list

    def getFilteredText(self):
        ''' remove filter words from the text
            return filtered text
        '''
        ## CODE HERE ##
        # this function splits the given text input string, then it appends the split words if its not in the stopWordsList into a list.
        words = self.text.split()
        list = []
        stopWords = self.getStopWords()
        for word in words:
            if word not in stopWords:
                list.append(word)
        return list


class TextAnalyzer(TextProcessor):
    def __init__(self, text):
        ''' Construct the class '''
        ## CODE HERE ##
        # this makes it inherit the previous class
        super().__init__(text)

    def getWordFrequency(self):
        ''' Call the getFilteredText() method
            Create a dictionary of words
            key = word and value= frequency
            return the dictionary
        '''
        ## CODE HERE ##
        # this returns the getFilteredText list and then it runs a for loop on getUniqWords then it counts how many times the unique words appear in getFilteredText then it stores the value for each word in a dictionary.
        frequencyOfWords = {}
        filteredText = TextProcessor.getFilteredText(self)
        for word in TextProcessor.getUniqWords(self):
            wordFrequency = filteredText.count(word)
            if wordFrequency > 0:
                frequencyOfWords[word] = wordFrequency
        return frequencyOfWords


class TextClassifier(TextProcessor):
    def __init__(self, text):
        ''' Construct the class '''
        ## CODE HERE ##
        # this makes it inherit the previous class
        super().__init__(text)

    def loadCorpus(self):
        ''' read documents into a dictionary such that
            keys of the dictionary are class ids
            and values are list of documents
            {1 : ['text of doc1', 'text of doc2'],
             2 : ['text of doc3', 'text of doc4']
            }
        '''
        ## CODE HERE ##
        # this function opens 14 texts files as rowx and reads it then it splits the string into a list then depending if the string has a yes or no it divides and appends them into seperate lists then it store the yesList and No list into a dictionary.
        corpus = {}
        yesList = []
        noList = []
        for x in range(1, 15):
            with open(f"row{x}.txt", "r") as rowx:
                rowxdata = rowx.read()
                wordsx = rowxdata.split()
                for word in wordsx:
                    if word.lower() == 'yes':
                        wordsx.pop(0)
                        wordsx.pop(-1)
                        yesList.append(wordsx)
                        corpus['Play is Yes'] = yesList
                    if word.lower() == 'no':
                        wordsx.pop(0)
                        wordsx.pop(-1)
                        noList.append(wordsx)
                        corpus['Play is No'] = noList
        return corpus

    def getDocumentProbabilityGivenClass(self, passeddoc, playNoplayclass):
        ''' Calculate conditional probability of a document given its class
        '''
        ## CODE HERE ##
        # this function returns the loadCorpus function and assigns totalYes variable as the length of the Play is Yes key in corpus and assigns the totalNo variable as the length of the Play is No key in corpus
        # depending if the given input of playNoplayclass is no play or play it gets the frequency of the words from the corpus key then it adds the probablity of each word in the yes or no list then it finally
        # multiplies the probablity of all the words given to get the probability of the doc/list given
        frequency = {}
        no = []
        yes = []
        corpus = self.loadCorpus()
        totalYes = len(corpus['Play is Yes'])
        totalNo = len(corpus['Play is No'])

        probabilityDoc = 1

        if playNoplayclass.lower() == 'no play':
            for word in passeddoc:
                for value in corpus['Play is No']:
                    if word in value:
                        if word in frequency.keys():
                            frequency[word] += 1
                        else:
                            frequency[word] = 1
            for value in frequency.values():
                no.append(float(value / totalNo))
            for value in no:
                probabilityDoc *= value
            return round(probabilityDoc, 4)

        elif playNoplayclass.lower() == 'play':
            for word in passeddoc:
                for value in corpus['Play is Yes']:
                    if word in value:
                        if word in frequency.keys():
                            frequency[word] += 1
                        else:
                            frequency[word] = 1
            for value in frequency.values():
                yes.append(float(value / totalYes))
            for value in yes:
                probabilityDoc *= value
            return round(probabilityDoc, 4)
        else:
            return "Error: enter 'No Play' or 'Play' after entering your list."

    def getPriorProbability(self, priorProbabilityClass):
        ''' return prior probability of a text class
        '''
        ## CODE HERE ##
        # this function assigns corpus as the return of the loadCorpus function then it assigns listNo as the value of the Play is No key and listYes as the value of the Play is Yes key listtotal is the combination of listYes and listNo
        # then it calculates the priorProbabilityPlay and priorProbabilityNoPlay by dividing the length of either yes or no by the lenth of the totallist then depending if the priorProbabilityClass input is play or no play it will return
        # the priorProbabilityPlay calculation or the priorProbabilityNoPlay calculation
        corpus = self.loadCorpus()
        listNo = corpus['Play is No']
        listYes = corpus['Play is Yes']
        listtotal = listYes + listNo

        priorProbabilityPlay = round(float(len(listYes) / len(listtotal)), 2)
        priorProbabilityNoPlay = round(float(len(listNo) / len(listtotal)), 2)
        if priorProbabilityClass.lower() == 'play':
            return priorProbabilityPlay
        elif priorProbabilityClass.lower() == 'no play':
            return priorProbabilityNoPlay

    def getClassProbabilityGivenDocument(self, passeddoc, playNoplayclass):  #
        ''' return class probability given a document
        '''
        ## CODE HERE ##
        # this function returns getDocumentProbabilityGivenClass times getPriorProbability to get the getClassProbabilityGivenDocument
        return self.getDocumentProbabilityGivenClass(passeddoc, playNoplayclass) * self.getPriorProbability(
            playNoplayclass)

    def getClassGivenDocument(self, passeddoc):
        ''' return class probability given a document
        '''
        ## CODE HERE ##
        # this function calls the getClassProbabilityGivenDocument and inputs the given doc/list it gets the probability of the list and depending on play or no play which ever
        # value of the given docs is higher it will return for example if play was higher then it will retun play if the value of no play is higher it will return no play
        play = self.getClassProbabilityGivenDocument(passeddoc, 'play')
        noPlay = self.getClassProbabilityGivenDocument(passeddoc, 'no play')
        if play > noPlay:
            return 'Play'
        else:
            return 'No Play'


# Test Cases
ta = TextAnalyzer("a quick brown fox " + "a quick brown fox jumps " + "a quick brown fox jumps over " +
                  "a quick brown fox jumps over the " + "a quick brown fox jumps over the lazy " +
                  "a quick brown fox jumps over the lazy dog")
ta.setStopWords(['a', 'the'])
print('Word Frequency: ', end='')
print(ta.getWordFrequency())
ta = TextClassifier('a quick fox')
print('Unique Words: ', end='')
print(ta.getUniqWords())
print('Corpus: ', end='')
print(ta.loadCorpus())
print('Prior Probability: ', end='')
print(ta.getPriorProbability('Play'))
print('Prior Probability: ', end='')
print(ta.getPriorProbability('No Play'))
print('Document Probability Given Class: ', end='')
print(ta.getDocumentProbabilityGivenClass(['Rain', 'Cool', 'Normal', 'Strong'], 'Play'))
print('Class Probability Given Document: ', end='')
print(ta.getClassProbabilityGivenDocument(['Rain', 'Cool', 'Normal', 'Strong'], 'Play'))
print('Class Given Document: ', end='')
print(ta.getClassGivenDocument(['Rain', 'Cool', 'Normal', 'Strong']))
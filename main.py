class TextProcessor:
    def __init__(self, text):
        self.text = text
        self.stopWordsList = []

    def setStopWords(self, stopWords):
        ''' set stop words as recieved in the parameters '''
        ## CODE HERE ##
        self.stopWordsList = stopWords

    def getStopWords(self):
        ''' return stop words '''
        ## CODE HERE ##
        return self.stopWordsList

    def getUniqWords(self):
        ''' return unique words in a document corpus '''
        ## CODE HERE ##
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
        super().__init__(text)

    def getWordFrequency(self):
        ''' Call the getFilteredText() method
            Create a dictionary of words
            key = word and value= frequency
            return the dictionary
        '''
        ## CODE HERE ##
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
        corpus = self.loadCorpus()
        totalYes = len(corpus['Play is Yes'])
        totalNo = len(corpus['Play is No'])
        no = []
        yes = []
        frequency = {}
        prob_doc_given_doc = 1

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
                prob_doc_given_doc *= value
            return round(prob_doc_given_doc, 4)

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
                prob_doc_given_doc *= value
            return round(prob_doc_given_doc, 4)
        else:
            return "Error: enter 'No Play' or 'Play' after entering your list."

    def getPriorProbability(self, priorProbabilityClass):
        ''' return prior probability of a text class
        '''
        ## CODE HERE ##
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
        return self.getDocumentProbabilityGivenClass(passeddoc, playNoplayclass) * self.getPriorProbability(
            playNoplayclass)

    def getClassGivenDocument(self, passeddoc):
        ''' return class probability given a document
        '''
        ## CODE HERE ##
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

import numpy as np
import requests
import pandas as pd
from urllib.parse import urlencode, quote_plus



class GetPhrases():
    """
    A class for extracting phrases and information from abstracts.

    Args:
        keywords (str): Keywords for searching abstracts.
        token (str): API token for accessing the ADS database. Defaults to "Fr3Tux4mhboAq9FvShdtTpZh3JtM9UL73zIyVsng".
        n (int): Number of rows to retrieve from the search results. Defaults to 50.

    Attributes:
        token (str): API token for accessing the ADS database.
        rows (int): Number of rows retrieved from the search results.
        keywords (str): Keywords used for searching abstracts.
        abstracts (str): Concatenated abstracts of the search results.
        indiv_abstracts (list): List of individual abstracts from the search results.
        titles (list): List of titles from the search results.
        links (list): List of links to the full articles.
        whole (str): Lowercased and punctuation-removed version of the abstracts.
        words (list): List of individual words extracted from the abstracts.
        sortedwords (list): List of words sorted by frequency in the abstracts.
        sciencewords (list): List of science-related words extracted from the sorted words.
        sortedphrases (list): List of sorted phrases extracted from the abstracts.
        trimmed (list): List of trimmed phrases, removing repeated phrases.

    Methods:
        encode(self): Encodes the keywords for the API query.
        get_abstract(self): Retrieves abstracts and other information from the API.
        get_links(self): Retrieves links to the full articles from the API.
        get_words(self): Extracts individual words from the abstracts and sorts them by frequency.
        get_science_words(self): Extracts science-related words from the sorted words.
        get_phrases(self): Extracts phrases of four or more words from the abstracts.
        trim_phrases(self): Trims phrases by removing repeated phrases.
        get_best_paper(self): Finds the best paper based on phrase count and returns the link.
        get_context(self, phrase): Retrieves sentences containing the given phrase from the abstracts.
        get_article(self, phrase): Retrieves information (title, abstract, link) about articles containing the given phrase.
        suggest_review_articles(self): Suggests review articles related to the keywords.
        make_questions(self, phrase): Creates a list of questions based on the given phrase (not implemented).
        find_acronyms_advanced(self): Finds acronyms and their definitions using advanced techniques.
        find_acronyms(self): Finds acronyms and their definitions using simple techniques.
    """
    
    def __init__(self, keywords, token="Fr3Tux4mhboAq9FvShdtTpZh3JtM9UL73zIyVsng", n=50):
        
        
        """
        Initializes a GetPhrases instance.
        
        ---
        Parameters:
            keywords (list): List of keywords to search for.
            token (str): API token for accessing the document database. Default is "Fr3Tux4mhboAq9FvShdtTpZh3JtM9UL73zIyVsng".
            n (int): Number of rows to retrieve from the API response. Default is 50.
        """
        
        self.token = token
        self.rows = n
        self.keywords = keywords
        GetPhrases.encode(self)
        self.abstracts = self.get_abstract() # call get_abstract to initialize abstracts
        GetPhrases.get_words(self)

        
        
    def encode(self):
        """
        Encodes the keywords and other parameters into a query string format for the API request.
        """
        
        self.query = urlencode({"q": self.keywords,
                           "fl": "title, bibcode, DOI, abstract",
                           "rows": self.rows
                          })
        

    def get_abstract(self):
        
        """
        Retrieves the abstracts, titles, and links from the API response and stores them in the object.
        
        ---
        Returns:
            self.abstracts (str): The concatenated abstracts
        """
        
        self.results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(self.query), \
                       headers={'Authorization': 'Bearer ' + self.token})
        
        self.abstracts = ""
        self.indiv_abstracts = []
        self.titles = []
        for i in range(0,len(self.results.json()['response']['docs'])):
            try:
                self.abstracts += " "
                self.indiv_abstracts.append(self.results.json()['response']['docs'][i]['abstract'])
                self.abstracts += self.results.json()['response']['docs'][i]['abstract']
                self.titles.append(str(self.results.json()['response']['docs'][i]['title']))
            except:
                pass
            
        
        return self.abstracts
        
    
    def get_links(self):
        """
        Retrieves the links for each document in the API response and returns them as a list.
        
        ---
        Returns:
            self.links (list): List of document links.
        """
        
        self.results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(self.query), \
                       headers={'Authorization': 'Bearer ' + self.token})
        
        self.links = []
        
        for i in range(0,len(self.results.json()['response']['docs'])):
            try:
                self.links.append('https://ui.adsabs.harvard.edu/link_gateway/{}/doi:{}'.format(self.results.json()['response']['docs'][0]['bibcode'],self.results.json()['response']['docs'][i]['doi'][0]))
            except:
                self.links.append('None')
        
        return self.links
    
        
    def get_words(self):
        '''
        Processes the abstracts to extract individual words, their counts, and sorts them in descending order.
        '''
        
        
        self.whole = self.abstracts.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '')
        self.words = self.whole.split()
        values, counts = np.unique(self.words, return_counts=True)
        cv = zip(counts,values)
        cv = sorted(cv,reverse=True)
        self.sortedwords = [x for y,x in cv if y>2]
    
    
    def get_science_words(self):
        '''
        Filters out common words from the list of sorted words and returns a list of science-related words.
        
        ---
        Returns:
            self.sciencewords (list): List of science-related words.
        
        '''
        common_words = [
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'person', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
            'is', 'are', 'has', 'was', 'were', 'be', 'been', 'being', 'am', 'do',
            'did', 'does', 'done', 'have', 'had', 'having', 'can', 'could', 'shall', 'should',
            'will', 'would', 'may', 'might', 'must', 'ought', 'need', 'dare', 'used', 'ought'
        ]
        self.sciencewords = []
        for i in range(0,len(self.sortedwords)):
            if not self.sortedwords[i] in common_words:
                self.sciencewords.append(self.sortedwords[i])
                
        return self.sciencewords
        
    
    def get_phrases(self):
        '''
        Extracts the most common phrases of four or more words from the abstracts and returns them as a list, using the method get_trimmed 
        to remove phrases that are subsets of other phrases.
        
        ---
        Returns:
            self.trimmed (list): List of phrases.
        
        
        '''
        
        # Convert the story to lowercase and remove punctuation
        story = self.abstracts.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '')
        
        # Split the story into words
        words = story.split()
        
        # Find the most common bigrams for phrases of 4 or more words
        num_words = 4
        unique_bigrams = []
        all_counts = []
        while True:
            # Create a list of n-grams (phrases of n words)
            ngrams = [np.array(words[i:i+num_words]) for i in range(len(words)-num_words)]
            # Count the frequency of each unique n-gram
            unique, counts = np.unique(ngrams, return_counts=True, axis=0)
            # Sort the n-grams by frequency in descending order
            sorted_idx = np.argsort(-counts)
            mask = np.where(counts[sorted_idx] > 1)
            sorted_ngrams = unique[sorted_idx][mask]
            # Check if any of the n-grams are repeats of previous n-grams
            if all(counts < 2):
                break
            # Add the new unique n-grams to the list of unique bigrams
            unique_bigrams.extend(sorted_ngrams)
            all_counts.extend(counts[sorted_idx][mask])
            # Increase the number of words per phrase
            num_words += 1

        sorted_unique_bigrams = unique_bigrams
        
        phrases = []
        for i in range(0,len(sorted_unique_bigrams)):
            phrases.append('')
            for j in range(0,len(sorted_unique_bigrams[i])):
                phrases[i] += sorted_unique_bigrams[i][j]
                phrases[i] += (' ')
                
        self.sortedphrases = phrases
        
        GetPhrases.trim_phrases(self)
        
        return self.trimmed
    
    
    def trim_phrases(self):
        '''
        Trims the list of phrases by removing any phrases that are subsets of other phrases.
        
        '''
        
        
        totrim = []
        for i in range(0,len(self.sortedphrases)):
            for j in range(0,len(self.sortedphrases)):
                if self.sortedphrases[i] in self.sortedphrases[j]:
                    if i != j:
                        totrim.append(i)
        
        trim = np.unique(totrim)
        
        trimmed = []
        for i in range(0,len(self.sortedphrases)):
            if i in trim:
                pass
            else:
                trimmed.append(self.sortedphrases[i])
        
        self.trimmed = trimmed

        
        
    def get_best_paper(self):
        
        '''
        Analyzes the phrases and individual abstracts to find the best paper based on phrase frequency and returns its link.
        
        ---
        Returns:
            (str): Link to the best paper.
        
        '''
        
        # Define the list of phrases to search for
        phrases_to_search = self.sortedphrases[:10]

        # Define a list of candidate abstracts to search
        candidate_abstracts = self.indiv_abstracts
        
        # Split each abstract into sentences
        candidate_sentences = []
        for abstract in candidate_abstracts:
            candidate_sentences.append(abstract.split('. '))
        
        # Flatten the list of sentences
        candidate_sentences = [sentence for sublist in candidate_sentences for sentence in sublist]
        
        # Count the number of occurrences of each phrase in each sentence
        phrase_counts = np.zeros((len(candidate_sentences), len(phrases_to_search)))
        for i, sentence in enumerate(candidate_sentences):
            for j, phrase in enumerate(phrases_to_search):
                phrase_counts[i,j] = sentence.count(phrase)
        
        # Calculate the sum of phrase counts for each abstract
        story_counts = np.sum(phrase_counts, axis=0)
        
        # Find the index of the abstract with the highest count
        best_story_idx = np.argmax(story_counts)
        
        # Print the best abstract
        return self.links[best_story_idx]
        
        
    def get_context(self,phrase):
        '''
        Searches the abstracts for sentences containing the specified phrase and returns the context sentences.
        
        ---
        Parameters:
            phrase (str): Phrase to search for in the abstracts.
        
        ---
        Returns:
            context (list): List of sentences containing the phrase.
        
        
        '''
        
        sentences = self.abstracts.split('. ')
        context = []
        for i in range(0,len(sentences)):
            if phrase in sentences[i].lower() and len(context) < 11:
                context.append(sentences[i])
        
        return context
    
    def get_article(self,phrase):
        '''
        Retrieves information (title, abstract, and link) for articles containing the specified phrase and returns it as a list.
        
        ---
        Parameters:
            phrase (str): Phrase to search for in the articles.
            
        ---
        Returns:
            info (list): List of dictionaries containing the article information (title, abstract, and link).
        '''
        
        
        GetPhrases.get_links(self)
        
        info = []
        for i in range(0,len(self.indiv_abstracts)):
            if phrase in self.indiv_abstracts[i].lower():
                info.append("Title: "+self.titles[i])
                info.append("Abstract: "+self.indiv_abstracts[i])
                info.append("Link: "+self.links[i])
            
        return info
            
    def suggest_review_articles(self):
        '''
        Performs a search for review articles related to the keywords and returns the titles, abstracts, and links as a list.
        
        ---
        Returns:
            info (list): List of dictionaries containing the review article information (title, abstract, and link).
        '''
        
        self.review_query = urlencode({"q": "review article "+self.keywords,
                           "fl": "title, bibcode, DOI, abstract",
                           "rows": 10
                          })
        
        self.review_results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(self.review_query), \
                       headers={'Authorization': 'Bearer ' + self.token})
        
        self.review_abstracts = ""
        self.review_indiv_abstracts = []
        self.review_titles = []
        for i in range(0,len(self.review_results.json()['response']['docs'])):
            try:
                self.review_abstracts += " "
                self.review_indiv_abstracts.append(self.review_results.json()['response']['docs'][i]['abstract'])
                self.review_abstracts += self.review_results.json()['response']['docs'][i]['abstract']
                self.review_titles.append(str(self.review_results.json()['response']['docs'][i]['title']))
            except:
                pass
            
        
        self.review_results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(self.review_query), \
                       headers={'Authorization': 'Bearer ' + self.token})
        
        self.review_links = []
        
        for i in range(0,len(self.review_results.json()['response']['docs'])):
            try:
                self.review_links.append('https://ui.adsabs.harvard.edu/link_gateway/{}/doi:{}'.format(self.review_results.json()['response']['docs'][0]['bibcode'],self.review_results.json()['response']['docs'][i]['doi'][0]))
            except:
                self.review_links.append('None')
                
                
        info = []
        for i in range(0,len(self.review_titles)):
            info.append("Title: "+self.review_titles[i])
            info.append("Abstract: "+self.review_indiv_abstracts[i])
            info.append("Link: "+self.review_links[i])
            
        return info
    
        
    
    def find_acronyms_advanced(self):
        '''
        Identifies acronyms and their definitions not formatted Like This (LT) in the abstracts and returns them as a sorted list based on frequency.
        
        ---
        Returns:
            self.sorted_acronyms (list): List of acronyms based on frequency
        '''
        
        words = self.abstracts.split()
        acronyms = []
        i = 0
        while i < len(words):
            if words[i].isupper():
                potential_acronym = words[i]
                if i+1 < len(words) and words[i+1] == '(':
                    # Skip over acronyms in parentheses, e.g. NATO (North Atlantic Treaty Organization)
                    j = i+2
                    while j < len(words) and words[j][-1] != ')':
                        j += 1
                    if j < len(words):
                        i = j+1
                        continue
                j = i+1
                while j < len(words) and not words[j][0].isupper():
                    potential_acronym += words[j]
                    j += 1
                # Check if the potential acronym appears in the text after its definition
                if potential_acronym.lower() in ' '.join(words[j:]).lower():
                    # Extract the definition of the acronym
                    k = i-1
                    while k >= 0 and not words[k][-1] in '.?!':
                        k -= 1
                    definition = ' '.join(words[k+1:i])
                    acronyms.append((potential_acronym, definition))
                i = j
            else:
                i += 1
            
        # Count the frequency of each unique acronym
        unique_acronyms, counts = np.unique(acronyms, return_counts=True)
        
        # Sort the acronyms by frequency in descending order
        sorted_idx = np.argsort(-counts)
        self.sorted_acronyms = unique_acronyms[sorted_idx]
        
        return self.sorted_acronyms
    
    def find_acronyms(self):
        '''
        Identifies acronyms formatted Like This (LT) and their definitions in the abstracts and returns them as a sorted list based on frequency.
        
        ---
        Returns:
            self.sorted_acronyms (list) = List of acronyms and definitions without repeats
        '''
        
        words = np.array(self.abstracts.lower().split())
        acrs = []
        defs = []
        for i in range(0,len(words)):
            # Find words in parentheses (potential acronyms) and check if the surrounding words have the same first letters.
            if words[i][0] == "(" and words[i][-1:] == ")":
                alength = len(words[i])-2
                if words[i-alength][0] == words[i][1]:
                    acrs.append(words[i][1:-1])
                    defs.append(np.array(words[i-alength:i]))
                elif words[i-alength-1][0] == words[i][1]:
                    acrs.append(words[i][1:-1])
                    defs.append(np.array(words[i-alength-1:i]))
                elif words[i-alength+1][0] == words[i][1]:
                    acrs.append(words[i][1:-1])
                    defs.append(np.array(words[i-alength+1:i]))
        
        # Format acronyms
        clean = []
        for i in range(0, len(defs)):
            clean.append('')
            for j in range(0,len(defs[i])):
                clean[i] += defs[i][j]
                clean[i] += ' '
            clean[i] += "("+acrs[i]+")"
            
        return list(np.unique(clean))
        
        
        

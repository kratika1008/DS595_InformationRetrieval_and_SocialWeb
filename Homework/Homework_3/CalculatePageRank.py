# homework 3
# goal: ranked retrieval, PageRank, crawling
# exports:
#   student - a populated and instantiated cs525.Student object
#   PageRankIndex - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents and providing a
#     ranked result set

# ########################################
# first, create a student object
# ########################################

import cs525
MY_NAME = "Kratika Agrawal"
MY_ANUM  = 861735836 # put your UID here
MY_EMAIL = "kagrawal@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = []

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "An Aggie does not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs525.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################

import bs4 as BeautifulSoup  # you will want this for parsing html documents
import urllib.request as request
from  urllib.parse import urljoin
import re
import numpy as np
# our index class definition will hold all logic necessary to create and search
# an index created from a web directory
#
# NOTE - if you would like to subclass your original Index class from homework
# 1 or 2, feel free, but it's not required.  The grading criteria will be to
# call the index_url(...) and ranked_search(...) functions and to examine their
# output.  The index_url(...) function will also be examined to ensure you are
# building the index sanely.

class PageRankIndex(object):
    def __init__(self):
        # you'll want to create something here to hold your index, and other
        # necessary data members
        self._web_graph = {}
        self._inverted_index={}
        self._url=[]
        self._pageRank = []

    def evaluate_pageRank(self):
        alpha = 0.1
        n = len(self._url)
        t = 1/n
        teleport = np.full((n,n),t)
        transition = np.zeros(teleport.shape)
        vec = np.full((1,n),t)
        for link in self._web_graph:
            i = self._url.index(link)
            for sublink in self._web_graph[link]:
                j = self._url.index(sublink)
                transition[i,j]=1
            transition[i,:] = transition[i,:]/np.sum(transition[i,:])
        P = alpha*teleport + (1-alpha)*transition
        rtol = 1e-08
        i=0
        while(1):
            vec1 = np.matmul(vec,P)
            i+=1
            if np.allclose(vec, vec1, rtol):
                break
            else:
                vec = vec1.copy()
        self._pageRank = vec.copy()

    # index_url( url )
    # purpose: crawl through a web directory of html files and generate an
    #   index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: use BeautifulSoup and urllib
    # parameters:
    #   url - a string containing a url to begin indexing at
    def index_url(self, url):
        # ADD CODE HERE
        page = request.urlopen(url)
        soup = BeautifulSoup.BeautifulSoup(page, 'html.parser')
        tokens = []
        for href_link in soup.find_all('a'):
            link = urljoin(url,href_link.get('href'))
            if link not in self._web_graph:
                self._url.append(link)
                self._web_graph[link]=[]
                page2 = request.urlopen(link)

                soup2 = BeautifulSoup.BeautifulSoup(page2, 'html.parser')
                for href_sublink in soup2.find_all('a'):
                    sublink = urljoin(url,href_sublink.get('href'))
                    if sublink not in self._web_graph[link]:
                        self._web_graph[link].append(sublink)

                text = soup2.get_text()
                doc_Tokens = self.tokenize(text)
                tokens.append(doc_Tokens)
                for word in doc_Tokens:
                    if word not in self._inverted_index:
                        self._inverted_index[word] = []
                    if link not in self._inverted_index[word]:
                        self._inverted_index[word].append(link)

        self.evaluate_pageRank()
        return len(self._url)

    # tokenize( text )
    # purpose: convert a string of terms into a list of terms
    # preconditions: none
    # returns: list of terms contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        text = text.lower()
        text = re.sub('[^0-9a-zA-Z]', ' ', text)
        tokens = text.split()
        return tokens

    # ranked_search( text )
    # purpose: searches for the terms in "text" in our index and returns
    #   AND results for highest 10 ranked results
    # preconditions: .index_url(...) has been called on our corpus
    # returns: list of tuples of (url,PageRank) containing relevant
    #   search results
    # parameters:
    #   text - a string of query terms
    def ranked_search(self, text):
        # ADD CODE HERE
        tokens = self.tokenize(text)
        containing_pages = []
        links=[]

        for i,t in enumerate(tokens):
            if t not in self._inverted_index:
                return ['No results found for the query term']
            else:
                if i==0:
                    links = self._inverted_index[t]
                links = list(set(self._inverted_index[t]) & set(links))
        if len(links)==0:
            return ['No results found for the query term']
        for l in links:
            index = self._url.index(l)
            rank = self._pageRank[0][index]
            containing_pages.append((l,rank))
        containing_pages.sort(key = lambda x: x[1],reverse=True)
        if len(containing_pages)>10:
            containing_pages = containing_pages[:10]
        return containing_pages


# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = PageRankIndex()
    url = 'http://web.cs.wpi.edu/~kmlee/cs525/new10/index.html'
    num_files = index.index_url(url)
    search_queries = (
       'palatial', 'college ', 'palatial college', 'college supermarket', 'famous aggie supermarket'
        )
    for q in search_queries:
        results = index.ranked_search(q)
        print("searching: %s -- results: %s" % (q, results))


# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

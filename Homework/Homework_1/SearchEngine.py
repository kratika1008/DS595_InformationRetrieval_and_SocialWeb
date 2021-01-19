# homework 1
# goal: tokenize, index, boolean query
# exports: 
#   student - a populated and instantiated ir4320.Student object
#   Index - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents


# ########################################
# first, create a student object
# ########################################

import cs525
import PorterStemmer

MY_NAME = "Kratika Agrawal"
MY_ANUM  = 123456789 # put your WPI numerical ID here
MY_EMAIL = "kagrawal@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = []

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "I do not lie, cheat or steal, or tolerate those who do."
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

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
class Index(object):
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._inverted_index = {}
        # _documents contains file names of documents
        self._documents = []
        # example:
        #   given the following documents:
        #     doc1 = "the dog ran"
        #     doc2 = "the cat slept"
        #   _documents = ['doc1', 'doc2']
        #   _inverted_index = {
        #      'the': [0,1],
        #      'dog': [0],
        #      'ran': [0],
        #      'cat': [1],
        #      'slept': [1]
        #      }


    # index_dir( base_path )
    # purpose: crawl through a nested directory of text files and generate an
    #   inverted index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
        num_files_indexed = 0
        # PUT YOUR CODE HERE
        docs = glob.glob(base_path+"/*.txt")
        tokens = []
        for i in range(len(docs)): 
            f = open(docs[i],encoding="utf8")
            text = f.read()
            doc_Tokens = self.tokenize(text)
            stemmed_tokens = self.stemming(doc_Tokens)
            tokens.append(stemmed_tokens)
            self._documents.append((docs[i].split('\\'))[1].split('.txt')[0])
            for word in stemmed_tokens:
                if word not in self._inverted_index:
                    self._inverted_index[word] = []
                    self._inverted_index[word].append(self._documents[i])
                else:
                    if self._documents[i] not in self._inverted_index[word]:
                        self._inverted_index[word].append(self._documents[i])
            f.close()
        num_files_indexed = len(self._documents)
        return num_files_indexed

    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        # PUT YOUR CODE HERE
        text = text.lower()
        text = re.sub('[^0-9a-zA-Z]', ' ', text)
        tokens = text.split()
        return tokens

    # purpose: convert a string of terms into a list of tokens.        
    # convert a list of tokens to a list of stemmed tokens,     
    # preconditions: tokenize a string of terms
    # returns: list of stemmed tokens
    # parameters:
    #   tokens - a list of tokens
    def stemming(self, tokens):
        stemmed_tokens = []
        # PUT YOUR CODE HERE
        p = PorterStemmer.PorterStemmer()
        for t in tokens:
            stemmed_tokens.append(p.stem(t,0,len(t)-1))
        return stemmed_tokens
    
    # boolean_search( text )
    # purpose: searches for the terms in "text" in our corpus using logical OR or logical AND. 
    # If "text" contains only single term, search it from the inverted index. If "text" contains three terms including "or" or "and", 
    # do OR or AND search depending on the second term ("or" or "and") in the "text".  
    # preconditions: _inverted_index and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def boolean_search(self, text):
        results = []
        #relevant_docs=[]
        # PUT YOUR CODE HERE
        operand = ''
        tokens = self.tokenize(text)
        if len(tokens)>1:
            operand = tokens[1]
            del tokens[1]
        stemmed_tokens = self.stemming(tokens)
        if len(stemmed_tokens)>1:
            if operand == 'and':
                results = [value for value in list(set(self._inverted_index[stemmed_tokens[0]]) & set(self._inverted_index[stemmed_tokens[1]]))]
            elif operand == 'or':
                results = [value for value in list(set(self._inverted_index[stemmed_tokens[0]]) | set(self._inverted_index[stemmed_tokens[1]]))]
        else:
            results = self._inverted_index[stemmed_tokens[0]]
        
        return results
    

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = Index()
    print("starting indexer")
    num_files = index.index_dir('data/')
    print("indexed %d files" % num_files)
    for term in ('football', 'mike', 'sherman', 'mike OR sherman', 'mike AND sherman'):
        results = index.boolean_search(term)
        print("searching: %s -- results: %s" % (term, ", ".join(results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    import glob
    import re
    main(sys.argv)


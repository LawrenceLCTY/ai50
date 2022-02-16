import nltk
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for f_name in os.listdir(directory):
        f_path = os.path.join(directory, f_name)
        if os.path.isfile(f_path) and f_name[-4:] == '.txt':
            with open(f_path, 'r', encoding = 'utf8') as f:
                files[f_name] = f.read()
    
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    doc = nltk.word_tokenize(document)
    word_list = []
    for word in doc:
        word = word.lower()
        if word not in nltk.corpus.stopwords.words('english'):
            for char in word:
                if char > 'a' and char < 'z':
                    word_list.append(word)
    return word_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    num_docs = len(documents)
    
    for docs in documents:
        repeated = set()
        for word in documents[docs]:
            if word not in repeated:
                repeated.add(word)
                try:
                    idfs[word] += 1
                except KeyError:
                    idfs[word] = 1
            
    for word in idfs:
        idfs[word] = math.log(num_docs / idfs[word])
        
    return idfs



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()
    for f in files:
        tf_idfs[f] = 0
        for q in query:
            tf_idfs[f] += files[f].count(q) * idfs[q]

    fn_list = []
    for k, v in sorted(tf_idfs.items(), key = lambda item : item[1], reverse = True)[:n]:
        fn_list.append(k)
    return fn_list



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    word_list = []
    for s in sentences:
        val = [s,0,0]
        for q in query:
            if q in sentences[s]:
                val[1] += (sentences[s].count(q) / len(sentences[s]))
                val[2] += idfs[q]
        word_list.append(val)

    ranked_list = []
    for i, j, k in sorted(word_list, key = lambda item: (item[2], item[1]), reverse = True)[:n]:
        ranked_list.append(i)
    return ranked_list



if __name__ == "__main__":
    main()

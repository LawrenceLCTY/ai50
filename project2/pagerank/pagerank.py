import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
      sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dist = dict()
    if corpus[page]:
        for site in corpus:
            prob_dist[site] = (1 - damping_factor) / len(corpus)
            if site in corpus[page]:
                prob_dist[site] += damping_factor / len(corpus[page])
    else:
        for site in corpus:
            prob_dist[site] = 1 / len(corpus)

    return prob_dist

 
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_sampling = dict()
    sample_page = None

    for site in corpus:
        pagerank_sampling[site] = 0.0

    for i in range(n):
        if sample_page != None:
            tm = transition_model(corpus, sample_page, damping_factor)
            count, weightage = zip(*tm.items())
            sample_page = random.choices(count, weights = weightage, k = 1)[0]
        else:
            sample_page = random.choices(list(corpus.keys()), k = 1)[0]

        pagerank_sampling[sample_page] += 1
    
    for site in corpus:
        pagerank_sampling[site] /= n

    return pagerank_sampling




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_iteration = dict()
    temp_pagerank = dict()

    for site in corpus:
        pagerank_iteration[site] = 1 / len(corpus)

    end_loop = False

    while end_loop == False:
        for page in pagerank_iteration:
            value = 0.0

            for site in corpus:
                if not corpus[site]:
                    value += pagerank_iteration[site] / len(corpus)
                elif page in corpus[site]:
                    value += pagerank_iteration[site] / len(corpus[site])

            temp_pagerank[page] = ((1 - damping_factor) / len(corpus)) + (damping_factor * value)

        end_loop = True

        for page in pagerank_iteration:
            if temp_pagerank[page] - pagerank_iteration[page] > 0.001:
                end_loop = False
            pagerank_iteration[page] = temp_pagerank[page]

    return pagerank_iteration



if __name__ == "__main__":
    main()

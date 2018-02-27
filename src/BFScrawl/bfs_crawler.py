# -------------------------------------------------------------------------
# Note : The download function is commented out in the main function.
# To download the 1000 webpages, please uncomment it.
# -------------------------------------------------------------------------

'''
Incorrect implementation of BFS -> -5
You need to crawl 1000 pages. You shouldn't stop when the frontier has 1000 links on it.
'''
# importing dependencies

import os
import time
import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------------
# Constants required for Crawling an Ranking

DELAY = 0.05    # Time delay for implementing politeness policy

# -------------------------------------------------------------------------





# -------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------

''' The webgraph consists of webpages(wikipedia articles) and links (inlinks and outlinks).

    Each webpage is a node.
    A node is represented as a list having [url, level] where:
    url (string) is the url of the wepage in the format
    level (int) is the level of the node in the BFS search,
    We also have another data structure: List of nodes, example 'crawled_urls'
    and 'processed' are list of nodes.

    Any downloaded webpage is a document.
    Every document has a unique docID, which is the webpage title directly
    extracted from the URL of the webpage.
    Example:
    docID for webpage "https://en.wikipedia.org/wiki/Solar_Eclipse" is
    Solar_Eclipse

    A Document is represented as a dictionary with docID as the key and its
    inlinks as the values.
'''
# -------------------------------------------------------------------------
# Given   : a list
# Returns : true iff list is empty else false
def empty(list):
    if len(list)==0:
        return True
    else:
        return False
# -------------------------------------------------------------------------
# Given   : a url string
# Returns : true iff it is a valid string
def valid_URL(url_string):
    if len(url_string)>0:
        if (url_string[0:5] == '/wiki'
            and not( ':' in url_string or  '.' in url_string or '#' in url_string)):
            # if the url string has . as in .svg or .jpg or has a # which represents
            # a navigation on the same page or a :, then it is not a valid url
            # It also need to have the keywords for making the search focused
            return True
        else:
            return False
    else:
        return False
# -------------------------------------------------------------------------
# Given   : a url string and a list of nodes where node is a list ['url', level]
# Returns : true iff it the given string is present in the
def present(s,list):
    result = False
    # .lower() handels the following SPECIAL case
    # https://en.wikipedia.org/wiki/Full_Moon and https://en.wikipedia.org/wiki/full_Moon
    # refer to same page
    # if we conside the split part after '/wiki', Full_Moon and full_Moon both
    # refer to the same link and hence must be treated as same.
    # Full_moon page is same as full_moon
    for element in list:
        if (element[0].lower() == s.lower()):
            result = True
            # duplicate hence skip it
            break
    return result

def createPathIfNotExists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

# -------------------------------------------------------------------------
# Given   :  list of nodes where node is a list ['url', level]
# Effect  :  writes the string url of all the nodes in the list to a text file
def write_urls_to_file(list):
    createPathIfNotExists('../savedDocs/')
    fileName = "../URL_list(BFS).txt"
    f= open(fileName,'w')
    i=0
    for element in list:
        f.write(str(element[0])+'\n')
        i+=1
    f.close()
    print('\n\tCrawled urls successfully saved to file : URL_list(BFS).txt')
    print('\n\tTotal no. of crawled URLs : {} '.format(i))
# -------------------------------------------------------------------------

# Given   : given a string
# Effect  : downloads the webpage (in raw html form) corresponding
#           to the given string url and saves it as a text file
def download_webpage(url):
    filename = os.getcwd()+"/BFS_Crawler_Docs/"+url.split('/wiki/')[-1] + '.txt'
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    else:
        #print('File already present')
        return ## Don't download this page and move onto next
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    f.close()

# ----------------------------------------------------------------------------
# Given   : given a list of url nodes
# Effect  : downloads  webpages of all the nodes from the list
def download_urls(list):
    i=0
    print('\n\tDownloading pages .............')
    for element in list:
        download_webpage(str(element[0]))
        time.sleep(DELAY)# Politeness policy: Wait sometime before downloading next page,
                        # as it sends the server a GET request
        i+=1
    print('\n\t{} pages downloaded.'.format(i))


# Given   :   1 seed url, total number of webpages to be crawled, max level
#             which can be crawled by BFS crawler.
# Returns : crawled nodes that are crawled by the focused crawler
def bfs_crawler(seed,max_links,max_level):

    # initailize
    queue = [[seed,1]]  # Queue stores root node which has seed url and its level {seed at level 1}
    crawled_urls = []
    processed = []  # none of the nodes has been processed till now
    level = queue[0][1]  # seed at level 1

    #  condition for halting the crawling process : count > max_links or level > max_depth:

    while not empty(queue) and len(crawled_urls) < max_links and level <= max_level:
        node = queue[0] # pop front element of Queue

        # process this node
        # processing the node begins >>>

        page = requests.get(str(node[0]))  # url from node
        parsed_page = BeautifulSoup(page.text, 'html.parser')
        links = parsed_page.find("div", {"id": "bodyContent"}).findAll('a')
        # all <a> tags inide div with class bodyContent are collected in Links

        level+=1

        for link in links:

            if len(crawled_urls) < max_links and level<=max_levels:
                # if we find a <a> tag which is inside side boxes or other tags
                # which don't directly refer to the body content then they are skipped

                # we now prune invalid links and add valid links to nighbours as neighbour nodes
                # along with their levels
                if (valid_URL(str(link.get('href')))
                and link.parent.get('class') != ['hatnote', 'navigation-not-searchable']  # <a> not in non searchable region
                and link.parent.get('class') != ['thumb tleft'] # <a> not in left side boxes
                and link.parent.get('class') != ['thumb tright']):  # <a> not in right side boxes
                    if link.findParents("table", {"class": "infobox"}) != [] :  # if <a>  in infobox, skip it and move ahead
                        #print(' infobox link')
                        continue

                    #if the url string found in link is not present in the crawled nodes, then add it to crawled nodes
                    if (not present('https://en.wikipedia.org'+str(link.get('href')),crawled_urls)) :
                        crawled_urls.append(['https://en.wikipedia.org'+str(link.get('href')),level])
                        #print('Link {}'.format(len(crawled_urls)).ljust(10) +': {}'.format(crawled_urls[len(crawled_urls)-1][0]).ljust(120)       +  'Level : {}'.format(crawled_urls[len(crawled_urls)-1][1]))

                    # add child of node to Queue if it has not already been processed
                    if (not present('https://en.wikipedia.org'+str(link.get('href')),processed)):
                       queue.append(['https://en.wikipedia.org'+str(link.get('href')),level])
                       #print('node added to Queue : {}'.format(len(queue)))
                        #download_page(str(crawled_urls[len(crawled_urls)-1][0]))

            else:   # either we have exhausted maximum search depth or crawled the maximum number of links
                break   # print('\n\tLinks exhausted or max depth reached.')

        # the node is now processed, so it is added to list of processed nodes and removed from the queue.
        processed.append(node)  # add to list of processed nodes
        queue.pop(0)    # remove this node from Queue

        time.sleep(DELAY) # Politeness policy: Wait sometime before processing another node,
                        # as processing a nodes uses GET request
    # end of while loop
    print('\n\t{} links crawled and crawler at depth {} in BFS tree'.format(len(crawled_urls),level))
    return crawled_urls



if __name__ == "__main__":

    global max_links    # maximum no. of links that need to be crawled
    global max_levels   # max depth allowed to be searched in BFS tree

    # initializaing attributes
    max_links= 100;     # total number of valid links that we need to crawl
    max_levels = 6           # max depth allowed to be searched in BFS tree

    seed = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    start_time = time.clock()       # for calculating the time taken by focused crawler
    print("\n\tCrawling started, please wait for some time . . . ")
    crawled_urls = bfs_crawler(seed,100,6)

    print("\n\tTime taken by BFS crawler (without downloading) : ",time.clock() - start_time," seconds ")

    write_urls_to_file(crawled_urls)  # adding unique crawled urls to file

    # downloading the webpage[raw html] for crawled urls
    #  -------- Uncomment this section to download webpages --------
    #download_urls(crawled_urls)
    # --------------------------------------------------------------

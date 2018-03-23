# -------------------------------------------------------------------------
# Note : The downloading the fetched file before crawling functionality is
# commented out. To download the 1000 webpages, please uncomment it.
# -------------------------------------------------------------------------

# importing dependencies

import os
import time
import requests
import pprint
from bs4 import BeautifulSoup

# -------------------------------------------------------------------------
# Constants required for Crawling and Ranking
DELAY = 1.05    # Time delay for implementing politeness policy
# -------------------------------------------------------------------------

# global variables -----------------------------------------------------------
# crawled_urls = []
webgraph = {}

# -------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------

''' The webgraph consists of webpages(wikipedia articles) and links (inlinks and outlinks).

    A webpage is represented as a list having [url, level] where:
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

    Crawled webpage/url :

    Frontier :

    crawled_urls :


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
    # .lower() handels the following SPECIAL case - This is the redirects case - ALREADY HANDLED
    # https://en.wikipedia.org/wiki/Full_Moon and https://en.wikipedia.org/wiki/full_Moon
    # refer to same page
    # if we conside the split part after '/wiki', Full_Moon and full_Moon both
    # refer to the same link and hence must be treated as same.
    # Full_moon page is same as full_moon
    for page in list:
        if str(page[0]).encode('utf-8') == s.encode('utf-8'):
            return True
            # duplicate hence skip it
    return False

# -------------------------------------------------------------------------

# Given   : given a string
# Effect  : downloads the webpage (in raw html form) corresponding
#           to the given string url and saves it as a text file
def download_webpage(url_str,fetched_url):
    filename = os.getcwd()+"/BFS_CrawlDocs/"+url_str.split('/wiki/')[-1] + '.txt'
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            for chunk in fetched_url.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        f.close()
        print("        DOWNLOADED : "+url_str.split('/wiki/')[-1] + '.txt')
    else:
        print("\n - - -  ALREADY DOWNLOADED  - - - - - - "+url_str.split('/wiki/')[-1] + '.txt'+"\n")
        # Don't download this page and move onto next


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

# ----------------------------------------------------------------------------
# Given   :  list of nodes where node is a list ['url', level]
# Effect  :  writes the string url of all the nodes in the list to a text file
def write_urls_to_file(webpage_list):
    #createPathIfNotExists('../savedDocs/')
    fileName = "URL_list(BFS).txt"
    f= open(fileName,'w')
    i=0
    for webpage in webpage_list:
        f.write(str(webpage[0]))
        f.write('\n')
        i+=1
    f.close()
    print('\n\tCrawled urls successfully saved to file : URL_list(BFS).txt')
    print('\n\t# of URLs added to \'URL_list(BFS).txt\' file: {} '.format(i))


# ----------------------------------------------------------------------------
# Given   :  list of webpages where a webpageis a list ['url', level]
# Effect  :  writes the url and the  of all the nodes in the list to a text file
def write_pages_to_file(list):
    f= open('BFS_webpages_info.txt','w')
    i=1
    for element in list:
        f.write(('Webpage {} :'.format(i).ljust(15)
        +str(element[0]).split('/wiki/')[-1].ljust(75)
        +'Level : {}'.format(element[1])+'\n'))
        i+=1
    f.close()
    print('\n\tCrawled pages [url,level] saved to file : BFS_webpages_info.txt')
    print('\n\tTotal no. of crawled URLs : {} '.format(i-1))
# ----------------------------------------------------------------------------

def print_webgraph():
    #pprint.pprint(webgraph, width=2)

    print('\n===============================================================')
    '''for key, value in webgraph.items() :
        print("  {}".format(key).ljust(40),value)
    print('\n================================================================')
    '''
    print("\n\t  Web Graph Stats")
    print('\n\t# of unique keys',len(webgraph))

# -----------------------------------------------------------------------------

# Given   :
# Effect  :
def write_graph_to_file():
    f= open('G1.txt','w')
    i=1
    for key,value in webgraph.items():
        f.write(key)
        for inlink in value:
            f.write(" "+inlink)
        f.write("\n")
        i+=1
    f.close()
    print('\n\tKeys added to file : G1.txt')
    print('\n\t# of keys : {} '.format(i-1))
# ----------------------------------------------------------------------------

'''
In the implementation of BFS and DFS you have to crawl 1000 pages.
In order to crawl a page, you need to make a request to the page and fetch
its contents. Your implementation, most likely, would stop when the frontier
has 1000 links on it. The links on the frontier are the potential pages to be
crawled in the future but not yet crawled
'''
# Given   :   1 seed url, total number of webpages to be crawled, max level
#             which can be crawled by BFS crawler.
# Returns : crawled nodes that are crawled by the focused crawler
def bfs_crawler(seed,max_links,max_level):

    global webgraph

    # add seed to Frontier (aka request queue)
    # Frontier is a list of webpages which need to be visited in the future
    frontier = [[seed,1]]  # Seed webpage : seed url and its level {seed at level 1}
    crawled_pages = []     # seen or visited or crawled URLS
    #seen = []       # none of the nodes has been processed till now
    level = frontier[0][1]  # seed at level 1
    #  condition for halting the crawling process : count > max_links or level > max_depth:

    while not empty(frontier) and len(crawled_pages) < max_links:
        webpage = frontier[0] # we need to process front element of the Request Queue
        # wepage is a list [url,level]
        # process this webpages

        #  Fetch it and check (after checking for redirects) if already
        # crawled/seen/visited/processed, then don't process it further
        # and pop it and move to next page in the frontier

        if (present(webpage[0],crawled_pages)):
            print("----------Found a match-------")

        # 1. Fetch it
        page = requests.get(str(webpage[0]))  # url from node
        webpage[0] = page.url  # base url , even if the page is redirected we end
                            # up at this url (base url)
        # check for redirect
        # if history is 0, it means it is base page
        # otherwise it means this page was redirected to a base page
        if (len(page.history)>0):
            # check if it is redirecting to an already crawled page
            if (present(webpage[0],crawled_pages)):
                print("--REDIRECT--"+webpage[0])
                frontier.pop(0)   # popping this webpage as it has already been crawled
                continue          # continue to next page in the frontier
        else:  # it is a base page
            # check if this base page has already been crawled
            if (present(webpage[0],crawled_pages)):
                print(webpage[0])
                frontier.pop(0)   # popping this webpage as it has already been crawled
                continue          # continue to next page in the frontier



        #2. Parse it
        parsed_page = BeautifulSoup(page.text, 'html.parser')

        #3. Find all links on the webpage (outgoing links)
        links = parsed_page.find("div", {"id": "bodyContent"}).findAll('a')
         # all <a> tags inide div with class bodyContent are collected in Links

        crawled_pages.append(webpage)  # add to list of processed nodes

        print(('\tLink {}'.format(len(crawled_pages)).ljust(10)
        +': {}'.format(crawled_pages[len(crawled_pages)-1][0].split('/wiki/')[-1]).ljust(75)
        +'Level : {}'.format(crawled_pages[len(crawled_pages)-1][1]).ljust(18)))

        '''downloading the webpage[raw html] for crawled urls
        -------- Uncomment the download_webpage line to download webpages --------
        '''
        # 4. download the webpage after it has been crawled
        download_webpage(str(webpage[0]),page)

        docID = str(webpage[0]).split('/wiki/')[-1]

        if docID not in webgraph:
            webgraph[docID] = []

        if crawled_pages[len(crawled_pages)-1][1] > max_level:
            print("max-depth [{}] searched, HALTING NOW.,".format(max_level))
            break

        else:
            for link in links: # for all links in webpage
                # Find Valid links
                # if we find a <a> tag which is inside side boxes or other tags
                # which don't directly refer to the body content then they are skipped

                # we now prune invalid links and add valid links to nighbours as neighbour nodes
                # along with their levels

                if (valid_URL(str(link.get('href')))
                and link.parent.get('class') != ['hatnote', 'navigation-not-searchable']  # <a> not in non searchable region
                and link.parent.get('class') != ['thumb tleft'] # <a> not in left side boxes
                and link.parent.get('class') != ['thumb tright']):
                    if link.findParents("table", {"class": "infobox"}) != [] :  # if <a>  in infobox, skip it and move ahead
                        #print(' infobox link')
                        continue

                    # add parent to child's inlinks
                    # parent's docID is docID of webpage
                    # childID is link's docID
                    childID = link.get('href').split('/wiki/')[-1]
                    if childID in webgraph:
                        child_inlinks = webgraph[childID]
                        if docID not in child_inlinks:
                            webgraph[childID].append(docID)


                   # if the link is not present in seen/crawled urls, then add it
                   # to frontier (so that it can be processed in the future )
                    if (not present('https://en.wikipedia.org'+str(link.get('href')),crawled_pages)):
                        frontier.append(['https://en.wikipedia.org'+str(link.get('href')),webpage[1]+1])
                        #print('\tFrontier Length : {}'.format(len(frontier)))

        # the webpage is now processed, so it  removed from the frontier
        # and added to list of processed/seen webpages i.e crawled_urls

        '''print(('\tFtr Head : {}'.format(frontier[0][0].split('/wiki/')[-1]).ljust(100)
        +'Frontier Length : {}'.format(len(frontier))))'''

        frontier.pop(0)    # removing the processed webpage from Frontier
        '''
        crawled_pages.append(webpage)  # add to list of processed nodes
        print(('\tLink {}'.format(len(crawled_pages)).ljust(10)
        +': {}'.format(crawled_pages[len(crawled_pages)-1][0].split('/wiki/')[-1]).ljust(50)
        +'Level : {} {}'.format(crawled_pages[len(crawled_pages)-1][1],level).ljust(35)
        '''


        #print("\tAdded to seen\/crawled\/visited\/processed ")

        time.sleep(DELAY)
        #print("\tDelay - {} sec".format(DELAY)) # Politeness policy: Wait sometime before processing another node,
                       # as processing a nodes uses GET request

                       # end of while loop
    print("\n\tCrawling stops!\n")
    print('\t# Links crawled : {}'.format(len(crawled_pages)))
    print('\tCrawler is at depth : {} \(in BFS tree\)'.format(level))
    print("\n\tTime taken by BFS crawler (without downloading) : ",time.clock() - start_time," seconds ")
    return crawled_pages



if __name__ == "__main__":
    global max_links    # maximum no. of links that need to be crawled
    global max_levels   # max depth allowed to be searched in BFS tree

    # initializaing attributes
    max_links= 1000;     # total number of valid links that we need to crawl
    max_levels = 6           # max depth allowed to be searched in BFS tree

    seed = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    start_time = time.clock()       # for calculating the time taken by focused crawler

    print("\n\tCrawling started, please wait for ______ (FILL) time . . . \n")

    crawled_pages= bfs_crawler(seed,10,6)
    write_urls_to_file(crawled_pages)  # adding unique crawled urls to file
    write_pages_to_file(crawled_pages) # adding unique crawled webpages (full info) to txt file
    write_graph_to_file()
    print_webgraph()

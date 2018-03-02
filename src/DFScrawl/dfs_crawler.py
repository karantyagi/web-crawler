# importing dependencies

import os
import time
import requests
from bs4 import BeautifulSoup

#global variables
count = 1
webgraph = {}  # inlinks graph

# -------------------------------------------------------------------------

# Constants required for Crawling an Ranking
DELAY = 1.25    # Time delay for implementing politeness policy
# -------------------------------------------------------------------------


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
    result = False
    # .lower() handels the following SPECIAL case
    # https://en.wikipedia.org/wiki/Full_Moon and https://en.wikipedia.org/wiki/full_Moon
    # refer to same page
    # if we conside the split part after '/wiki', Full_Moon and full_Moon both
    # refer to the same link and hence must be treated as same.
    # Full_moon page is same as full_moon
    for page in list:
        if str(page[0] == s:
            result = True
            # duplicate hence skip it
            break
    return result

# -------------------------------------------------------------------------

def createPathIfNotExists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


# -------------------------------------------------------------------------

# Given   : given a string
# Effect  : downloads the webpage (in raw html form) corresponding
#           to the given string url and saves it as a text file
def download_webpage(url_str,fetched_url):
    filename = os.getcwd()+"/DFS_CrawlDocs/"+url_str.split('/wiki/')[-1] + '.txt'
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    else:
        #print('File already present')
        return ## Don't download this page and move onto next
    fetched_url = requests.get(url_str, stream=True)
    with open(filename, 'wb') as f:
        for chunk in fetched_url.iter_content(chunk_size=1024):
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

# ----------------------------------------------------------------------------
# Given   :  list of nodes where node is a list ['url', level]
# Effect  :  writes the string url of all the nodes in the list to a text file
def write_urls_to_file(webpage_list):
    #createPathIfNotExists('../savedDocs/')
    fileName = "URL_list(DFS).txt"
    f= open(fileName,'w')
    i=0
    for webpage in webpage_list:
        f.write(str(webpage[0]))
        f.write('\n')
        i+=1
    f.close()
    print('\n\tCrawled urls successfully saved to file : URL_list(DFS).txt')
    print('\n\t# of URLs added to \'URL_list(DFS).txt\' file: {} '.format(i))


# ----------------------------------------------------------------------------
# Given   :  list of webpages where a webpageis a list ['url', level]
# Effect  :  writes the url and the  of all the nodes in the list to a text file
def write_pages_to_file(list):
    f= open('DFS_webpages_info.txt','w')
    i=1
    for element in list:
        f.write(('Webpage {} :'.format(i).ljust(15)
        +str(element[0]).split('/wiki/')[-1].ljust(75)
        +'Level : {}'.format(element[1])+'\n'))
        i+=1
    f.close()
    print('\n\tCrawled pages [url,level] saved to file : DFS_webpages_info.txt')
    print('\n\tTotal no. of crawled URLs : {} '.format(i-1))
# ----------------------------------------------------------------------------

def print_webgraph():
    #pprint.pprint(webgraph, width=2)

    print('\n===============================================================')
    '''for key, value in webgraph.items() :
        print("  {}".format(key).ljust(40),value)
    print('\n================================================================')
    '''
    print("\tPrinting only stats now, other things are commented, use util functions")
    print("\n\t  Web Graph Stats")
    print('\n\t# of unique keys',len(webgraph))

# -----------------------------------------------------------------------------

# Given   :
# Effect  :
def write_graph_to_file():
    f= open('G2.txt','w')
    i=1
    for key,value in webgraph.items():
        f.write(key)
        for inlink in value:
            f.write(" "+inlink)
        f.write("\n")
        i+=1
    f.close()
    print('\n\tKeys added to file : G2.txt')
    print('\n\t# of keys : {} '.format(i-1))
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
'''
# Given    :  a node
# Returns  :  find all its immediate neighbours which are valid urls
def findValidLinks(webpage):

    global count
    neighbours = []
    time.sleep(DELAY)# Politeness policy: Wait sometime before processing another node,
                    # as processing a nodes uses GET request
    page = requests.get(str(webpage[0]))  # url from node
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    links = parsed_page.find("div", {"id": "bodyContent"}).findAll('a')
    # all <a> tags inide div with class bodyContent are collected in Links

    # we have crawled th page by fetching it, parsing it and finding the links
    print(('\tLink {}'.format(count).ljust(10)
    +': {}'.format(webpage[0].split('/wiki/')[-1]).ljust(90)
    +'Depth : {}'.format(webpage[1])))
    crawled_pages.append(webpage)
    count+=1

    # we now prune invalid links and add valid links to nighbours as neighbour nodes
    # along with their levels

    for link in links:
        if (valid_URL(str(link.get('href')))
        and link.parent.get('class') != ['hatnote', 'navigation-not-searchable'] # <a> not in non searchable region
        and link.parent.get('class') != ['thumb tleft']     # <a> not in left side boxes
        and link.parent.get('class') != ['thumb tright']):  # <a> not in right side boxes
            if link.findParents("table", {"class": "infobox"}) != [] : # if <a>  in infobox, skip it and move ahead
                #print(' infobox link')
                continue
            neighbours.append(['https://en.wikipedia.org'+str(link.get('href')),(webpage[1]+1)]) #any random depth
    return neighbours

# ----------------------------------------------------------------------------
'''
# Given   :
# Returns :
def redirect(page,crawled_urls):
    '''
    if (page.status_code >= 300
    and document.status_code < 400
    and page.headers['location'] in crawled_urls):
        print(page.headers['location'])
        print(type(page.headers['location']))
        print("True")
        return True
    else:
        return False
    '''
    return False

'''
In the implementation of BFS and DFS you have to crawl 1000 pages.
In order to crawl a page, you need to make a request to the page and fetch
its contents. Your implementation, most likely, would stop when the frontier
has 1000 links on it. The links on the frontier are the potential pages to be
crawled in the future but not yet crawled
'''

def recursive_dfs_crawl(webpage, crawled_pages):
    #recursive depth first search from start till max depth of 6
    global count
    global max_links
    global max_depth
    global webgraph



    if count > max_links :
        return crawled_pages
    else:
        #print('\t URLs crawled : {}'.format(count))

        if webpage[1] > max_depth:
            return crawled_pages

        neighbours = []
        time.sleep(DELAY)# Politeness policy: Wait sometime before processing another node,
                        # as processing a nodes uses GET request




        page = requests.get(str(webpage[0]))  # url from node
        webpage[0] = page.url  # base url , even if the page is redirected we end
                            # up at this url (base url)
        # check for redirect
        # if history is 0, it means it is base page
        # otherwise it means this page was redirected to a base page
        if (len(page.history)>0):
            # check if it is redirecting to an already crawled page
            if (present(webpage[0],crawled_pages)):
                return crawled_pages
        else:  # it is a base page
            # check if this base page has already been crawled
            if (present(webpage[0],crawled_pages)):
                return crawled_pages

        parsed_page = BeautifulSoup(page.text, 'html.parser')
        links = parsed_page.find("div", {"id": "bodyContent"}).findAll('a')
        # all <a> tags inide div with class bodyContent are collected in Links

        # we have crawled th page by fetching it, parsing it and finding the links

        print(('\tLink {}'.format(count).ljust(10)
        +': {}'.format(webpage[0].split('/wiki/')[-1]).ljust(90)
        +'Depth : {}'.format(webpage[1])))
        crawled_pages.append(webpage)
        count+=1

        docID = str(webpage[0]).split('/wiki/')[-1]

        if docID not in webgraph:
            webgraph[docID] = []

        # 4. download the webpage after it has been crawled
        ''' Download NOT allowed | Uncomment to allow download
        download_webpage(str(webpage[0]),page)'''

        # we now prune invalid links and add valid links to nighbours as neighbour nodes
        # along with their levels

        for link in links:
            if (valid_URL(str(link.get('href')))
            and link.parent.get('class') != ['hatnote', 'navigation-not-searchable'] # <a> not in non searchable region
            and link.parent.get('class') != ['thumb tleft']     # <a> not in left side boxes
            and link.parent.get('class') != ['thumb tright']
            and not redirect(page,crawled_pages)):  # <a> not in right side boxes
                if link.findParents("table", {"class": "infobox"}) != [] : # if <a>  in infobox, skip it and move ahead
                    #print(' infobox link')
                    continue

                # add parent to child's inlinks
                # parent's docID is docID of webpage
                # childID is link's docID
                childID = link.get('href').split('/wiki/')[-1]

                #if childID not in webgraph:
                #    webgraph[childID] = []

                if childID in webgraph:
                    child_inlinks = webgraph[childID]
                    if docID not in child_inlinks:
                        webgraph[childID].append(docID)
                        #print("\nCHILD LINK: ",childID," || PARENT : ",docID," || updated inlink list : ",webgraph[childID])

                neighbours.append(['https://en.wikipedia.org'+str(link.get('href')),(webpage[1]+1)]) #any random depth

        if len(neighbours) >0:
            for neighbor in neighbours:
                if neighbor not in crawled_pages:
                    crawled_pages = recursive_dfs_crawl(neighbor,crawled_pages)

        return crawled_pages

# Given   : a root_node which contains a seed
# returns : the visited nodes
def dfs_crawler(seed):

    start_time = time.clock()   # for calculating the time taken by focused crawler
    print("\n\tCrawling started, please wait for ______ (FILL) time . . . \n")
    seed_page = [seed,1]  # start at depth 1
     # has no crawled webpages at the moment

    crawled_pages = recursive_dfs_crawl(seed_page,[])
    #print('\n\tControl back to dfs_crawler()')
    print("\n\tTime taken by DFS crawler : ",time.clock() - start_time," seconds ")

    return crawled_pages



if __name__ == "__main__":                      #  main function

    global max_links    # maximum no. of links that need to be crawled
    global max_depth     # max depth allowed to be searched in DFS tree

    # initializaing attributes
    max_links =  10 # total number of valid links that we need to crawl
    max_depth =  6 # max depth allowed in DFS tree
    seed = 'https://en.wikipedia.org/wiki/Solar_eclipse'

    crawled_pages= dfs_crawler(seed)

    write_urls_to_file(crawled_pages)  # adding unique crawled urls to file
    write_pages_to_file(crawled_pages) # adding unique crawled webpages (full info) to txt file
    write_graph_to_file()
    print_webgraph()

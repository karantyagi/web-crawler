# importing dependencies

import os
import time
import requests
from bs4 import BeautifulSoup

# global variables
max_links = 0   # maximum no. of links that need to be crawled
max_levels = 0  # max depth allowed to be searched in BFS tree

# -------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------

''' The search graph consists of nodes.
    Each node is considered as a list : [url string, level], where level is the level of the
    node in the BFS search tree.
    We also have another data structure: List of nodes, example 'crawled_urls'
    and 'processed' are list of nodes.
'''

# Given   : a list
# Returns : true iff list is empty else false
def empty(list):
    if len(list)==0:
        return True
    else:
        return False

# Given   : a string
# Returns : true iff any of the keywords occurs in the string (not case sensitive)
# where keywords is a list of strings
def hasKeyword(keywords,string):
    result = False
    for word in keywords:
        if word.lower() in string.lower():
            result = True
        else:
            continue
    return result


# Given   : a url string and a list of keywords
# Returns : true iff it is a valid string
def valid_focused_URL(url_string,keywords):
    if len(url_string)>0:
        # if the url string has . as in .svg or .jpg or has a # which represents
        # a navigation on the same page or a :, then it is not a valid url
        # It also need to have the keywords for making the search focused
        if url_string[0:5] == '/wiki' and not( ':' in url_string or  '.' in url_string or '#' in url_string) \
        and hasKeyword(keywords,url_string) :
            return True
        else:
            return False
    else:
        return False


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


# Given   :  list of nodes where node is a list ['url', level]
# Effect  :  writes the string url of all the nodes in the list to a text file
def add_to_file(list):
    f= open('Focused_URLs.txt','w')
    for element in list:
        f.write(str(element[0])+'\n')

    f.close()
    print('\n\tCrawled urls successfully saved to file : Focused_URLs.txt')


# Given   :  list of nodes where node is a list ['url', level]
# Effect  :  writes the string url of all the nodes in the list to a text file
def focused_bfs_crawler(frontier, max_links, max_levels, keywords):
    #max_links = 1000
    #max_levels = 6 # seed is considered 1 in my case

    # initailize
    queue = [[frontier,1]]  # Queue stores root node which has seed url and its level {seed at level 1}
    crawled_urls = []
    processed = []
    level = queue[0][1]  # seed at level 1

    #  condition for halting the crawling process : count > max_links or level > max_depth:

    while not empty(queue) and len(crawled_urls) < max_links and level <= max_levels:
        node = queue[0] # pop front element of Queue
        # process this node(web-page)
        page = requests.get(str(node[0]))  # url from node
        parsed_page = BeautifulSoup(page.text, 'html.parser')
        links = parsed_page.find("div", {"id": "bodyContent"}).findAll('a')
        level+=1

        for link in links:
            if len(crawled_urls) < max_links and level<=max_levels:
                if (valid_focused_URL(str(link.get('href')),keywords)
                and link.parent.get('class') != ['hatnote', 'navigation-not-searchable']
                and link.parent.get('class') != ['thumb tleft']
                and link.parent.get('class') != ['thumb tright']):
                    if link.findParents("table", {"class": "infobox"}) != [] :
                        #print(' infobox link')
                        continue


                    if (not present('https://en.wikipedia.org'+str(link.get('href')),crawled_urls)) :
                        crawled_urls.append(['https://en.wikipedia.org'+str(link.get('href')),level])
                        print('Link {}'.format(len(crawled_urls)).ljust(10) +': {}'.format(crawled_urls[len(crawled_urls)-1][0]).ljust(120)       +  'Level : {}'.format(crawled_urls[len(crawled_urls)-1][1]))

                    if (not present('https://en.wikipedia.org'+str(link.get('href')),processed)):
                       queue.append(['https://en.wikipedia.org'+str(link.get('href')),level])
                       #print('node added to Queue : {}'.format(len(queue)))
                        #download_page(str(crawled_urls[len(crawled_urls)-1][0]))

            else:
                print('\n\tLinks exhausted or max depth reached.')
                print('\n\tLinks Crawled : {}  Depth reached : {}'.format(len(crawled_urls),level))
                break

        # node is now processed
        processed.append(node)  # add to list of processed nodes
        queue.pop(0)    # remove this node from Queue
        #print('node removed from Queue : {}'.format(len(queue)))
        time.sleep(1.5) # Wait sometime before processing another node
    # end of while loop

    print('\n\t{} links crawled and crawler at {} depth in BFS tree'.format(len(crawled_urls),level))

    return crawled_urls



if __name__ == "__main__":

    global max_links
    global max_levels

    # initializaing attributes
    total_links = 1000;     # total number of valid links that we need to crawl
    max_depth = 6           # max depth allowed to be searched in BFS tree
    seed = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    keywords = ['moon','lunar']  #Keyword for focussed crawling

    start_time = time.clock()   # for calculating the time taken by focused crawler
    crawled_urls = focused_bfs_crawler(seed,total_links,max_depth,keywords)
    print("\n\tTime taken by Focused BFS crawler : ",time.clock() - start_time," seconds")

    add_to_file(crawled_urls)    # adding unique crawled urls to file
    #download_urls(crawled_urls) # downloading the webpage[raw html] for crawled urls

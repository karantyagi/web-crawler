import os
import time
import requests
from bs4 import BeautifulSoup

# Helper functions

# Given   : a list
# Returns : true iff list is empty else false
def empty(list):
    if len(list)==0:
        return True
    else:
        return False

def hasKeyword(keywords,string):
    result = False
    for word in keywords:
        if word in string.lower():
            result = True
        else:
            continue
    return result


# improve function - too many returns and unnecessary if else
# 2 0- try to optimize design  - you are passing same thing from 1st to 2nd to 3rd function -find a better way
def valid_URL(url_string):
    if len(url_string)>0:
        if (url_string[0:5] == '/wiki'
            and not( ':' in url_string or  '.' in url_string or '#' in url_string)):
            return True
        else:
            return False
    else:
        return False

#given : a url{string} and a list having url and its level ['url', level]
#returns :
def present(s,list):
    result = False

    # .lower() handels the following
    # https://en.wikipedia.org/wiki/Full_Moon and https://en.wikipedia.org/wiki/full_Moon
    # refer to same page

    # Full_moon page is same as full_moon

    for element in list:
        if (element[0].lower() == s.lower()):
            result = True
            # duplicate hece skipped
            #print('   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   - SKIPPED')
            break
    return result

def add_to_file(list):
    f= open('BFS_URLs.txt','w')
    for element in list:
        f.write(str(element[0])+'\n')
        #download_page(str(element[0]))
    f.close()
    print('\n\tCrawled urls saved to file successfully')



def download_page(url):
    filename = os.getcwd()+"/BFS_crawler_files/"+url.split('/wiki/')[-1] + '.txt'
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    else:
        #print('File already present')
        return ## Don't download this page and move onto next

    r = requests.get(url, stream=True) # what is stream paramater ??
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    f.close()
    #print('        /'+ url.split('/wiki/')[-1])

def download_urls(list):
    i=0
    print('\n\tDownloading pages .............')
    for element in list:
        download_page(str(element[0]))
        time.sleep(0.2) # change to 1.5 or as per assignment
        i+=1
    print('\n\t{} pages downloaded.'.format(i))

# test for repetition of links - whether that module is working fine or not??
# generalize for max level as 6
def bfs_crawler(frontier, max_links, max_levels):
    #max_links = 1000
    #max_levels = 6 # seed is considered 1 in my case

    # initailize
    queue = [[frontier,1]]  # Queue stores link, and the level in BFS tree. # seed at level 1
    crawled_urls = []
    processed = []
    level = queue[0][1]  # seed at level 1
    print('                start level : {} '.format(level))
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
                if (valid_URL(str(link.get('href')))
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



def main():                      # Define the main function
    # initializaing attributes
    total_links = 1000;     # total number of valid links that we need to crawl

    # valid links :
    max_depth = 6           # max depth allowed in BFS tree
    seed = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    start_time = time.clock()
    crawled_urls = bfs_crawler(seed,total_links,max_depth)
    print("\n\tTime taken by BFS crawler : ",time.clock() - start_time," seconds")

    add_to_file(crawled_urls)  # adding unique crawled urls to file
    download_urls(crawled_urls) # downloading the webpage[raw html] for crawled urls



main()                           # Invoke the main function

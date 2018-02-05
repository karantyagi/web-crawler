# importing dependencies

import os
import time
import requests
from bs4 import BeautifulSoup

# global variables
count = 0

# -------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------

''' The search graph consists of nodes.
    Each node is a list : [url string, level], where level is the level of the
    node in the BFS search tree.

'''

# Given   : a list
# Returns : true iff list is empty else false
def empty(list):
    if len(list)==0:
        return True
    else:
        return False


# 2 0- try to optimize design  - you are passing same thing from 1st to 2nd to 3rd function -find a better way
def valid_URL(url_string):
    if len(url_string)>0:
        if (url_string[0:5] == '/wiki' and not( ':' in url_string or  '.' in url_string or '#' in url_string)):
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
    f= open('DFS_URLs.txt','w')
    i = 0;
    for element in list:
        f.write(str(element[0])+'\n')
        #download_page(str(element[0]))
        i+=1
    f.close()
    print('\n\tCrawled urls saved to file successfully')
    print('\n\tTotal crawled URLs : {} '.format(i))



def download_page(url):
    filename = os.getcwd()+"/DFS_crawler_files/"+url.split('/wiki/')[-1] + '.txt'
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

# node['url',depth]
def findValidLinks(node):
    neighbours = []
    time.sleep(1.2)
    page = requests.get(str(node[0]))  # url from node
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    links = parsed_page.find("div", {"id": "bodyContent"}).findAll('a')
    #print('\tTotal neighbours {}'.format(len(links)))

    for link in links:
        if (valid_URL(str(link.get('href')))
        and link.parent.get('class') != ['hatnote', 'navigation-not-searchable']
        and link.parent.get('class') != ['thumb tleft']
        and link.parent.get('class') != ['thumb tright']):
            if link.findParents("table", {"class": "infobox"}) != [] :
                #print(' infobox link')
                continue
            neighbours.append(['https://en.wikipedia.org'+str(link.get('href')),(node[1]+1)]) #any random depth


    #print('\tTotal valid neighbours :  {}'.format(len(neighbours)))
    return neighbours


def recursive_dfs(node, visited):
    #recursive depth first search from start till max depth of 6
    global count
    global max_links
    global max_depth
    if count > max_links :
        return visited
    else:
        print('\t URLs crawled : {}'.format(count))
        #print('\t Max links          : {}'.format(max_links))
        visited.append(node)
        count+=1
        print('\tLink {}'.format(count).ljust(10) +': {}'.format(node[0]).ljust(90)+'Depth : {}'.format(node[1]))
        neighbours = findValidLinks(node)
        #print('\tNeighbours :  {}'.format(len(neighbours)))

        if len(neighbours) >0:
            #print('\t TEST Neighbour 1 :  {}'.format(neighbours[0]))
            for neighbor in neighbours:
                if node[1] < max_depth:
                    if neighbor not in visited:
                        visited = recursive_dfs(neighbor,visited)
                else:
                    break

        return visited




def dfs_crawler(frontier):

    global max_links
    global max_depth
    root_node = [frontier,1]  # start at depth 1
    crawled_urls = [] # has no url node
    visited = [] # has no nodes
    print('\n\tSeed Link :  {}'.format(root_node))
    #print('\tMax Links allowed :  {}'.format(max_links))
    #print('\tMax Depth allowed :  {}'.format(max_depth))
    visited = recursive_dfs(root_node,visited)
    #print('\n\tControl back to dfs_crawler()')
    return visited

if __name__ == "__main__":                      #  main function

    global max_links
    global max_depth
    # initializaing attributes
    max_links = 15 # total number of valid links that we need to crawl
    max_depth =  6 # max depth allowed in DFS tree
    seed = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    start_time = time.clock()
    crawled_urls= dfs_crawler(seed)
    print("\n\tTime taken by DFS crawler : ",time.clock() - start_time," seconds")

    crawled_urls.pop(0)
    add_to_file(crawled_urls)  # adding unique crawled urls to file
    #download_urls(crawled_urls) # downloading the webpage[raw html] for crawled urls

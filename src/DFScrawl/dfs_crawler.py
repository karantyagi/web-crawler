# importing dependencies

import os
import time
import requests
from bs4 import BeautifulSoup

#global variables
count = 0

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


# Given   : a url string
# Returns : true iff it is a valid string
def valid_URL(url_string):
    if len(url_string)>0:
        if (url_string[0:5] == '/wiki' and not( ':' in url_string or  '.' in url_string or '#' in url_string)):
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
    f= open('DFS_URLs.txt','w')
    i = 0
    for element in list:
        f.write(str(element[0])+'\n')
        i+=1
    f.close()
    print('\n\tCrawled urls successfully saved to file : DFS_URLs.txt')
    print('\n\tTotal crawled URLs : {} '.format(i))


# Given    :  a node
# Returns  :  find all its immediate neighbours which are valid urls
def findValidLinks(node):
    neighbours = []
    time.sleep(1.2)# Politeness policy: Wait sometime before processing another node,
                    # as processing a nodes uses GET request
    page = requests.get(str(node[0]))  # url from node
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    links = parsed_page.find("div", {"id": "bodyContent"}).findAll('a')
    # all <a> tags inide div with class bodyContent are collected in Links

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
            neighbours.append(['https://en.wikipedia.org'+str(link.get('href')),(node[1]+1)]) #any random depth
    return neighbours


def recursive_dfs(node, visited):
    #recursive depth first search from start till max depth of 6
    global count
    global max_links
    global max_depth
    if count > max_links :
        return visited
    else:
        #print('\t URLs crawled : {}'.format(count))
        visited.append(node)
        count+=1
        #print('\tLink {}'.format(count).ljust(10) +': {}'.format(node[0]).ljust(90)+'Depth : {}'.format(node[1]))
        neighbours = findValidLinks(node)

        if len(neighbours) >0:
            for neighbor in neighbours:
                if node[1] < max_depth:
                    if neighbor not in visited:
                        visited = recursive_dfs(neighbor,visited)
                else:
                    break

        return visited

# Given   : a root_node which contains a seed
# returns : the visited nodes
def dfs_crawler(frontier):

    global max_links
    global max_depth
    root_node = [frontier,1]  # start at depth 1
    crawled_urls = [] # has no url node
    visited = [] # has no nodes
    #print('\n\tSeed Link :  {}'.format(root_node))

    visited = recursive_dfs(root_node,visited)
    #print('\n\tControl back to dfs_crawler()')
    return visited



if __name__ == "__main__":                      #  main function

    global max_links    # maximum no. of links that need to be crawled
    global max_depth     # max depth allowed to be searched in DFS tree

    # initializaing attributes
    max_links = 1000 # total number of valid links that we need to crawl
    max_depth =  6 # max depth allowed in DFS tree
    seed = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    start_time = time.clock()   # for calculating the time taken by focused crawler
    print("\n\tCrawling started, please wait for some time . . . ")
    crawled_urls= dfs_crawler(seed)
    print("\n\tTime taken by DFS crawler (without downloading) : ",time.clock() - start_time," seconds ")

    crawled_urls.pop(0)        # we don't want to save the seed link in the file
    add_to_file(crawled_urls)  # adding unique crawled urls to file

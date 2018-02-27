Installation

1.  Install Python 3.6.3
2.  Install pip if not present
3.  Install the required dependencies

Install the dependencies from requirements.txt file by using :
$ pip install -r requirements.txt
---------------------------------------------------------------------------

Compiling and running the files

$ python bfs_crawler.py  :  For BFS crawler
Note : The download function is commented out in the main function, to download the 1000 webpages you need to uncomment the download_urls function

$ python dfs_crawler.py      :  For DFS crawler
$ python focused_crawler.py  :  For Focused crawler
---------------------------------------------------------------------------

Sources used :

1) http://docs.python-requests.org/en/master/
2) https://www.crummy.com/software/BeautifulSoup/bs4/doc/
3) https://docs.python.org/3/library/time.html
4) https://docs.python.org/3/library/os.html
 -------------------------------------------------------------------------

BFS Crawling 
 Max depth reached :  3
 Links crawled :  1000

DFS Crawling 
 Max depth reached :  6
 Links crawled :  1000

Focused Crawling (Task 2)
 Max depth reached : 6 
 Links crawled : 442
Crawler stopped at 442 links as we exhausted all valid links at level 6.
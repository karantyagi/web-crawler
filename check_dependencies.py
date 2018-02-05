try:
    import bs4
    from bs4 import BeautifulSoup
except ImportError:
    print("Please install BeautifulSoup.")

try:
    import time
except ImportError:
    print("Please install time.")

try:
    import os
except ImportError:
    print("Please install os.")

try:
    import requests
except ImportError:
    print("Please install requests.")

print('All requirements are satisfied')

import requests
import re
import urllib
from lxml import html
from bs4 import BeautifulSoup as bs4

requests.packages.urllib3.disable_warnings()

opener = urllib.request.build_opener()
opener.addheaders = []
thefile = open('URLliste.txt', 'w+')
failcheck = open('failcheck.txt', 'w+')
allcheck = open('allcheck.txt', 'w+')
washfile = open('washfile.txt', 'w+')
emailsliste = []
linklist = []

def get_links():
    washed = []
    dirty = []
    site = "https://www.google.com/search?q=inurl%3Akemner&num=1000"
    page = opener.open(site)
    soup = bs4(page,'lxml')
    for link in soup.find_all('h3', class_='r'):
        text = link.a['href'][7:]
        head, sep, tail = text.partition('&sa')
        linklist.append(head)
        for link in linklist:
            if 'http' in link and '.kommune.no' in link:
                washfile.write("%s\n" % link)
                washed.append(link)
            else:
                dirty.append(link)
    return list(set(washed))

def get_mails(url):
    try:
        r = requests.get(url)
        soup = bs4(r.content, 'lxml')
        pre = [a["href"] for a in soup.select('a[href^=mailto:]')]
        nyepre = [x.replace('mailto:', '')for x in pre]
            
        return nyepre
    except:
        try:
            r = requests.get(url, verify = False)
            soup = bs4(r.content, 'lxml')
            pre = [a["href"] for a in soup.select('a[href^=mailto:]')]
            nyepre = [x.replace('mailto:', '')for x in pre]
            failcheck.write("%s\n" % url)
           
            return nyepre
        except:
            failcheck.write("%s\n" % url)
            pass
    
count = 0
    
for i in get_links():
    count = count+1
    print(count)
    for x in get_mails(i):
        if x not in emailsliste and "?subject" not in x:
            thefile.write("%s\n" % x.strip("%20"))
            emailsliste.append(x.strip("%20"))
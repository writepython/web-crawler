import os, errno
import urllib, urlparse
from bs4 import BeautifulSoup

from config import urls_to_crawl

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
            
def url_should_be_downloaded(url):
    return True

def download_url(url):
    return True

def add_new_urls(current_url, html):
    parsed_html = BeautifulSoup(html)
    for tag in parsed_html.findAll('a', href=True):
        href_absolute_url = urlparse.urljoin(current_url, tag['href'])
        if current_url in href_absolute_url and href_absolute_url not in all_urls:
            urls_to_visit.append(href_absolute_url)
            all_urls.append(href_absolute_url)

def crawl_url(url):
    print "*** NEW CRAWLING SESSION FOR URL: %s ***" % url

    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop(0)
        urls_visited.append(current_url)
        print "Requesting url: ", current_url
        try:
            html = urllib.urlopen(current_url).read()
            try:
                add_new_urls(current_url, html)
            except:
                print "Error parsing html for url: ", current_url          
        except:
            print "Error accessing url: ", current_url

                
if __name__ == "__main__":
    #output_directory = os.path.join( os.path.dirname(__file__), 'output' )
    print os.getcwd()

    for url in urls_to_crawl:
        initial_url = url
        urls_to_visit = [url]
        all_urls = [url]    
        crawl_url(url)

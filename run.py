import os, errno
#import urllib
import urlparse
import requests
from bs4 import BeautifulSoup

from config import urls_to_crawl, content_types_to_download

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def conditionally_download_file(current_url, html=None):            
    return True

def add_new_urls(current_url, html):
    parsed_html = BeautifulSoup(html)
    for tag in parsed_html.findAll('a', href=True):
        href_absolute_url = urlparse.urljoin(current_url, tag['href'])
        if follow_links_containing in href_absolute_url and href_absolute_url not in all_urls:
            urls_to_visit.append(href_absolute_url)
            all_urls.append(href_absolute_url)

def crawl_url():
    print "*** NEW CRAWLING SESSION FOR URL: %s ***" % initial_url

    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop(0)
        print len(urls_to_visit)
        head_response = requests.head(current_url)
        if head_response.status_code == requests.codes.ok:
            current_url_head_content_type = head_response.headers.get('content-type')
            if current_url_head_content_type == 'text/html':
                get_response = requests.get(current_url)
                if get_response.status_code == requests.codes.ok:
                    html = get_response.text
                    add_new_urls(current_url, html)
                    if 'text/html' in content_types_to_download:
                        conditionally_download_file(current_url, html)
            else:
                
                    

                    
                            r.status_code == requests.codes.ok
                        GET and parse

            potentially download
        else:
            potentially download
            

            r.status_code == requests.codes.ok


        try:
            html = urllib.urlopen(current_url).read()
        except:
            print "Error accessing url: ", current_url
        else:
            try:

            except:
                print "Error parsing html for url: ", current_url
            else:
                try:
                    conditionally_download_url(current_url, html)
                except:
                    print "Error downloading file: ", current_url
if regex1.search(test)
                
if __name__ == "__main__":
    #output_directory = os.path.join( os.path.dirname(__file__), 'output' )
    output_directory = os.path.join( os.getcwd(), "output" )

    for d in urls_to_crawl:
        initial_url = d["url"]
        urls_to_visit = [initial_url]
        all_urls = [initial_url]
        follow_link_containing = d["follow_links_containing"]
        regex_filters = [ re.compile(regex_filter) for regex_filter in d["regex_filters"] ]
        if regex_filters:
            using_regex_filters = True                          
        crawl_url()

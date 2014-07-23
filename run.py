import os, errno
#import urllib
import urlparse
import requests
import mimetypes
from bs4 import BeautifulSoup

from config import urls_to_crawl, file_extensions_to_download

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def download_file(current_url, data):
    """
    Data will either be data from an HTML file or None for other file types
    """
    print "Attempting to download file: ", current_url
    if not data:
        get_response = requests.get(current_url)
        if get_response.status_code == requests.codes.ok:
            data = get_response.text
        else:
            print "Could not get data from file: ", current_url
    if data:
        
def add_new_urls(current_url, html):
    print "Adding new links found at: ", current_url
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
        html_data = None
        found_html = False        
        print "Starting to process url: ", current_url
        print len(urls_to_visit)
        # Look for a valid head response from the URL
        head_response = requests.head(current_url)
        if not head_response.status_code == requests.codes.ok:
            print "Received an invalid head response from URL: ", current_url
        else:
            head_content_type = head_response.headers.get('content-type')
            # If we found an HTML file, grab all the links
            if 'text/html' in head_content_type:
                get_response = requests.get(current_url)
                if get_response.status_code == requests.codes.ok:
                    html_data = get_response.text
                    found_html = True
                    add_new_urls(current_url, html_data)
            # Check if we should download files with this extension
            proper_extension = False
            url_path = urlparse.urlparse(current_url).path
            for file_extension in file_extensions_to_download:
                if file_extension in url_path:
                    proper_extension = True
                    break
                # If we want to download all HTML files and found HTML at a non-standard extension or at "/"
                elif file_extension == '.html' and found_html:
                    proper_extension = True
                    break
                elif file_extension == '.htm' and found_html:
                    proper_extension = True
                    break
            # Check if we should download this file based on regex restrictions, only if it passed the extension test
            if proper_extension:
                if not using_regex_filters:
                    download_file(current_url, html_data)
                else:
                    for regex_filter in regex_filters:
                        if regex_filter.search(current_url):
                            download_file(current_url, html_data)
                            break
            print "Finished processing url: ", current_url
                
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

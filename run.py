import os, errno, string, urlparse, mimetypes
import requests
from bs4 import BeautifulSoup

from config import urls_to_crawl, file_extensions_to_download

fs_path_acceptabl_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._'

fs_path_trans_table  = string.maketrans( fs_path_acceptabl_chars, '_' * len(fs_path_acceptabl_chars) )
    
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def download_file(current_url, data):
    """
    Data will either be data from an HTML file or None
    """
    print "Attempting to download file: ", current_url
    if not data:
        get_response = requests.get(current_url)
        if get_response.status_code == requests.codes.ok:
            data = get_response.text
        else:
            print "Could not get data from file: ", current_url
    if data:
        url_parsed = urlparse.urlparse(current_url)
        netloc = url_parsed.netloc
        url_path = url_parsed.path.strip()
        if url_path in ["/", "", ".", ".."]:
            fs_path = netloc
            with open('workfile', 'r') as f:
            filename = "root.file"
            fs_path = None
        elif url_path.endswith("/"): # Still not catching the edge case where we have file /abc and then later directory /abc/
            fs_path = url_path + "root.file"
        else:
            path = url_path.strip("/")
            path = url_path.split("/")
            path = [ p.translate(fs_path_trans_table) for p in path ]
            path = "/".join(path)


with open('workfile', 'r') as f:            
        #netloc_dir = os.path.join(output_dir, url_parsed.netloc)
        #if not os.path.exists(netloc_dir):
        #mkdir_p(netloc_dir)
        url_path = url_parsed.path
        if url_path.endswith("/") or url_path == "":
            filename = "path_root.html"
        
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
        current_url_parsed = urlparse.urlparse(current_url)        
        html_data = None
        met_mimetype_criteria = False
        met_file_extension_criteria = False                                        
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
                    add_new_urls(current_url, html_data)
            # Check if we should download files with this mimetype or extension
            for mimetype in mimetypes:
                if mimetype in head_content_type:
                    met_mimetype_criteria = True
            if not met_mimetype_criteria:
                for file_extension in file_extensions:
                    if file_extension in current_url: # This could be swapped for urlparse(current_url).path...[-1]
                        met_file_extension_criteria = True                
            # Check if we should download this file based on potential regex restrictions, only if it passes the mimetype or extension tests
            if met_mimetype_criteria or met_file_extension_criteria:
                if not using_regex_filters:
                    download_file(current_url, html_data)
                else:
                    for regex_filter in regex_filters:
                        if regex_filter.search(current_url):
                            download_file(current_url, html_data)
                            break                
            print "Finished processing url: ", current_url
                
if __name__ == "__main__":
    output_dir = os.path.join( os.getcwd(), "output" )
    if not os.path.exists(output_dir):
        mkdir_p(output_dir)
    
    for d in urls_to_crawl:
        initial_url = d["url"]
        urls_to_visit = [initial_url]
        all_urls = [initial_url]
        follow_link_containing = d["follow_links_containing"]
        regex_filters = d.get("regex_filters")
        if regex_filters:
            using_regex_filters = True
            regex_filters = [ re.compile(regex_filter) for regex_filter in regex_filters ]
        else:
            using_regex_filters = False            
        crawl_url()

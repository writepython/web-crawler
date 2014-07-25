import os, re, sys, errno, traceback, string, urlparse, mimetypes
import requests
from bs4 import BeautifulSoup

from config import urls_to_crawl, file_extensions_list, mimetypes_list, request_timeout

fs_path_acceptable_chars = frozenset('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/._')
files_written = 0            
    
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def download_file(current_url, data, encoding):
    """
    Data will either be data from an HTML file or None
    Encoding is the encoding of the data
    """
    print "Attempting to download file"
    if not data:
        get_response = requests.get(current_url, timeout=request_timeout)
        if get_response.status_code == requests.codes.ok:
            data = get_response.text
            encoding = get_response.encoding
        else:
            print "Could not get data from file: ", current_url
    if data:
        url_parsed = urlparse.urlparse(current_url)
        netloc = url_parsed.netloc
        url_path = url_parsed.path.strip().lstrip("/")
        if url_path == "":
            filename = "root.file" # Could also guess extension based on mimetype
            fs_path = netloc
        else:
            if url_path.endswith("/"): # There is still an extreme edge case where we have file /abc and then later directory /abc/
                url_path = url_path + "root.file" # Could also guess extension based on mimetype
            url_path = netloc + "/" + url_path
            url_path = ''.join(c for c in url_path if c in fs_path_acceptable_chars)                
            url_path_list = url_path.split("/")
            filename = url_path_list.pop()
            fs_path = "/".join(url_path_list)            
        fs_path = os.path.join( output_dir, fs_path)
        mkdir_p(fs_path)
        filepath = os.path.join(fs_path, filename)
        print "* Writing file: ", filepath
        with open(filepath, 'w') as f:
            f.write( data.encode(encoding) )
        global  files_written
        files_written += 1        
        
def add_new_urls(current_url, html):
    print "Adding new links"
    parsed_html = BeautifulSoup(html)
    for tag in parsed_html.findAll('a', href=True):
        href_absolute_url = urlparse.urljoin(current_url, tag['href'].strip() ) # Stripping handles <a href=" http...
        if follow_links_containing in href_absolute_url and href_absolute_url not in all_urls:
            urls_to_visit.append(href_absolute_url)
            all_urls.append(href_absolute_url)

def crawl_url():
    print "\n* NEW CRAWLING SESSION FOR URL: %s *\n" % initial_url

    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop(0)
        try:
            current_url_parsed = urlparse.urlparse(current_url)
            html_data = None
            met_mimetype_criteria = False
            met_file_extension_criteria = False                                        
            print "\nSTARTING TO PROCESS URL: %s\n" % current_url
            print "Remaining URLs: %d" % len(urls_to_visit)
            # Look for a valid head response from the URL
            head_response = requests.head(current_url, timeout=request_timeout)
            if not head_response.status_code == requests.codes.ok:
                print "Received an invalid head response"
            else:
                head_content_type = head_response.headers.get('content-type')
                # If we found an HTML file, grab all the links
                if 'text/html' in head_content_type:
                    get_response = requests.get(current_url, timeout=request_timeout)
                    if get_response.status_code == requests.codes.ok:
                        html_data = get_response.text
                        encoding = get_response.encoding                    
                        add_new_urls(current_url, html_data)
                # Check if we should download files with this mimetype or extension
                for mimetype in mimetypes_list:
                    if mimetype in head_content_type:
                        met_mimetype_criteria = True
                if not met_mimetype_criteria:
                    for file_extension in file_extensions_list:
                        if file_extension in current_url: # This could be swapped for urlparse(current_url).path...[-1]
                            met_file_extension_criteria = True                
                # Check if we should download this file based on potential regex restrictions, only if it passes the mimetype or extension tests
                if met_mimetype_criteria or met_file_extension_criteria:
                    if not using_regex_filters:
                        download_file(current_url, html_data, encoding)
                    else:
                        for regex_filter in regex_filters:
                            if regex_filter.search(current_url):
                                download_file(current_url, html_data, encoding)
                                break
            print "Files written: %d" % files_written
            print "Finished processing URL"
        except:
            try:
                traceback_info = '\n'.join(traceback.format_exception(*(sys.exc_info())))
            except:
                traceback_info = ''
            print "*** ERROR PROCESSING: %s ***\nTraceback: %s\n" % ( current_url, traceback_info )
            
if __name__ == "__main__":
    output_dir = os.path.join( os.getcwd(), "output" )
    if not os.path.exists(output_dir):
        mkdir_p(output_dir)
    
    for d in urls_to_crawl:
        initial_url = d["url"]
        urls_to_visit = [initial_url]
        all_urls = [initial_url]
        follow_links_containing = d["follow_links_containing"]
        regex_filters = d.get("regex_filters")
        if regex_filters:
            using_regex_filters = True
            regex_filters = [ re.compile(regex_filter) for regex_filter in regex_filters ]
        else:
            using_regex_filters = False
        crawl_url()

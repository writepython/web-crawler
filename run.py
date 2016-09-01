import os, re, sys, getopt, errno, time, traceback, datetime, string, urlparse, mimetypes, platform
import requests
from bs4 import BeautifulSoup
from functions import mkdir_p, get_selenium_browser, get_filepath, get_encoded_data

from config import urls_to_crawl, file_extensions_list, mimetypes_list, request_delay

USAGE_MESSAGE = 'Usage: run.py -o <output_dir>'
REQUEST_HEADERS = { 'User-Agent': 'Mozilla/5.0' }

def add_new_urls(url, html):
    print "Adding new URLs from page source of URL: %s" % url
    parsed_html = BeautifulSoup(html)
    for tag in parsed_html.findAll('a', href=True):
        href = tag['href'].strip() # Stripping handles <a href=" http...
        anchor_index = href.find("#") 
        if anchor_index != -1:
            href = href[:anchor_index] # We don't care about anchors
        if href:
            if ignore_query_strings:
                query_string_index = href.find("?") 
                if query_string_index != -1:
                    href = href[:query_string_index]
            href_absolute_url = urlparse.urljoin(url, href)
            if href_absolute_url.startswith('http'): # We don't care about mailto:foo@bar.com etc.
                if follow_links_containing in href_absolute_url and href_absolute_url not in all_urls:
                    urls_to_visit.append(href_absolute_url)
                    all_urls.append(href_absolute_url)
        
def crawl_url():
    global errors_encountered
    print "\n* NEW CRAWLING SESSION FOR CONFIG URL: %s *\n" % seed_url

    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop(0)
        try:
            time.sleep(request_delay)
            page_source = None
            met_mimetype_criteria = False
            met_file_extension_criteria = False
            write_file = False                                        
            print "\nProcessing URL: %s\n" % current_url
            # Look for a valid head response from the URL
            print "HEAD Request of URL: ", current_url
            head_response = requests.head(current_url, allow_redirects=True, headers=REQUEST_HEADERS, timeout=60)
            if not head_response.status_code == requests.codes.ok:
                print "Received an invalid HEAD response for URL: ", current_url
            else:
                content_type = head_response.headers.get('content-type')
                encoding = head_response.encoding
                final_url = head_response.url                
                # If we found an HTML file, grab all the links
                if 'text/html' in content_type:
                    print "Requesting URL with Python Requests: ", current_url
                    get_response = requests.get(current_url, headers=REQUEST_HEADERS, timeout=60)
                    content_type = get_response.headers.get('content-type')
                    encoding = get_response.encoding
                    page_source = get_response.text
                    final_url = get_response.url
                    if force_javascript_execution or ('text/html' in content_type and not "<body" in page_source):
                        print "Requesting URL with Selenium: ", final_url
                        try:
                            browser.get(final_url)
                            page_source = browser.page_source                    
                        except:
                            print "First Selenium request failed. Trying one last time."
                            browser.get(final_url)
                            page_source = browser.page_source                    
                        else:
                            if 'text/html' in content_type and not "<body" in page_source:
                                print "No <body> tag found in page source. Requesting URL with Selenium one last time."                        
                                browser.get(final_url)
                                page_source = browser.page_source                                            
                        final_url = browser.current_url
                    add_new_urls(final_url, page_source)
                # Check if we should write files with this mimetype or extension
                for mimetype in mimetypes_list:
                    if mimetype in content_type:
                        met_mimetype_criteria = True
                if not met_mimetype_criteria:
                    url_parsed = urlparse.urlsplit(final_url)
                    url_path = url_parsed.path.strip()
                    for file_extension in file_extensions_list:
                        if url_path.endswith(file_extension):
                            met_file_extension_criteria = True                
                # Check if we should write this file based on potential regex restrictions, only if it passes the mimetype or extension tests
                if met_mimetype_criteria or met_file_extension_criteria:
                    if not using_regex_filters:
                        write_file = True
                    else:
                        for regex_filter in regex_filters:
                            if regex_filter.search(final_url):
                                write_file = True
                                break
                # Write a file if we need to
                if write_file:
                    print "Need to write file"
                    if not page_source:
                        print "Requesting URL with Python Requests: ", final_url
                        get_response = requests.get(final_url, headers=REQUEST_HEADERS, timeout=60)
                        encoding = get_response.encoding
                        page_source = get_response.text
                        final_url = get_response.url
                    encoded_data, encoding_used = get_encoded_data(page_source, encoding)            
                    filepath = get_filepath(final_url, encoding_used, output_dir)
                    with open(filepath, 'w') as f:
                        f.write(encoded_data)
                    print "Wrote file: %s with encoding: %s" % (filepath, encoding_used)
                    global files_written
                    files_written += 1

            global files_processed
            files_processed += 1
            print "Files Found: %d  Processed: %d  Remaining: %d  Written: %d  Operational Errors: %d" % ( len(all_urls), files_processed, len(urls_to_visit), files_written, errors_encountered )
        except:
            errors_encountered += 1
            try:
                traceback_info = '\n'.join(traceback.format_exception(*(sys.exc_info())))
            except:
                traceback_info = ''
            print "*** ERROR PROCESSING: %s ***\nTraceback: %s\n" % ( current_url, traceback_info )

if __name__ == "__main__":
    argv = sys.argv[1:]
    # Find or create output directory
    output_dir = None    
    try:
        opts, args = getopt.getopt(argv, "o:" )
    except getopt.GetoptError:
        print USAGE_MESSAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-o":
            output_dir = arg
    if not output_dir:
        print USAGE_MESSAGE
        sys.exit(2)
    if os.path.isdir(output_dir):
        print "Found directory: %s" % output_dir
    else:
        mkdir_p(output_dir)
        print "Created directory: %s" % output_dir
    # Get URLs from config
    for d in urls_to_crawl:
        files_processed = 0
        files_written = 0            
        errors_encountered = 0
        seed_url = d["url"]
        urls_to_visit = [seed_url]
        all_urls = [seed_url]
        follow_links_containing = d["follow_links_containing"]
        ignore_query_strings = d.get("ignore_query_strings", False)
        force_javascript_execution = d.get("force_javascript_execution", False)
        # Selenium browser
        browser = get_selenium_browser()        
        # Regex
        regex_filters = d.get("regex_filters")
        if regex_filters:
            using_regex_filters = True
            regex_filters = [ re.compile(regex_filter) for regex_filter in regex_filters ]
        else:
            using_regex_filters = False
            
        start_time = datetime.datetime.now()
        print "\nCurrent Time:  %s" % start_time
        crawl_url()
        end_time = datetime.datetime.now()
        print "\nStart:  %s\nFinish: %s\n" % (start_time, end_time)

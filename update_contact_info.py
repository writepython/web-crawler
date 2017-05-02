import os, csv, re, sys, getopt, errno, time, traceback, datetime, string, urlparse, mimetypes, platform
import requests
from bs4 import BeautifulSoup
from functions import mkdir_p, get_filepath, get_encoded_data

USAGE_MESSAGE = 'Usage: update_contact_info.py -i <input_file> -o <output_file>'
REQUEST_HEADERS = { 'User-Agent': 'Mozilla/5.0' }
EMAIL_REGEX = re.compile(r"[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+")

contact_info_dict = {}
ignore_query_strings = False
ignore_anchors = False

def add_contact_info(seed_url, html):
    email_addresses = re.findall(EMAIL_REGEX, html)
    contact_info_dict[seed_url]['email'] = contact_info_dict[seed_url]['email'] + email_addresses

def fits_url_blacklist(url):
    if 'wikipedia' in url.lower():
        return True
    return False

def get_processed_whitelist_url(url):
    # Check if facebook, twitter, last.fm, etc. for an about page, otherwise return None
    if 'facebook.com' in url and not 'about' in url:
        if not url.endswith('/'):
            url = '%s/' % url
        url = urlparse.urljoin(url, 'about')
        return url

    return None

def add_new_urls(url, page_source):
    if fits_url_blacklist(url):
    print "Adding new URLs from page source of URL: %s" % url
    parsed_html = BeautifulSoup(page_source)
    for tag in parsed_html.findAll('a', href=True):
        href = tag['href'].strip() # Stripping handles <a href=" http...
        if ignore_anchors:
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
                if fits_url_blacklist(href_absolute_url): # Ignore blacklisted
                    continue
                if contact_info_dict[seed_url]['final_url_hostname'] in final_url: # Part of the same domain                                
                    if href_absolute_url not in all_urls:                
                        urls_to_visit.append(href_absolute_url)
                        all_urls.append(href_absolute_url)
                else: # Check a whitelist of URLs that we will potentially modify
                    processed_url = get_processed_whitelist_url(final_url)
                    if processed_url:                    
                        if processed_url not in all_urls:                
                            urls_to_visit.append(processed_url)
                            all_urls.append(processed_url)
        
def crawl_url(seed_url):
    global errors_encountered
    print "\n* NEW CRAWLING SESSION FOR URL: %s *\n" % seed_url
    contact_info_dict[seed_url] = { 'final_url': '', 'final_url_hostname': '', 'email': [], 'phone': [], 'twitter': [] }
    is_seed_url = True
    
    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop(0)
        do_get_request = False
        do_add_urls = False
        try:
            # time.sleep(request_delay)
            if fits_url_blacklist(final_url):
                continue
            print "\nProcessing URL: %s\n" % current_url            
            get_response = requests.get(final_url, headers=REQUEST_HEADERS, timeout=60)
            content_type = get_response.headers.get('content-type')
            if 'text/html' in content_type:                
                final_url = get_response.url
                final_url_parsed = urlparse.urlsplit(final_url)
                final_url_hostname = final_url_parsed.hostname
                if is_seed_url:
                    contact_info_dict[seed_url]['final_url'] = final_url
                    contact_info_dict[seed_url]['final_url_hostname'] = final_url_hostname
                page_source = get_response.text
                if page_source:
                    add_contact_info(seed_url, page_source)
                    if is_seed_url:
                        add_new_urls(seed_url, page_source)
                    elif contact_info_dict[seed_url]['final_url_hostname'] in final_url:
                        add_new_urls(seed_url, page_source)
                ## else:
                ## if 'text/html' in content_type:
                ##     final_url = head_response.url
                ##     final_url_parsed = urlparse.urlsplit(final_url)
                ##     final_url_hostname = final_url_parsed.hostname
                ##     if is_seed_url:
                ##         contact_info_dict[seed_url]['final_url'] = final_url
                ##         contact_info_dict[seed_url]['final_url_hostname'] = final_url_hostname
                ##     if fits_url_blacklist(final_url):
                ##         continue
                ##     if contact_info_dict[seed_url]['final_url_hostname'] in final_url:
                ##         do_get_request = True
                ##         do_add_urls = True
                ##     else:
                ##         final_url = get_processed_whitelist_url(final_url)
                ##         if final_url:
                ##             do_get_request = True
                ##     if do_get_request:
                ##         print "Requesting URL with Python Requests: ", current_url
                ##         get_response = requests.get(final_url, headers=REQUEST_HEADERS, timeout=60)
                ##         content_type = get_response.headers.get('content-type')
                ##         if 'text/html' in content_type:
                ##             page_source = get_response.text
                ##             if page_source:
                ##                 add_contact_info(seed_url, page_source)
                ##                 if do_add_urls:
                ##                     add_new_urls(seed_url, page_source)

            is_seed_url = False                                    
            global files_processed
            files_processed += 1
            print "Files Found: %d  Processed: %d  Remaining: %d  Contact Items Found: %d  Operational Errors: %d" % ( len(all_urls), files_processed, len(urls_to_visit), contact_items_found, errors_encountered )
            print contact_info_dict
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
    output_file = None
    input_file = None
    try:
        opts, args = getopt.getopt(argv, "i:o:" )
    except getopt.GetoptError:
        print USAGE_MESSAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            input_file = arg
        if opt == "-o":
            output_file = arg
    if not input_file or not output_file:
        print USAGE_MESSAGE
        sys.exit(2)
    with open(input_file) as f:
        urls = f.readlines()
    print "Found %d URLs" % len(urls)

    with open(output_file, 'wb') as f:
        csv_writer = csv.writer(f)        
        for url in urls:
            url = url.strip()
            if not url:
                continue
            files_processed = 0
            errors_encountered = 0
            contact_items_found = 0
            urls_to_visit = [url]
            all_urls = [url]

            start_time = datetime.datetime.now()
            print "\nCurrent Time:  %s" % start_time
            crawl_url(url)
            end_time = datetime.datetime.now()
            print contact_info_dict
            print "\nStart:  %s\nFinish: %s\n" % (start_time, end_time)

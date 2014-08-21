import os, re, sys, errno, time, traceback, datetime, string, urlparse, mimetypes, platform
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from config import urls_to_crawl, file_extensions_list, mimetypes_list, request_timeout, request_delay, use_selenium, browser_name

request_headers = { 'User-Agent': 'Mozilla/5.0' }
        
def add_new_urls(url, html):
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
            html_data = None
            met_mimetype_criteria = False
            met_file_extension_criteria = False                                        
            print "\nProcessing URL: %s\n" % current_url

            # Look for a valid head response from the URL
            print "HEAD Request of URL: ", current_url
            head_response = requests.head(current_url, allow_redirects=True, headers=request_headers, timeout=request_timeout)
            if not head_response.status_code == requests.codes.ok:
                print "Received an invalid HEAD response for URL: ", current_url
            else:
                head_content_type = head_response.headers.get('content-type')
                encoding = head_response.encoding                                    
                # If we found an HTML file, grab all the links
                if 'text/html' in head_content_type:
                    try:
                        final_url, html_data = get_request(current_url)
                    except:
                        # Show error message and move on to next URL
                        print "Received an error requesting URL: ", current_url
                        continue
                    else:
                        add_new_urls(final_url, html_data)
                # Check if we should write files with this mimetype or extension
                for mimetype in mimetypes_list:
                    if mimetype in head_content_type:
                        met_mimetype_criteria = True
                if not met_mimetype_criteria:
                    for file_extension in file_extensions_list:
                        if file_extension in final_url: # This could be swapped for urlsplit(final_url).path...[-1]
                            met_file_extension_criteria = True                
                # Check if we should write this file based on potential regex restrictions, only if it passes the mimetype or extension tests
                if met_mimetype_criteria or met_file_extension_criteria:
                    if not using_regex_filters:
                        if not html_data:
                            final_url, html_data = get_request(current_url)
                        write_file(final_url, html_data, encoding)
                    else:
                        for regex_filter in regex_filters:
                            if regex_filter.search(final_url):
                                if not html_data:
                                    final_url, html_data = get_request(current_url)                                
                                write_file(final_url, html_data, encoding)
                                break
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
    output_dir = os.path.join( os.getcwd(), "output" )
    if not os.path.exists(output_dir):
        mkdir_p(output_dir)
    
    for d in urls_to_crawl:
        files_processed = 0
        files_written = 0            
        errors_encountered = 0
        seed_url = d["url"]
        urls_to_visit = [seed_url]
        all_urls = [seed_url]
        follow_links_containing = d["follow_links_containing"]
        ignore_query_strings = d.get("ignore_query_strings", False)
        # Selenium browser
        if not use_selenium:
            get_request = python_request
        else:
            get_request = selenium_request                
            if browser_name == "PhantomJS":
                user_os = platform.system()
                if user_os == "Darwin":
                    phantomjs_filepath = "phantomjs/phantomjs_mac"
                elif user_os == "Linux":
                    user_machine = platform.machine()
                    if user_machine == "x86_64":
                        phantomjs_filepath = "phantomjs/phantomjs_linux_64"        
                    else:
                        phantomjs_filepath = "phantomjs/phantomjs_linux_i686"        
                phantomjs_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), phantomjs_filepath )
                browser = webdriver.PhantomJS(executable_path=phantomjs_path)
            elif browser_name == "Firefox":
                browser = webdriver.Firefox()
            elif browser_name == "Chrome":
                browser = webdriver.Chrome()
            elif browser_name == "Safari":
                browser = webdriver.Safari()
            elif browser_name == "Opera":
                browser = webdriver.Opera()                                       
            browser.set_page_load_timeout(request_timeout)        
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

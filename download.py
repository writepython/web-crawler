import os, sys, getopt, traceback
import requests
from functions import mkdir_p, get_selenium_browser, get_filepath, get_encoded_data

USAGE_MESSAGE = 'Usage: download.py -i <input_file> -o <output_dir>'
REQUEST_HEADERS = { 'User-Agent': 'Mozilla/5.0' }

def main(argv):
    input_file = None
    output_dir = None
    failed_urls = []
    errors_encountered = 0
    try:
        opts, args = getopt.getopt(argv, "i:o:" )
    except getopt.GetoptError:
        print USAGE_MESSAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            input_file = arg
        if opt == "-o":
            output_dir = arg
    if not input_file or not output_dir:
        print USAGE_MESSAGE
        sys.exit(2)
    if os.path.isdir(output_dir):
        print "Found directory: %s" % output_dir
    else:
        mkdir_p(output_dir)
        print "Created directory: %s" % output_dir
    with open(input_file) as f:
        urls = f.readlines()
    print "Found %d URLs" % len(urls)
    browser = get_selenium_browser()
    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:
            print "\nProcessing URL: %s" % url
            print "Requesting URL with Python Requests: ", url
            get_response = requests.get(url, headers=REQUEST_HEADERS, timeout=60)
            content_type = get_response.headers.get('content-type')
            encoding = get_response.encoding
            page_source = get_response.text
            final_url = get_response.url
            if 'text/html' in content_type and not "<body" in page_source:
                print "No <body> tag found in page source. Requesting URL with Selenium: ", final_url
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
            print "Found final URL: %s" % final_url
            encoded_data, encoding_used = get_encoded_data(page_source, encoding)            
            filepath = get_filepath(final_url, encoding_used, output_dir)
            with open(filepath, 'w') as f:
                f.write(encoded_data)
            print "Wrote file: %s with encoding: %s" % (filepath, encoding_used)
        except:
            errors_encountered += 1
            failed_urls.append(url)
            try:
                traceback_info = '\n'.join(traceback.format_exception(*(sys.exc_info())))
            except:
                traceback_info = ''
            print "*** ERROR PROCESSING: %s ***\nTraceback: %s\n" % ( url, traceback_info )

    print "\nOperational Errors: %d\n" % errors_encountered
    if failed_urls:
        print "The following %d URLs failed:" % len(failed_urls)
        for url in failed_urls:
            print url
    
if __name__ == "__main__":
    main(sys.argv[1:])    

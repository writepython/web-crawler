import os, csv, re, sys, getopt, errno, time, traceback, datetime, string, urlparse, mimetypes, platform
import requests
from bs4 import BeautifulSoup
from functions import mkdir_p, get_filepath, get_encoded_data

USAGE_MESSAGE = 'Usage: update_contact_info.py -i <input_file> -o <output_file>'
REQUEST_HEADERS = { 'User-Agent': 'Mozilla/5.0' }
EMAIL_REGEX = re.compile(r"[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+")

ignore_query_strings = False
ignore_anchors = False
site_urls_cutoff = 36
current_row = 0
contact_info_dict = {}

BLACKLISTED_ENDINGS = (
    '.mp3', '.wav', '.m4a', '.3gp', '.ogg', '.flac', '.wma', '.aiff', '.m3u',
    '.mp4', '.mov', '.m4v', '.wmv', 
    '.jpg', '.jpeg', '.png', '.gif',
    '.7z', '.zip', '.cals', '.tar', '.gz',
    '.pdf',
)

def add_contact_info(seed_url, html):
    email_addresses = []
    html = html.replace('&#064;', '@')
    potential_email_addresses = list(set(re.findall(EMAIL_REGEX, html)))
    if potential_email_addresses:
        for potential_email in potential_email_addresses:
            if not potential_email.lower().endswith(BLACKLISTED_ENDINGS):
                email_addresses.append(potential_email)
    if email_addresses:
        contact_info_dict[seed_url]['email'] = list(set(contact_info_dict[seed_url]['email'] + email_addresses))

def fits_url_blacklist(url):
    # BLACKLISTED_CONTAINS = ['wikipedia', 'youtube', 'facebook', 'twitter', 'last.fm', 'tumblr', 'myspace', 'instagram']
    if url.lower().endswith(BLACKLISTED_ENDINGS):
        return True
    
    return False

def get_modified_seed_url(url):
    # Modify certain URLs like facebook, twitter, last.fm, etc. to get about page. Blacklist certain others.
    if 'facebook.com' in url:
        ## if not 'facebook.com/pg' in url:
        ##     url = url.replace('facebook.com', 'facebook.com/pg')
        if not 'about' in url:
            if not url.endswith('/'):
                url = '%s/' % url
            url = urlparse.urljoin(url, 'about')
        return url
    elif fits_url_blacklist(url):
        return None
    return url

def add_new_urls(url, seed_url, page_source):
    # print "Adding new URLs from page source of URL: %s" % url
    # if 'facebook' in seed_url:
    #     return True
    parsed_html = BeautifulSoup(page_source)
    for tag in parsed_html.findAll('a', href=True):
        if len(all_urls) > site_urls_cutoff:
            # print "Reached site URLs cutoff for %s" % seed_url
            return True
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
                href_absolute_url = get_modified_seed_url(href_absolute_url)
                if href_absolute_url:
                    #if contact_info_dict[seed_url]['seed_url_hostname'] in href_absolute_url or contact_info_dict[seed_url]['final_url_hostname'] in href_absolute_url: # Part of the same domain as the seed URL                               
                    if href_absolute_url not in all_urls:                
                        urls_to_visit.append(href_absolute_url)
                        all_urls.append(href_absolute_url)
        
def crawl_url(seed_url, musicbrainz_id, musicbrainz_name):
    global errors_encountered
    global current_row
    global contact_info_dict
    current_row += 1
    # print "\n* (%d) NEW CRAWLING SESSION FOR URL: %s *\n" % (current_row, seed_url)
    # contact_info_dict[seed_url] = { 'seed_url_hostname': '', 'final_url': '', 'final_url_hostname': '', 'email': [], 'phone': [], 'twitter': [] }
    contact_info_dict[seed_url] = { 'seed_url_hostname': '', 'final_url': '', 'final_url_hostname': '', 'email': [] }
    is_seed_url = True
    
    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop(0)
        try:
            # time.sleep(request_delay)
            # print "\nProcessing URL: %s\n" % current_url
            head_response = requests.head(current_url, allow_redirects=True, headers=REQUEST_HEADERS, timeout=30)
            if head_response.status_code == requests.codes.ok:
            # if head_response.status_code:                
                content_type = head_response.headers.get('content-type')                    
                if 'text/html' in content_type:            
                    get_response = requests.get(current_url, headers=REQUEST_HEADERS, timeout=30)
                    content_type = get_response.headers.get('content-type')
                    if 'text/html' in content_type:                
                        final_url = get_response.url
                        final_url_hostname = urlparse.urlsplit(final_url).hostname
                        if is_seed_url:
                            seed_url_hostname = urlparse.urlsplit(seed_url).hostname
                            contact_info_dict[seed_url]['final_url'] = final_url
                            contact_info_dict[seed_url]['final_url_hostname'] = final_url_hostname                    
                            contact_info_dict[seed_url]['seed_url_hostname'] = seed_url_hostname
                        page_source = get_response.text
                        if page_source:
                            add_contact_info(seed_url, page_source)
                        if is_seed_url: # and 'facebook' not in final_url:
                            add_new_urls(final_url, seed_url, page_source)
                        # elif contact_info_dict[seed_url]['seed_url_hostname'] in final_url:
                        #     add_new_urls(final_url, seed_url, page_source)
                        # elif contact_info_dict[seed_url]['final_url_hostname'] in final_url:
                        #     add_new_urls(final_url, seed_url, page_source)                        

            is_seed_url = False                                    
            global files_processed
            files_processed += 1
            # print "Files Found: %d  Processed: %d  Remaining: %d  Operational Errors: %d" % ( len(all_urls), files_processed, len(urls_to_visit), errors_encountered )
            # print contact_info_dict
            if len(urls_to_visit) == 0:
                for email in contact_info_dict[seed_url]['email']:
                    csv_writer.writerow([ musicbrainz_id, musicbrainz_name, seed_url, contact_info_dict[seed_url]['seed_url_hostname'], contact_info_dict[seed_url]['final_url'], contact_info_dict[seed_url]['final_url_hostname'], email ])
                contact_info_dict = {}
                if files_processed % 2 == 0:
                    f.flush()
        except:
            errors_encountered += 1
            try:
                traceback_info = '\n'.join(traceback.format_exception(*(sys.exc_info())))
            except:
                traceback_info = ''
            # print "*** ERROR PROCESSING: %s ***\nTraceback: %s\n" % ( current_url, traceback_info )

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

    with open(output_file, 'wb') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([ 'Artist ID', 'Artist Name', 'seed_url', 'seed_url_hostname', 'final_url', 'final_url_hostname', 'email' ])
        f.flush()
        with open(input_file, 'rb') as r:
            musicbrainz_url_reader = csv.reader(r)
            for reader_row in musicbrainz_url_reader:

                    musicbrainz_id = reader_row[0]
                    musicbrainz_name = reader_row[1]
                    url = reader_row[2].strip()
                    if not url:
                        continue
                    url = get_modified_seed_url(url)
                    if not url:
                        continue            
                    files_processed = 0
                    errors_encountered = 0
                    urls_to_visit = [url]
                    all_urls = [url]

                    start_time = datetime.datetime.now()
                    print "\nCurrent Time:  %s" % start_time
                    crawl_url(url, musicbrainz_id, musicbrainz_name)
                    end_time = datetime.datetime.now()
                    print "\nStart:  %s\nFinish: %s\n" % (start_time, end_time)


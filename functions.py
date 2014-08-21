import os, re, errno, urlparse

fs_path_bad_chars_re = re.compile(r"[^0-9a-zA-Z/._?%=-]") # The / char will be split out later
request_headers = { 'User-Agent': 'Mozilla/5.0' }

def mkdir_p(path):
    """ Emulates UNIX mkdir -p """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def get_filepath(url, encoding, output_dir):
    """
    Turns a URL string into a valid filesystem path and filename with the encoding is built into the filename.
    Returns the filepath to be passed to the write_file function.
    """
    url_parsed = urlparse.urlsplit(url)
    netloc = url_parsed.netloc
    url_path = url_parsed.path.strip().lstrip("/")
    query_string = url_parsed.query
    if query_string:
        url_path = url_path + '?' + query_string
    if url_path == "":
        filename = "root_" + encoding + ".file"
        fs_path = netloc
    else:
        if url_path.endswith("/"): 
            url_path = url_path + "root" 
        url_path = netloc + "/" + url_path
        url_path_sanitized = fs_path_bad_chars_re.sub('_', url_path)
        url_path_list = url_path_sanitized.split("/")
        filename = url_path_list.pop()
        filename = filename[:240] + "_" + encoding + ".file" # Most systems have a 255 char limit on filenames
        fs_path = "/".join(url_path_list)            
    fs_path = os.path.join( output_dir, fs_path)
    mkdir_p(fs_path)
    filepath = os.path.join(fs_path, filename)
    return filepath

def get_encoded_data(data, encoding):
    encoded_data = None
    print "Encoding data with encoding %s" % encoding
    try:
        encoded_data = data.encode(encoding)
    except:
        print "Could not encode data with encoding %s. Trying UTF-8 instead" % encoding
        encoding = 'utf-8'
        encoded_data = data.encode('utf-8')
    return encoded_data, encoding
    
def write_file(data, filepath):
    with open(filepath, 'w') as f:
        f.write(data)
        print "Wrote file: %s" % filepath

def get_response_data(url):
    
def selenium_request(url):
    "Uses Selenium browser to returns a tuple of (final_url, page_source)"
    try:
        # Get final URL after HTTP and JS redirects
        print "Requesting URL with Selenium: ", url
        browser.get(url)
        final_url = browser.current_url
        if final_url not in all_urls:
            all_urls.append(final_url)
        page_source = browser.page_source
        print "Found final URL: ", final_url
        return final_url, page_source
    except:
        # If we get an error, try one last time
        print "Requesting URL with Selenium: ", url
        browser.get(url)
        final_url = browser.current_url
        if final_url not in all_urls:
            all_urls.append(final_url)
        page_source = browser.page_source
        print "Found final URL: ", final_url
        return final_url, page_source

def python_request(url):
    "Uses Python Requests Library to returns a tuple of (final_url, page_source)"
    try:
        # Get final URL after HTTP redirects
        print "Requesting URL with Python Requests: ", url
        get_response = requests.get(url, headers=request_headers, timeout=request_timeout)
        final_url = get_response.url
        if final_url not in all_urls:
            all_urls.append(final_url)
        page_source = get_response.text
        print "Found final URL: ", final_url
        return final_url, page_source
    except:
        print "Requesting URL with Python Requests: ", url
        get_response = requests.get(url, headers=request_headers, timeout=request_timeout)
        final_url = get_response.url
        if final_url not in all_urls:
            all_urls.append(final_url)
        page_source = get_response.text
        print "Found final URL: ", final_url
        return final_url, page_source    
                
#############


                global files_written
                files_written += 1                

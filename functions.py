import os, re, errno, urlparse, platform
from selenium import webdriver

FS_PATH_BAD_CHARS_RE = re.compile(r"[^0-9a-zA-Z/._?%=-]") # The / char will be split out later

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
    file_extension = os.path.splitext(url_path)[1]
    if not file_extension:
        file_extension = '.file'
    query_string = url_parsed.query
    if query_string:
        url_path = url_path + '?' + query_string
    if url_path == "":
        filename = "root_" + encoding + file_extension
        fs_path = netloc
    else:
        if url_path.endswith("/"): 
            url_path = url_path + "root" 
        url_path = netloc + "/" + url_path
        url_path_sanitized = FS_PATH_BAD_CHARS_RE.sub('_', url_path)
        url_path_list = url_path_sanitized.split("/")
        filename = url_path_list.pop()
        filename = filename[:240] + "_" + encoding + file_extension # Most systems have a 255 char limit on filenames
        fs_path = "/".join(url_path_list)            
    fs_path = os.path.join( output_dir, fs_path)
    mkdir_p(fs_path)
    filepath = os.path.join(fs_path, filename)
    return filepath

def get_encoded_data(data, encoding):
    encoded_data = None
    if encoding:
        print "Encoding data with encoding: %s" % encoding
        try:
            encoded_data = data.encode(encoding)
        except:
            print "Could not encode data with encoding: %s. Trying UTF-8 instead." % encoding
    if not encoded_data:
        encoding = 'utf-8'
        encoded_data = data.encode('utf-8')
    return encoded_data, encoding

def get_selenium_browser(browser_name="PhantomJS", request_timeout=60):
    if browser_name == "PhantomJS":
        user_os = platform.system()
        if user_os == "Darwin":
            phantomjs_filepath = "phantomjs/phantomjs_mac"
        elif user_os == "Linux":
            user_machine = platform.machine()
            if user_machine == "x86_64":
                phantomjs_filepath = "phantomjs/phantomjs_linux_64_1.9.7"        
            else:
                phantomjs_filepath = "phantomjs/phantomjs_linux_i686_1.9.7"        
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
    return browser

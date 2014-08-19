import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def write_file(url, data, encoding, output_dir):
    """
    Data is the response body.
    Encoding is the encoding of the data as specified by the response header.
    """
    if not data:
        print "No data for URL: %s" % url
    else:
        url_parsed = urlparse.urlsplit(url)
        netloc = url_parsed.netloc
        url_path = url_parsed.path.strip().lstrip("/")
        query_string = url_parsed.query
        if query_string:
            url_path = url_path + '?' + query_string
        if url_path == "":
            filename = "root.file" 
            fs_path = netloc
        else:
            if url_path.endswith("/"): 
                url_path = url_path + "root" 
            url_path = netloc + "/" + url_path
            url_path_sanitized = fs_path_bad_chars_re.sub('_', url_path)
            url_path_list = url_path_sanitized.split("/")
            filename = url_path_list.pop()
            filename = filename[:249] + ".file" # Most systems have a 255 char limit on filenames
            fs_path = "/".join(url_path_list)            
        fs_path = os.path.join( output_dir, fs_path)
        mkdir_p(fs_path)
        filepath = os.path.join(fs_path, filename)
        encoded_data = None
        print "Encoding data with encoding %s" % encoding
        try:
            encoded_data = data.encode(encoding)
            print "Could not encode data with encoding %s. Trying UTF-8 instead" % encoding            
        except:
            # In case the encoding specified by the web server is wrong, try again with UTF-8
            encoded_data = data.encode('utf-8')
        if encoded_data:
            with open(filepath, 'w') as f:
                f.write( encoded_data)
                print "Wrote file: %s" % filepath
                global files_written
                files_written += 1        


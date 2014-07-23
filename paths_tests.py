import os, urlparse

unacceptable_directory_names = [ ".", "..", "/" ]
acceptable_path_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._'

urls = ["http://www.google.com", "http://www.google.com/", "http://www.google.com/a/", "http://www.google.com/a"]

output_dir = os.path.join( os.getcwd(), 'output' )
if not os.path.exists(output_dir):
    mkdir_p(output_dir)

for url in urls:
    url_parsed = urlparse.urlparse(url)
    url_netloc = url_parsed.netloc
    url_path = url_parsed.path.strip("/")
    dir_path_sections = [ url_netloc ]
    for p in url_path.split('/'):
        dir_path_sections.append(p)
    netloc_dir = os.path.join( output_dir, url_parsed.netloc)
    if not os.path.exists(netloc_dir):
        mkdir_p(netoc_dir)

        # If no file extension, add GUID and treat as file

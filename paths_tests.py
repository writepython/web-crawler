import os, urlparse

file_extensions_to_download = ['.html', '.htm']
unacceptable_directory_names = [ ".", "..", "/" ]
acceptable_path_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._'

urls = ["http://www.google.com", "http://www.google.com/", "http://www.google.com/a/", "http://www.google.com/a", ]

output_dir = os.path.join( os.getcwd(), 'output' )
if not os.path.exists(output_dir):
    mkdir_p(output_dir)

for url in urls:
    url_parsed = urlparse.urlparse(url)
    url_netloc = url_parsed.netloc
    url_path = url_parsed.path.strip().strip("/")
    if url_path and "/" in url_path:    
        url_path_split = url_path.split('/')
        
        for extension in file_extensions_to_download:
            if 

    dir_path_sections.append(p)
    netloc_dir = os.path.join( output_dir, url_parsed.netloc)
    if not os.path.exists(netloc_dir):
        mkdir_p(netoc_dir)

        # If no file extension, add '.file' extension and treat as file

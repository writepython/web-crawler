request_timeout = 10

mimetypes_list = [ 'text/html' ]
file_extensions_list = []

urls_to_crawl = [
    {
        "url": "http://www.google.com",
        "follow_links_containing": "www.google.com",
        "regex_filters": [r"rya."]
    }
]

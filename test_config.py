request_timeout = 10

mimetypes_list = [ 'text/html' ]
file_extensions_list = []

urls_to_crawl = [
    {
        "url": "http://madeinheights.com",
        "follow_links_containing": "madeinheights.com",
        "regex_filters": [r"story"]
    }
]

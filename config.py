
mimetypes_list = [ 'text/html' ]

file_extensions_list = [ ]

request_timeout = 20

urls_to_crawl = [
    {
        "url": "http://madeinheights.com",
        "follow_links_containing": "madeinheights.com",
        "regex_filters": [ r"st.ry" ]
    },
]

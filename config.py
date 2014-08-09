mimetypes_list = [ ]

file_extensions_list = [ '.html' ]

request_timeout = 20

request_delay = 0

urls_to_crawl = [
    {
        "url": "http://www.cuyoo.com/",
        "follow_links_containing": "cuyoo.com",
        "regex_filters": [ r"/article" ],
        "handle_js_redirects_with_browser": True,
        "ignore_query_strings": True,
    },
]

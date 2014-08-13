mimetypes_list = [ ]

file_extensions_list = [ '.html', '.htm' ]

request_timeout = 60

request_delay = 0

use_selenium = False

browser_name = "Firefox"

urls_to_crawl = [
    {
        "url": "http://madeinheights.com",
        "follow_links_containing": "madeinheights.com",
        "regex_filters": [ r"st.ry" ]
    },
    {
        "url": "http://www.china.com.cn",
        "follow_links_containing": "www.china.com.cn",
        "regex_filters": [ r"/2014-07/\d\d/" ],
        "ignore_query_strings": True,
    }
    ## {
    ##     "url": "http://www.cuyoo.com/",
    ##     "follow_links_containing": "cuyoo.com",
    ##     "regex_filters": [ r"/article" ],
    ##     "ignore_query_strings": True,
    ## },
]

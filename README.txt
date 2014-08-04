=== About ===

- This python web crawler will read in a configuration file containing seed URLs to crawl, and download filtering parameters.  
- A directory called "output" will be created inside the current working directory (the directory from which the script was invoked).
- The program will then crawl each seed URL in succession and add any subsequently found URLs to a queue of URLs to visit.
- As each URL is visited, if it satisfies the given filtering parameters, it will be downloaded while maintaining the directory structure of the website.
- The value of URLs to visit will thus grow initially, round off when no new URLs are being discovered, and eventually shrink down to zero, at which point the program will move on to the next seed URL, or exit if there are no more URLs to process.

=== Usage ===

1. cd web-crawler-master
2. Edit config.py (Explanation below)
3. python run.py

=== Config.py Variables ===

mimetypes_list is an array of mimetypes that determines which files will be downloaded, provided they pass the regular expression filters.

file_extensions_list is an array of file extensions that determines which files will be downloaded, provided they pass the regular expression filters.

*Note: It will take less time to process each URL if one or the other of the above are used rather than both.

request_timeout is a float describing how long to wait in seconds for the server to issue a response for each URL.

request_delay is a float describing how long to wait in seconds before making the next request.

urls_to_crawl is an array of hashes containing the items url, follow_links_containing, and (optionally) regex_filters.

url is a url string in the style http://www.main.russia.org

follow_links_containing is a string that determines what links are followed.  For example, www.main.russia.org will follow all links containing www.main.russia.org and russia.org will follow all links containing russia.org.  www.main.russia.org is thus more restrictive and will take less time to process.

regex_filters is an optional array of Perl-style regular expression patterns.  Files matching any one of the patters will be downloaded.  "\d" means a single digit and "." means any character except the newline character.  Prefix regex stings with an "r" so that the "/" character is interpreted properly, as in: r"/2014/07\d\d/"  http://docs.python.org/2/howto/regex.html#regex-howto

=== An Example config.py ===

mimetypes_list = [ 'text/html' ]

file_extensions_list = [ '.asp', '.aspx' ]

request_timeout = 20

urls_to_crawl = [
    {
        "url": "http://madeinheights.com",
        "follow_links_containing": "madeinheights.com",
        "regex_filters": [ r"st.ry" ]
    },
    {
        "url": "http://www.china.com.cn",
        "follow_links_containing": "www.china.com.cn",
        "regex_filters": [ r"/2014-07/\d\d/" ]
    },
    {
        "url": "http://politics.people.com.cn",
        "follow_links_containing": "politics.people.com.cn",
        "regex_filters": [ r"/2014/07\d\d/" ]
    }    
]

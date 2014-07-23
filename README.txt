In config.py:

urls_to_crawl is an array of hashes containing the items url, follow_links_containing, and regex_filters.

url is a url string in the style http://www.main.russia.org or https://www.main.russia.org

follow_links_containing is a string that determines what links are followed.  For example, www.main.russia.org will follow all links containing www.main.russia.org and russia.org will follow all links containing russia.org.  www.main.russia.org is thus more restrictive.

regex_filters is an array of Perl-style regular expression patterns.  Files matching any one of the patters will be dowloaded.  http://docs.python.org/2/howto/regex.html#regex-howto

urls_to_crawl = [
    {
        "url": "http://www.main.russia.org",
        "follow_links_containing": "main.russia.org",
        "regex_filers": ["2014", "2013"]
    },
    {
        "url": "http://community.people.org",
        "follow_links_containing": "community.people.org",
        "regex_filters": ["2014", "2013"]
    }
]

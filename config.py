mimetypes_list = [ 'html' ]

binary_mimetypes_list = [ 'pdf', 'video', 'audio', 'image' ]

file_extensions_list = [ ]

request_delay = 0

urls_to_crawl = [
    {
		"url": "http://www.dalailama.com/webcasts/post/360-meeting-with-the-shia-and-sunni-communities-in-leh",
		"follow_links_containing": "dalailama.com",
		"ignore_query_strings": True,
    },    
    {
		"url": "http://www.cuyoo.com/article-22417-1.html",
		"follow_links_containing": "http://www.cuyoo.com/article-22417-1.html",
		"ignore_query_strings": True,
    },
]

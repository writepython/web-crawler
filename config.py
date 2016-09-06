mimetypes_list = [ ]

binary_mimetypes_list = [ ]

file_extensions_list = [ '.html' ]

request_delay = 0

urls_to_crawl = [
    {
		"url": "http://www.pbc.gov.cn/english/130721/index.html",
		"follow_links_containing": "english",
		"ignore_query_strings": True,
        "force_javascript_execution": True,
    },
    {
		"url": "http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html",
		"follow_links_containing": "goutongjiaoliu",
		"ignore_query_strings": True,
        "force_javascript_execution": True,        
    },
]

import requests, chardet

request_headers = { 'User-Agent': 'Mozilla/5.0' }
url = "http://www.cuyoo.com/article-22418-1.html"

head_response = requests.get(url, allow_redirects=True, headers=request_headers, timeout=20)
print head_response.headers
print head_response.headers.get('content-type')
print head_response.encoding
print head_response.url
print head_response.status_code
text = head_response.text

g = text.encode('gbk')
u = text.encode('utf-8')

print chardet.detect(g)
print chardet.detect(u)
## with open('requests_utf8.txt', 'w') as h:
##     h.write( head_response.text.encode('utf-8', 'replace') )


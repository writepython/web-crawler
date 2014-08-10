import requests

request_headers = { 'User-Agent': 'Mozilla/5.0' }
url = "http://www.cuyoo.com/article-22418-1.html"

head_response = requests.head(url, allow_redirects=True, headers=request_headers, timeout=20)
print head_response.headers
print head_response.encoding

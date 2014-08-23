import requests, chardet

request_headers = { 'User-Agent': 'Mozilla/5.0' }

url = "http://d138hkes00e90m.cloudfront.net/release_images/DarkEngine_02-1.png"
url = "http://www.rfc-editor.org/rfc/rfc6708.txt"
url = "http://www.rfc-editor.org/CurrQstats.txt"

response = requests.get(url, allow_redirects=True, headers=request_headers, timeout=20)
print response.headers
print response.headers.get('content-type')
encoding = response.encoding
print encoding
print type(encoding)
print "__%s__" % encoding
print response.url
print response.status_code
with open('a', 'w') as h:
    data = response.text
    encoding = 'utf-8'
    encoded_data = data.encode('utf-8')
    h.write( encoded_data )
## text = response.text
## print text
## g = text.encode('gbk')
## u = text.encode('utf-8')

## print chardet.detect(g)
## print chardet.detect(u)
## with open('requests_utf8.txt', 'w') as h:
##     h.write( response.text.encode('utf-8', 'replace') )


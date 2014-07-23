import re

tests = ["", " ", "2014", "/2014/07", "/2014/0711", "/2014/0711/", "/2014-07/11/", "a/2014/07", "a/2014/0711", "a/2014/0711/", "a/2014-07/11/"]

regex1 = re.compile(r"/2014/07../")
regex2 = re.compile(r"/2014-07/../")
regex3 = re.compile(r"/2014-07/\d\d/")

for test in tests:
    if regex1.search(test):
        print "regex1 found:%s" % test
    if regex2.search(test):
        print "regex2 found:%s" % test
    if regex3.search(test):
        print "regex3 found:%s" % test        

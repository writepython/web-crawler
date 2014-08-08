from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.cuyoo.com/article-22536-1.html")
try:
    print driver.execute_script("return window;")
except:
    print "caught exception"
#with open('selenium.txt', 'w') as f:
#    f.write( driver.page_source.encode('utf-8') )
#print driver.title
#print driver.page_source
driver.close()

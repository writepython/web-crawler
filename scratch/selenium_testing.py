from selenium import webdriver

urls = ["http://www.cuyoo.com/article-22418-1.html", "http://www.cuyoo.com/article-22536-1.html"]
driver = webdriver.Firefox()
for i, url in enumerate(urls):
        driver.get(url)
        print driver.current_url

#print "caught exception"
#with open('selenium.txt', 'w') as f:
#    f.write( driver.page_source.encode('utf-8') )
#print driver.title
#print driver.page_source
#print driver.execute_script("return window;")
driver.close()

from selenium import webdriver

urls = [
    "http://www.cuyoo.com/article-22418-1.html", "http://www.cuyoo.com/article-22536-1.html", "http://google.com/aksdahkgha",
    "htt://google.com/aksdahkgha"
    ]

driver = webdriver.Firefox()
driver.set_page_load_timeout(5)
driver.set_window_size(50, 50)
for i, url in enumerate(urls):
    try:
        driver.get(url)
        print driver.current_url
    except:
        print "error"

#with open('selenium.txt', 'w') as f:
#    f.write( driver.page_source.encode('utf-8') )
#print driver.title
#print driver.page_source
#print driver.execute_script("return window;")
driver.quit()

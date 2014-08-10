import os, datetime
from selenium import webdriver

start_time = datetime.datetime.now()

urls = [
    "http://www.cuyoo.com/article-22418-1.html", "http://www.cuyoo.com/article-22536-1.html", "http://google.com/aksdahkgha",
    "http://google.com/aksdahkgha"
    ]

phantomjs_path = os.path.join( os.getcwd(), "phantomjs" )
#driver = webdriver.Firefox()
driver = webdriver.PhantomJS(executable_path=phantomjs_path)
driver.set_page_load_timeout(40)
driver.set_window_size(50, 50)
for i, url in enumerate(urls):

        driver.get(url)
        print driver.current_url


#with open('selenium.txt', 'w') as f:
#    f.write( driver.page_source.encode('utf-8') )
#print driver.title
#print driver.page_source
#print driver.execute_script("return window;")
driver.quit()

end_time = datetime.datetime.now()

print "\nStart:  %s\nFinish: %s\n" % (start_time, end_time)

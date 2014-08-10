import os, sys, datetime, traceback, platform
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

start_time = datetime.datetime.now()

urls = [
    "http://www.cuyoo.com/article-22418-1.html", "http://www.cuyoo.com/article-22536-1.html", "http://google.com/aksdahkgha",
    "http://google.com/a"
    ]

try:
    user_os = platform.system()
    if user_os == "Darwin":
        phantomjs_filepath = "phantomjs/phantomjs_mac"
    elif user_os == "Linux":
        user_machine = platform.machine()
        if user_machine == "x86_64":
            phantomjs_filepath = "phantomjs/phantomjs_linux_64"        
    phantomjs_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), phantomjs_filepath )
    #phantomjs_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), "phantomjs_linux_64" )
    #print phantomjs_path
    #browser = webdriver.Chrome()
    browser = webdriver.PhantomJS(executable_path=phantomjs_path)
    #browser.set_window_size(200, 200)
    browser.set_page_load_timeout(60)
    #browser.set_script_timeout(0.1)

    for url in urls:

        browser.get(url)
        #body = browser.find_element_by_tag_name('body')

        #body = WebDriverWait(browser, 5).until( expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')) )
        
        print browser.current_url
        #print browser.page_source
    #print "error"

    #with open('selenium.txt', 'w') as f:
    #    f.write( browser.page_source.encode('utf-8') )
    #print browser.title
    
    #print browser.execute_script("return window;")
    end_time = datetime.datetime.now()

    print "\nStart:  %s\nFinish: %s\n" % (start_time, end_time)
except:
    try:
        traceback_info = '\n'.join(traceback.format_exception(*(sys.exc_info())))
    except:
        traceback_info = ''
    print "*** ERROR  ***\nTraceback: %s\n" % traceback_info

finally:
    browser.quit()



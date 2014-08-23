#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt
import codecs

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:" )
    except getopt.GetoptError:
        print 'open_unicode_file.py -i <inputfile>'
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-i":
                inputfile = arg
        ## f = open(inputfile)
        ## for line in f:
        ##     try:
        ##         line.decode('gbk')
        ##     except:
        ##         print line
        f = codecs.open(inputfile, 'r', 'utf-8')
        with codecs.open("test_output", "w", "utf-8") as temp:
            temp.write(f.read())

    
if __name__ == "__main__":
    main(sys.argv[1:])    

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt
import codecs

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:o:" )
    except getopt.GetoptError:
        print 'redirect_to_file.py -i <inputfile>'
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-i":
                inputfile = arg
        f = open(inputfile)
        for line in f:
            print line
    
if __name__ == "__main__":
    main(sys.argv[1:])    

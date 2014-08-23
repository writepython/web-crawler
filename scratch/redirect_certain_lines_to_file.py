#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:o:" )
    except getopt.GetoptError:
        print 'redirect_certain_lines_to_file.py -i <inputfile>'
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-i":
                inputfile = arg
        f = open(inputfile)
        for line in f:
            if """法俄军售僵局暴露西方内部分歧""" in line:
                print line
    
if __name__ == "__main__":
    main(sys.argv[1:])    

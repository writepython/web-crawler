import sys, getopt

usage_message = 'Usage: download.py -i <input_file> -o <output_dir>'

def main(argv):
    input_file = None
    try:
        opts, args = getopt.getopt(argv, "i:o:" )
    except getopt.GetoptError:
        print usage_message
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-i":
                input_file = arg
            if opt == "-o":
                output_dir = arg
    if not input_file or not output_dir:
        print usage_message
    else:
        print input_file
        print output_dir        
    #download_files(input_file, output_dir)
    
if __name__ == "__main__":
    main(sys.argv[1:])    

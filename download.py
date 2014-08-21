import os, sys, getopt
from functions import mkdir_p, get_response_data, write_file

usage_message = 'Usage: download.py -i <input_file> -o <output_dir>'

def download_files(urls, output_dir):

    
    filepath = os.path.join

        
def main(argv):
    input_file = None
    try:
        opts, args = getopt.getopt(argv, "i:o:" )
    except getopt.GetoptError:
        print usage_message
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            input_file = arg
        if opt == "-o":
            output_dir = arg
    if not input_file or not output_dir:
        print usage_message
        sys.exit(2)
    if os.path.isdir(output_dir):
        print "Found directory %s" % output_dir
    else:
        mkdir_p(output_dir)
        print "Created directory %s" % output_dir
    with open(input_file) as f:
        urls = f.readlines()
    print "Found %d URLs" % len(urls)
    for url in urls:
        url = url.strip()
        final_url, data, encoding = get_response_data(url)
        filepath = get_filepath(final_url, encoding, output_dir)
        encoded_data = get_encoded_data(data, encoding)
        write_file(encoded_data, filepath)
    
if __name__ == "__main__":
    main(sys.argv[1:])    

from __future__ import print_function
from core.colors import end, green, red, white, bad, info

import pyfiglet

# my project banner 
banner = pyfiglet.figlet_format("WEB-WHISPER")
colored_banner = f"{green}{banner}{end}"
print(colored_banner)
line = f"_" * 73
c_line = f"{green}{line}{end}"
print(c_line)

try:
    import concurrent.futures
    from urllib.parse import urlparse
    try:
        import fuzzywuzzy
    except ImportError:
        import os
        print ('%s fuzzywuzzy is not installed, installing now.' % info)
        install_code = os.system('pip3 install fuzzywuzzy')
        if(install_code != 0):
            print('%s fuzzywuzzy installation has failed.' % bad)
            quit()
        print ('%s fuzzywuzzy has been installed, restart XSStrike.' % info)
        quit()
except ImportError: #error mostlikely form python verion
    print('%s Web-Whisper isn\'t compatible with python2.\n Use python > 3.4 to run XSStrike.' % bad)
    quit()

# Let's import whatever we need from standard lib
import sys
import json
import argparse


import core.config 
import core.log

# processing command line arguments, where dest var name will be mapped to local vars with the same name 
parser = argparse.ArgumentParser() # the function parse.ArgumentParser() by default is to display the name of the file regardless of where the program file is being called/run from e.g. web-whisper.py
parser.add_argument('-u', '--url', help='recieves url input', dest='target')
parser.add_argument('-e', '--encode', help='encode payloads', dest='encode')
parser.add_argument('--fuzzer', help='fuzzer', dest='fuzz', action='store_true')
parser.add_argument('--proxy', help='use prox(y|ies)',dest='proxy', action='store_true')
parser.add_argument('--crawl', help='crawl',dest='recursive', action='store_true')
parser.add_argument('--json', help='treat post data as json',dest='jsonData', action='store_true')
parser.add_argument('-f', '--file', help='load payloads from a file', dest='args_file')

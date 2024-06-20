import sys
import os
import platform

operating_sytem = sys.platform #To identify the OS
colors = True #the output should be colored
OS_Version = platform.platform() #Get the current OS version

if operating_sytem.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False # Colors wouldn't be displayed on mac and windows 
if OS_Version.startswith("windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('') #enables ANSI colors
if not colors: #if colors is False
    end = red = white = green = yellow = run = bad = good = info = que = ''
else:
    white = '\033[97m'
    green = '\033[92m'
    red = '\033[91m'
    yellow = '\033[93m'
    end = '\033[0m'
    back = '\033[7;91m'
    info = '\033[93m[!]\033[0m'
    que = '\033[94m[?]\033[0m'
    bad = '\033[91m[-]\033[0m'
    good = '\033[92m[+]\033[0m'
    run = '\033[97m[~]\033[0m'

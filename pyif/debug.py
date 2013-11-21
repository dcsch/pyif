
#import sys
from . import glk

def log(string):
    #sys.stdout.write("[LOG] %s\n" % string)
    glk.put_string("[LOG] %s\n" % string)
    #pass

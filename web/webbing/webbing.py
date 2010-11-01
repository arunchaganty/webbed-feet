#!/usr/bin/env python2
# Scheduler for matches 

#import settings
import urllib2
import sys
import time

import gbl

from TaskManager import TaskManager

def server_alive():
   # Periodically ping the webbed-feet server to check if it is alive. 
   url = gbl.PING_URL

   try :
       f = urllib2.urlopen(url)
       if f.code != 200:
           raise Exception("Can not ping server")
       else:
           print "Server still alive..."
   except StandardError, e:
       print "Server error: ", str(e)
       return False

   return True

def main():
    # Add to a work queue. 

    manager = TaskManager()
    manager.loop_condition = server_alive

    manager.run()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "start":
        print "Webbing is the scheduler daemon for webbed-feet"
        print "Usage: %s start"%(sys.argv[0])
        sys.exit(1)
    else:
        main()


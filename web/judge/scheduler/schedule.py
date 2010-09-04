# Scheduler for matches 

import urllib
import sys
import time

import gbl

from TaskManager import TaskManager
import Scheduler

_opener = urllib.URLopener(proxies={})

def server_alive():
   # Periodically ping the webbed-feet server to check if it is alive. 
   url = gbl.PING_URL

   try :
       f = _opener.open(url)
       if f.getcode() != 200:
           raise Exception("Can not ping server")
       else:
           print "Server still alive..."
   except StandardError as e:
       print "Server error: ", e.msg
       return False

   return True

def main():
    # Add to a work queue. 
    manager = TaskManager(Scheduler.TestScheduler([1,2,3,4,5,6,7,8,9]))
    manager.loopCondition = server_alive

    manager.run()

if __name__ == "__main__":
    main()


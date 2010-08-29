# Scheduler for matches 

import settings
import urllib
import sys
import time

import gbl

from TaskManager import TaskManager
import Scheduler

_opener = urllib.URLopener(proxies={})

def server_alive():
    # Periodically ping the webbed-feet server to check if it is alive. 
   url = urllib.basejoin(settings.SITE_URL, gbl.PING_URL)
   print url

   try :
       f = _opener.open(url)
       print f.getcode()
       if f.getcode() != 200:
           raise Exception("Can not ping server")
   except StandardError as e:
       print e.msg
       return False

   return True

def main():
    # Add to a work queue. 
    manager = TaskManager(Scheduler.TestScheduler())
    manager.loopCondition = server_alive

    manager.run()

if __name__ == "__main__":
    main()


#!/usr/bin/env python
# Scheduler for matches 

#import settings
import urllib2
import sys
import time

import gbl

from TaskManager import TaskManager

class PingingTaskManager(TaskManager):
    def loop_condition(self):
        """Should the manager stop, restart?"""
        # Periodically ping the webbed-feet server to check if it is alive. 
        url = gbl.PING_URL

        stop, restart = False, False

        try :
            f = urllib2.urlopen(url)
            if f.code != 200:
                raise Exception("Can not ping server")
            else:
                code = f.read()
                print "Server returned", code
                if code == "1":
                    print "Restarting server"
                    restart = True
        except StandardError, e:
            print "Server error: ", str(e)
            stop = True

        return stop, restart

def main():
    # Add to a work queue. 

    manager = PingingTaskManager()
    manager.run()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "start":
        print "Webbing is the scheduler daemon for webbed-feet"
        print "Usage: %s start"%(sys.argv[0])
        sys.exit(1)
    else:
        main()


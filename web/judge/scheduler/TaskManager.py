# Task Manager

import subprocess
import os
import time

import gbl

class TaskManager:
    period = -1 
    parallelism=1
    threads = []
    scheduler = []
    tasks = [].__iter__()

    def __init__(self, scheduler, period = gbl.MAINLOOP_PERIOD, parallelism=1):
        self.period = period
        self.parallelism = parallelism
        self.scheduler = scheduler
        self.tasks = (task for task in scheduler)
        
    def loopCondition(self):
        return True

    def loop(self):
        # Terminate dead threads
        live = []
        for thread in self.threads:
            if thread.isAlive():
                live.append(thread)
            else:
                thread.join()
        self.threads = live

        # Launch threads if possible
        if len(self.threads) < self.parallelism:
            try:
                task = self.tasks.next()
                self.threads.append(task)
                task.start()
            except StopIteration:
                pass
        return

    def run(self):
        while self.loopCondition():
            self.loop()
            time.sleep(self.period)


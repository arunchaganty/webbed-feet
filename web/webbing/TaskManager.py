# Task Manager

import os
import time
import random
import subprocess

import gbl

class TaskManager:
    period = -1 
    parallelism=1

    threads = []
    sources = []
    tasks = []

    def __init__(self, db, period = gbl.MAINLOOP_PERIOD, parallelism=1):
        self.db = db
        self.period = period
        self.parallelism = parallelism

    def addGenerator(self, generator):
        self.sources.append(generator.__iter__())

    def addTask(self, task):
        """Add an immediate task"""
        self.tasks.append(task)
        
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
                # First process immediate tasks
                if len(self.tasks) > 0:
                    task = self.tasks.pop(0)
                    print 'immediate task'
                else:
                    # Else generate something from one of the generators
                    source = random.choice(self.sources)
                    task = source.next()
                    print 'generated task'
                    print task
                self.threads.append(task)
                task.taskManager = self
                task.start()
            except StopIteration:
                pass
        return

    def run(self):
        while True:
            if self.loopCondition():
                self.loop()
            time.sleep(self.period)   #changed


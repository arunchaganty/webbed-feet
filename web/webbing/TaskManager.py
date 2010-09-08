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
    source = [].__iter__()
    tasks = []


    def __init__(self, scheduler, db, period = gbl.MAINLOOP_PERIOD, parallelism=1):
        self.period = period
        self.parallelism = parallelism
        self.scheduler = scheduler
        self.db = db
        self.source = scheduler.__iter__()

    def addTask(self, task):
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
                if len(self.tasks) > 0:
                    task = self.tasks.pop(0)
                else:
                    task = self.source.next()
                self.threads.append(task)
                task.taskManager = self
                task.start()
            except StopIteration:
                pass
        return

    def run(self):
        while self.loopCondition():
            self.loop()
            time.sleep(self.period)


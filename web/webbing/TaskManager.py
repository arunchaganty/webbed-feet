# Task Manager

import os
import time
import random
import subprocess

from web.judge import models

import gbl

class TaskManager:
    period = -1 
    parallelism=1

    threads = []
    sources = []
    tasks = []

    def __init__(self, period = gbl.MAINLOOP_PERIOD, parallelism=1):
        self.period = period
        self.parallelism = parallelism

        self.add_generators()

    def add_generators(self):
        """Add generators for all the games"""
        for game in models.Game.objects.all():
            if game.active:
                gen = game.scheduler.schedule( game )
                self.add_generator( gen )

    def add_generator(self, generator):
        self.sources.append(generator.__iter__())

    def add_task(self, task):
        """Add an immediate task"""
        self.tasks.append(task)
        
    def loop_condition(self):
        return True

    def loop(self):
        # Terminate dead threads
        live = []
        for thread in self.threads:
            if thread.is_alive():
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
                    print 'generated task', task
                self.threads.append(task)
                task.taskManager = self
                task.start()
            except StopIteration:
                pass
        return

    def run(self):
        while True:
            if self.loop_condition():
                self.loop()
            time.sleep(self.period)   #changed


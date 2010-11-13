# Task Manager

import os
import time
import random
import subprocess

from web.judge import models

import gbl

class TaskManager:
    period = -1 
    parallelism=gbl.PARALLEL_THREADS

    threads = []
    sources = []
    tasks = []

    def __init__(self, period = gbl.MAINLOOP_PERIOD, parallelism=gbl.PARALLEL_THREADS):
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
        return False, False

    def loop(self):
        # Terminate dead threads
        live = []
        for thread in self.threads:
            if thread.is_alive():
                live.append(thread)
            else:
                thread.join()
        self.threads = live

        print len(self.threads), self.parallelism
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
            stop, restart = self.loop_condition()
            if stop:
                break

            if restart:
                for thread in self.threads:
                    thread.join()
                self.sources = []
                self.tasks = []
                self.add_generators()

            self.loop()
            time.sleep(self.period)   #changed


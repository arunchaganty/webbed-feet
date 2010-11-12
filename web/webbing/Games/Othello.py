# Abstraction of a game and all it's aspects

import Game

import os
import time
import signal
import shutil
import zipfile
import hashlib
import subprocess
from datetime import datetime

import tempfile 
from django.core.files.base import File

from web.webbing import errors
from web.webbing import gbl

def obliterate(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

class Othello(Game.Game):
    GAME_CWD = os.path.join(gbl.ROOT_DIR, "runnest/othello/")
    EXECUTABLE = os.path.join(gbl.ROOT_DIR, "runnest/othello/bin/Desdemona")
    POST_RUN_LOG = "game.log"

    BUILDNEST = os.path.join(gbl.ROOT_DIR, "buildnest/othello/bots/SubmissionBot")
    BOT_OUTPUT = "bot.so"

    @classmethod 
    def submissionHook(cls, uploaded_file):
        """Expect a tarball containing a Makefile
        Compile the submission"""

        old_mask = os.umask(0)

        try:
            f = zipfile.ZipFile(uploaded_file)
        except zipfile.BadZipfile:
            raise errors.BuildError("Invalid zip file")

        # Copy files to buildnest

        # Handle older versions of zipfile that do not contain 'extractall'
        if hasattr(f, "extractall"):
            f.extractall(path=cls.BUILDNEST)
        else:
            for name in f.namelist():
                path = os.path.join(cls.BUILDNEST, name)
                f_ = open(path, "wb")
                f_.write( f.read( name ) )
                f_.close()

        # make in the buildnest
        p = subprocess.Popen(["make"], stderr=subprocess.PIPE, cwd=cls.BUILDNEST)
        output = p.communicate()[1]
        ret = p.wait()

        # Report errors
        if ret != 0:
            os.umask(old_mask)
            raise errors.BuildError(output)

        output = os.path.join(cls.BUILDNEST, cls.BOT_OUTPUT)

        if not os.path.exists(output):
            raise errors.BuildError("No %s found after build"%(cls.BOT_OUTPUT))

        # Save the output    
        botSo = open(output, "rb")

        # TODO: Check compiled .so?
        os.umask(old_mask)

        def read_in_chunks(file_object, chunk_size=1024):
            """Lazy function (generator) to read a file piece by piece.
            Default chunk size: 1k."""
            while True:
               data = file_object.read(chunk_size)
               if not data:
                   break
               yield data

        uploaded_file = File(tempfile.NamedTemporaryFile())
        for piece in read_in_chunks(botSo):
            uploaded_file.write(piece)
        uploaded_file.size = os.stat(os.path.join(cls.BUILDNEST, cls.BOT_OUTPUT)).st_size
        botSo.close()

        # Clean up 
        obliterate(cls.BUILDNEST)

        return uploaded_file

    @classmethod
    def runHook(cls, player1, player2):
        # Get arguments for the game
        so1 = os.path.join(gbl.MEDIA_DIR, str(player1.data))
        so2 = os.path.join(gbl.MEDIA_DIR, str(player2.data))
        args = [cls.EXECUTABLE, so1, so2]

        # Run the game
        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=cls.GAME_CWD)

        # Time the execution
        start = time.time()
        while (time.time() - start) < gbl.TIMEOUT:
            # Keep polling
            ret = p.poll()
            if ret != None: break
            time.sleep(1)
        else:
            os.kill( p.pid, signal.SIGTERM )
            ret = p.poll()
            if not ret:
                os.kill( p.pid, signal.SIGKILL )
                ret = p.poll()
                
        output = p.communicate()[0]

        # The hook takes care of output codes
        output = output.strip()
        try:
            score1, score2, status = cls.scoreHook(output)
        except:
            score1, score2, status = 0, 0, "ERR"

        log_path = ""
        print "Output in hook - <"+output+">"
        try:
            # Also, save the game log file.
            if cls.POST_RUN_LOG:
                log_in = os.path.join(cls.GAME_CWD, cls.POST_RUN_LOG)

                sha1sum = hashlib.sha1(open(log_in).read()).hexdigest()

                log_path = os.path.join("logs",sha1sum)
                log_out = os.path.join(gbl.MEDIA_DIR, log_path)
                # Copy the log file to the log location
                shutil.copy(log_in, log_out)
        except StandardError, e:
            print e
            log_path = ""

        run = (datetime.now(), player1, player2, score1, score2, status, log_path)

        return run

    @classmethod
    def scoreHook(cls, output):
        lines = output.strip().splitlines()
        if len(lines) == 1:
            try:
                status = "OK"
                score = int(output)
                print score
                # 
                if score < 0:
                    score = -score
                    score1 = 0
                    score2 = score + 50
                elif score == 0:
                    score1 = 25
                    score2 = 25 
                elif score > 0:
                    score1 = score + 50
                    score2 = 0
            except:
                # Else expect an error code
                if output in ["DQ1", "TO1"]:
                    status = output
                    score1 = 0
                    score2 = 50 + 64
                elif output in ["DQ2", "TO2"]:
                    status = output
                    score1 = 50 + 64
                    score2 = 0
                else: # output in ["CR1", "CR2", "ERR"]:
                    if output not in ["CR1", "CR2", "ERR"]:
                        output = "ERR"
                    status = output
                    score1 = 0
                    score2 = 0
        else:
            output = "ERR"
            status = output
            score1 = 0
            score2 = 0

        return score1, score2, status


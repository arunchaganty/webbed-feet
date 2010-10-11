# Abstraction of a game and all it's aspects

import os
import shutil
import hashlib
import subprocess
from datetime import datetime

import Bot
import errors
import gbl

import zipfile

class Game:
    @classmethod
    def submissionHook(cls, uploaded_file):
        return uploaded_file

    @classmethod
    def runHook(cls, player1, player2):
        return 0

    @classmethod
    def scoreHook(cls, output):
        if score.isdigit():
            score = int(score)
            # Make any modifications
            return score
        else:
            # Handle various error codes
            return 0

class SnakeGame(Game):
    GAME_CWD = "/home/codingevents/automania/runnests/snake/"
    EXECUTABLE = "/home/codingevents/automania/runnests/snake/bin/snake"
    POST_RUN_LOG = "game_out.txt"

    BUILDNEST = "/home/codingevents/automania/buildnests/snake/bots/"
    BOT_INPUT = "bot.cpp"
    BOT_HEADER = "bot.h"
    BOT_OUTPUT = "bot.so"

    @classmethod 
    def submissionHook(cls, uploaded_file):
        """Expect a tarball containing bot.cpp (and bot.h).
        Compile the submission"""

        old_mask = os.umask(0)
        # Read as a zipfile
        # Read the uploaded file
        try:
            f = zipfile.ZipFile(uploaded_file)
            if cls.BOT_INPUT not in f.namelist():
                raise errors.BuildError("Zip file does not contain 'bot.cpp'")
        except zipfile.BadZipfile:
            raise errors.BuildError("Invalid zip file")

        # Copy files to buildnest

        # Handle older versions of zipfile that do not contain 'extract'
        if hasattr(f, "extract"):
            f.extract(cls.BOT_INPUT, path=cls.BUILDNEST)
            if cls.BOT_HEADER in f.namelist():
                f.extract(cls.BOT_HEADER, path=cls.BUILDNEST)
        else:
            f_ = open(os.path.join(cls.BUILDNEST, cls.BOT_INPUT), "w")
            f_.write(f.read(cls.BOT_INPUT))
            if cls.BOT_HEADER in f.namelist():
                f_ = open(os.path.join(cls.BUILDNEST, cls.BOT_HEADER), "wb")
                f_.write(f.read(cls.BOT_HEADER))
        
        # make in the buildnest
        p = subprocess.Popen(["make"], stderr=subprocess.PIPE, cwd=cls.BUILDNEST)
        output = p.communicate()[1]
        ret = p.wait()
        
        # Report errors
        if ret != 0:
            os.umask(old_mask)
            raise errors.BuildError(output)

        # Save the output    
        botSo = open(os.path.join(cls.BUILDNEST, cls.BOT_OUTPUT), "rb")

        # Clean up 
        for name in [cls.BOT_INPUT, cls.BOT_HEADER]:
            path = os.path.join(cls.BUILDNEST, name)
            if os.path.exists(path):
                os.remove(path)

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

        uploaded_file.truncate(0)
        for piece in read_in_chunks(botSo):
            uploaded_file.write(piece)
        uploaded_file.size = os.stat(os.path.join(cls.BUILDNEST, cls.BOT_OUTPUT)).st_size
        uploaded_file.close()
        botSo.close()
        
        return uploaded_file

    @classmethod
    def runHook(cls, player1, player2):
        # Get arguments for the game
        so1 = os.path.join(gbl.BASE_LOCATION, player1.data)
        so2 = os.path.join(gbl.BASE_LOCATION, player2.data)
        args = [cls.EXECUTABLE, so1, so2]

        # Run the game
        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=cls.GAME_CWD)
        output = p.communicate()[0]
        ret = p.wait()

        # The hook takes care of output codes
        output = output.strip()
        score1, score2, status = cls.scoreHook(output)

        log_path = ""
        try:
            # Also, save the game log file.
            if cls.POST_RUN_LOG:
                log_in = os.path.join(cls.GAME_CWD, cls.POST_RUN_LOG)

                sha1sum = hashlib.sha1(open(log_in, 'rb').read()).hexdigest()

                log_path = os.path.join("logs",sha1sum)
                log_out = os.path.join(gbl.BASE_LOCATION, log_path)
                # Copy the log file to the log location
                shutil.copy(log_in, log_out)
        except StandardError, e:
            print e
            log_path = ""

        run = Bot.Run(datetime.now(), player1, player2, score1, score2, status, log_path)

        return run

    @classmethod
    def scoreHook(cls, output):
        print "Output in hook - <"+output+">"
        try:
            status = "OK"
            score = int(output)
            print score
            # 
            if score < 0:
                score1 = score
                score2 = -score
            elif score == 0:
                score1 = 0
                score2 = 0
            elif score > 0:
                score1 = score
                score2 = -score
        except:
            # Else expect an error code
            if output in ["DQ1", "TO1"]:
                status = output
                score1 = -50
                score2 = 50
            elif output in ["DQ2", "TO2"]:
                status = output
                score1 = 50
                score2 = -50
            else: # output in ["CR1", "CR2", "ERR"]:
                if output not in ["CR1", "CR2", "ERR"]:
                    output = "ERR"
                status = output
                score1 = 0
                score2 = 0

        return score1, score2, status


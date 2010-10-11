# Abstraction of a game and all it's aspects

import Game

import os
import shutil
import zipfile
import hashlib
import subprocess
from datetime import datetime

from web.webbing import errors
from web.webbing import Bot

class Othello(Game.Game):
    GAME_CWD = "/home/teju/Projects/Desdemona/"
    EXECUTABLE = "/home/teju/Projects/Desdemona/bin/Desdemona"
    POST_RUN_LOG = "game.log"

    BUILDNEST = "/home/teju/Projects/webbed-feet/buildnest/othello/bots/SubmissionBot/"
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
                f_.write( f.read( path ) )
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

        uploaded_file.truncate(0)
        for piece in read_in_chunks(botSo):
            uploaded_file.write(piece)
        uploaded_file.size = os.stat(os.path.join(cls.BUILDNEST, cls.BOT_OUTPUT)).st_size
        uploaded_file.close()
        botSo.close()

        # Clean up 
        shutil.rmtree(cls.BUILDNEST)


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
        score = cls.scoreHook(output)
        if output.isdigit():
            status = "OK"
        # Else expect an error code
        elif output in ["DQ1", "DQ2", "TO1", "TO2", "CR1", "CR2", "ERR"]:
            status = output
        else:
            status = "ERR"

        log_path = ""
        print "Output in hook - <"+output+">"
        try:
            # Also, save the game log file.
            if cls.POST_RUN_LOG:
                log_in = os.path.join(cls.GAME_CWD, cls.POST_RUN_LOG)

                sha1sum = hashlib.sha1(open(log_in).read()).hexdigest()

                log_path = os.path.join("logs",sha1sum)
                log_out = os.path.join(gbl.BASE_LOCATION, log_path)
                # Copy the log file to the log location
                shutil.copy(log_in, log_out)
        except StandardError as e:
            print e
            log_path = ""

        run = Bot.Run(datetime.now(), player1, player2, score, status, log_path)

        return run

    @classmethod
    def scoreHook(cls, output):
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

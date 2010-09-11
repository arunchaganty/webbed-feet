# Abstraction of a game and all it's aspects

import os
import shutil
import hashlib
import subprocess
from datetime import datetime

import Bot
import gbl

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
    GAME_CWD = "/home/teju/Projects/automania/prob1/"
    EXECUTABLE = "/home/teju/Projects/automania/prob1/bin/snake"
    POST_RUN_LOG = "game_out.txt"

    BUILDNEST = "/home/teju/Projects/automania/buildnest/bots/"
    BOT_INPUT = "bot.cpp"
    BOT_OUTPUT = "bot.so"

    @classmethod 
    def submissionHook(cls, uploaded_file):
        """Compile the submission"""
        # Read the uploaded file
        uploaded_file.seek(0)

        # Copy to the buildnest
        botFile = open(os.path.join(cls.BUILDNEST, cls.BOT_INPUT), "w")
        for chunk in uploaded_file.chunks():
            botFile.write(chunk)
        botFile.close()

        # make in the buildnest
        p = subprocess.Popen(["make"], stderr=subprocess.PIPE, cwd=cls.BUILDNEST)
        output = p.communicate()[1]
        ret = p.wait()
        
        # Report errors
        if ret != 0:
            raise errors.BuildError(output)

        # Save the output    
        botSo = open(os.path.join(cls.BUILDNEST, cls.BOT_OUTPUT), "r")
        data = botSo.read()

        # TODO: Check compiled .so?

        uploaded_file.truncate(0)
        uploaded_file.write(data)
        uploaded_file.close()
        
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
        if output.isdigit():
            score = int(output)
            # Add a constant offset of 50
            if score < 0:
                score -= 50
            elif score > 0:
                score += 50
            return score
        else:
            # Handle various error codes
            return 0

class OthelloGame(Game):
    GAME_CWD = "/home/teju/Projects/Desdemona/"
    EXECUTABLE = "/home/teju/Projects/Desdemona/bin/Desdemona"
    POST_RUN_LOG = "game.log"

    #BUILDNEST = "/home/teju/Projects/automania/buildnest/bots/"
    #BOT_INPUT = "bot.cpp"
    #BOT_OUTPUT = "bot.so"

    @classmethod 
    def submissionHook(cls, uploaded_file):
        """Save the uploaded file the submission"""
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
        if output.isdigit():
            score = int(output)
            # Add a constant offset of 50
            if score < 0:
                score -= 50
            elif score > 0:
                score += 50
            return score
        else:
            # Handle various error codes
            return 0

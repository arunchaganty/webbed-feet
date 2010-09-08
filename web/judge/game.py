# Contains the parameter settings for handling submissions on Webbed-Feet

import os
import urllib
import subprocess

from web.webbing import errors

# Game Properties
BASE_LOCATION="/home/teju/Projects/webbed-feet/web/media/"

BUILDNEST = "/home/teju/Projects/automania/buildnest/bots/"
BOT_INPUT = "bot.cpp"
BOT_OUTPUT = "bot.so"

def compileSubmission(uploaded_file):
    """Compile the submission"""
    
    # Read the uploaded file
    uploaded_file.seek(0)
    data = uploaded_file.read()

    # Copy to the buildnest
    botFile = open(os.path.join(BUILDNEST, BOT_INPUT), "w")
    botFile.write(data)
    botFile.close()

    # make in the buildnest
    p = subprocess.Popen(["make"], stderr=subprocess.PIPE, cwd=BUILDNEST)
    output = p.communicate()[1]
    ret = p.wait()
    
    # Report errors
    if ret != 0:
        raise errors.BuildError(output)

    # Save the output    
    botSo = open(os.path.join(BUILDNEST, BOT_OUTPUT), "r")
    data = botSo.read()

    # TODO: Check compiled .so?

    uploaded_file.truncate(0)
    uploaded_file.write(data)
    uploaded_file.close()
    
    return uploaded_file

BOT_SUBMISSION_HOOK=compileSubmission


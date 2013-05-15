#!/usr/bin/env python3
#
# Automatically posts recurring threads to reddit
# Author: /u/MasterMic


# Imports
import json
import praw


# Global varibales
submissions = []


# A submission
class Submission(object):
    def __init__(self, subreddit, username, password, title, text):
        self.subreddit = subreddit
        self.username = username
        self.password = password
        self.title = title
        self.text = text

    def submit(self):
        r = praw.Reddit(user_agent="reddit-poster")
        r.login(self.username, self.password)
        r.submit(self.subreddit, self.title, text=self.text)
        print("[ INFO ] Submitted submission titled \"" + self.title + "\"")


# This method is used when rposter.py is invoked from the command line
def main():
    # Load the config file
    data = json.load(open("config.json"))
    print("[ INFO ] Submission data loaded from config.json")

    # Initialize the submissions
    global submissions
    for s in data:
        a_submission = Submission(s["subreddit"], s["username"], s["password"],
                                  s["title"], s["text"])
        submissions.append(a_submission)
        print("[ INFO ] Parsed submission titled \"" + s["title"] + "\"")


# Call main() when rposter.py is invoked from the command line
if __name__ == "__main__":
    main()

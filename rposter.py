#!/usr/bin/env python
#
# Automatically posts recurring threads to reddit
# Author: /u/MasterMic


# Imports
import json
import praw
import time

# Constants
RETRY_WAIT_TIME = 10  # Number of seconds to wait before retrying to submit an submission
WEEKDAYS = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
            5: "Friday", 6: "Saturday"}

# Global varibales
submissions = []


# A submission
class Submission(object):
    def __init__(self, subreddit, username, password, title, text, time):
        self.subreddit = subreddit
        self.username = username
        self.password = password
        self.title = title
        self.text = text
        self.time = time

    def submit(self):
        try:
            r = praw.Reddit(user_agent="reddit-poster")
            r.login(self.username, self.password)
            r.submit(self.subreddit, self.title, text=self.text
                     + "\n\n\n===\nPosted by reddit-poster")
            print("[ INFO ] Submitted submission titled \"" + self.title + "\"")
        except praw.errors.APIException as e:
            print("[ ERROR ] Submission of submission titled \"" + self.title
                  + "\" failed, trying again in " + str(RETRY_WAIT_TIME) + " seconds:")
            print(str(e))
            time.sleep(RETRY_WAIT_TIME)
            self.submit()


class Time(object):
    def __init__(self, day, hour, minute):
        # Ensure the time format is correct
        if day < 0 or day > 6:
            print("[ ERROR ] 'day' must be an integer ranging from 0 to 6")
            exit(1)
        if (hour < 0 or hour > 23):
            print("[ ERROR ] 'hour' must be an integer ranging from 0 to 23")
            exit(1)
        if (minute < 0 or minute > 59):
            print("[ ERROR ] 'minute' must be an integer ranging from 0 to 59")
            exit(1)

        self.day = day
        self.hour = hour
        self.minute = minute

    def to_string(self):
        return WEEKDAYS[self.day] + " at " + str(self.hour) + ":" + str(self.minute)


# This method is used when rposter.py is invoked from the command line
def main():
    # Load the config file
    data = json.load(open("config.json"))
    print("[ INFO ] Submission data loaded from config.json")

    # Initialize the submissions
    global submissions
    for s in data:
        try:
            a_time = Time(s["time"]["day"], s["time"]["hour"], s["time"]["minute"])
            a_submission = Submission(s["subreddit"], s["username"], s["password"],
                                      s["title"], s["text"], a_time)
            submissions.append(a_submission)
            print("[ INFO ] Parsed submission titled \"" + s["title"] + "\" to be run "
                  "every " + a_time.to_string())
        except KeyError as e:
            print("[ ERROR ] The key " + str(e) + " could not be found for a submission, "
                  + "check your config.json file")
            exit(1)

    # Queue the submissions to be submitted at the appropriate time
    # We assume all submissions prior to this time have been submitted


# Call main() when rposter.py is invoked from the command line
if __name__ == "__main__":
    main()

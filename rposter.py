#!/usr/bin/env python
#
# Automatically posts recurring threads to reddit
# Author: /u/MasterMic


# Imports
import json
import praw
import time


# Constants
CHECK_INTERVAL = 10  # Number of seconds to wait between checking for submissions to post
RETRY_WAIT_TIME = 10  # Number of seconds to wait before retrying to submit an submission
WEEKDAYS = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday",
            5: "Saturday", 6: "Sunday"}


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

    def in_interval(self, lower, upper):
        lower_minutes = get_minutes(lower.tm_wday, lower.tm_hour, lower.tm_min)
        upper_minutes = get_minutes(upper.tm_wday, upper.tm_hour, upper.tm_min)
        sub_minutes = get_minutes(self.time.day, self.time.hour, self.time.minute)

        if lower_minutes <= upper_minutes:
            return sub_minutes > lower_minutes and sub_minutes <= upper_minutes
        else:
            return sub_minutes > lower_minutes or sub_minutes <= upper_minutes

    def to_string(self):
        return "\"" + self.title + "\" to be run every " + self.time.to_string()


# A time object
class Time(object):
    def __init__(self, day, hour, minute):
        # Ensure the time format is correct
        if day < 0 or day > 6:
            print("[ ERROR ] 'day' must be an integer ranging from 0 to 6, "
                  + "check your config.json file")
            exit(1)
        if (hour < 0 or hour > 23):
            print("[ ERROR ] 'hour' must be an integer ranging from 0 to 23, "
                  + "check your config.json file")
            exit(1)
        if (minute < 0 or minute > 59):
            print("[ ERROR ] 'minute' must be an integer ranging from 0 to 59, "
                  + "check your config.json file")
            exit(1)

        self.day = day
        self.hour = hour
        self.minute = minute

    def to_string(self):
        return WEEKDAYS[self.day] + " at " + str(self.hour) + ":" + str(self.minute)


def get_minutes(day, hour, minute):
    return (day * 1440) + (hour * 60) + minute


# This method is used when rposter.py is invoked from the command line
def main():
    # Load the config file
    data = json.load(open("config.json"))
    print("[ INFO ] Submission data loaded from config.json")

    # Initialize the submissions
    submissions = []
    for s in data:
        try:
            a_time = Time(s["time"]["day"], s["time"]["hour"], s["time"]["minute"])
            a_submission = Submission(s["subreddit"], s["username"], s["password"],
                                      s["title"], s["text"], a_time)
            submissions.append(a_submission)
            print("[ INFO ] Parsed submission titled " + a_submission.to_string())
        except KeyError as e:
            print("[ ERROR ] The key " + str(e) + " could not be found for a submission, "
                  + "check your config.json file")
            exit(1)

    # Queue the submissions to be submitted at the appropriate time
    # We assume all submissions prior to this time have been submitted
    # We also assume that all time intervals last less than one week
    prev_time = time.localtime()
    while True:
        curr_time = time.localtime()
        print("[ INFO ] Checking for submissions to submit (current time "
              + str(curr_time.tm_hour) + ":" + str(curr_time.tm_min) + ":"
              + str(curr_time.tm_sec) + ")")

        for s in submissions:
            if s.in_interval(prev_time, curr_time):
                s.submit()

        prev_time = curr_time
        time.sleep(CHECK_INTERVAL)


# Call main() when rposter.py is invoked from the command line
if __name__ == "__main__":
    main()

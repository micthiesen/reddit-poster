#!/usr/bin/env python
#
# Automatically posts recurring threads to reddit
# Author: /u/MasterMic


# Imports
import json
import praw
import time


# Constants
CHECK_INTERVAL = 30  # Number of seconds to wait between checking for submissions to post
RETRY_WAIT_TIME = 30  # Number of seconds to wait before retrying to submit an submission
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
            submission = r.submit(self.subreddit, self.title, text=self.text
                     + "\n\n---\nAutomatically posted by "
                     + "[reddit-poster](https://github.com/MasterMic/reddit-poster)")
            print("[ INFO ] Submitted submission titled \"" + self.title + "\" at "
                  + submission.short_link)
        except praw.errors.APIException as e:
            print("[ ERROR ] Submission of submission titled \"" + self.title
                  + "\" failed, trying again in " + str(RETRY_WAIT_TIME) + " seconds:")
            print(str(e))
            time.sleep(RETRY_WAIT_TIME)
            self.submit()

    def in_interval(self, lower, upper):
        lower_minutes = lower.get_minutes()
        upper_minutes = upper.get_minutes()
        minutes = self.time.get_minutes()

        if lower_minutes <= upper_minutes:
            return minutes > lower_minutes and minutes <= upper_minutes
        else:
            return minutes > lower_minutes or minutes <= upper_minutes

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

    def get_minutes(self):
        return (self.day * 1440) + (self.hour * 60) + self.minute

    def to_string(self):
        hour_str = str(self.hour)
        if self.hour < 10:
            hour_str = "0" + hour_str

        minute_str = str(self.minute)
        if self.minute < 10:
            minute_str = "0" + minute_str

        return WEEKDAYS[self.day] + " at " + hour_str + ":" + minute_str


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
    sys_time = time.localtime()
    prev_time = Time(sys_time.tm_wday, sys_time.tm_hour, sys_time.tm_min)
    while True:
        sys_time = time.localtime()
        curr_time = Time(sys_time.tm_wday, sys_time.tm_hour, sys_time.tm_min)
        print("[ INFO ] Checking for submissions to submit (current time "
              + curr_time.to_string() + ")")

        for s in submissions:
            if s.in_interval(prev_time, curr_time):
                s.submit()

        prev_time = curr_time
        time.sleep(CHECK_INTERVAL)


# Call main() when rposter.py is invoked from the command line
if __name__ == "__main__":
    main()

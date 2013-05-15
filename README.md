# reddit-poster
A bot that automatically posts recurring weekly threads to reddit using an easy to configure JSON file. If you are a subreddit moderator, this could be useful for you!

## Installation
1. Make sure you have [Python](http://www.python.org/download/) installed (Python 2.7.4 works best).
2. Install [PRAW](https://github.com/praw-dev/praw), a python reddit API wrapper. reddit-poster depends on this.
3. Download reddit-poster using the ZIP button above. Extract the contents to a folder of your choosing. (Alternatively, you can simply clone this repository.)
4. Configure the settings file, config.json, to your liking (see the next section for details).
5. Run the bot by executing `python rposter.py` in a terminal or command line while in the folder containing rposter.py. If you change the contents of config.json, the bot will need to be restarted.

## Configuration File
There is an example config.json included in the repository which shows the format of the file. More submission objects can be created; just make sure they are separated by a comma. The bot will let you know if the is an error parsing your configuration file.

## More Configuration
By default, the bot checks for submissions to post every 10 seconds. This value can be changed by editing the `CHECK_INTERVAL` global variable found in rposter.py.

Similarly, if posting a submission fails, the bot tries again in 10 seconds. This value can be changed by editing the `RETRY_WAIT_TIME` global variable found in rposter.py.

## Common Issues
If the account you use to post submissions is new or does not have much karma, you will be forced to type a captcha when the bot submits a submission. The bot will be paused until the captcha is entered. Sometimes, if you post too frequently, you will be barred from posting at all.

Gathering enough karma for your bot account usually fixes this problem.

# reddit-poster
A bot that automatically posts recurring weekly threads to reddit using an easy to configure JSON file. If you are a subreddit moderator, this could be useful for you!

## Installation
1. Make sure you have [Python](http://www.python.org/download/) installed (Python 2.7.X works best).
2. Install [PRAW](https://github.com/praw-dev/praw), a python reddit API wrapper. reddit-poster depends on this.
3. Download reddit-poster using the ZIP button above. Extract the contents to a folder of your choosing. (Alternatively, you can simply clone this repository.)
4. Configure a settings file, named config.json, to your liking. An example file (config.json.example) is provided (see the next section for details).
5. Run the bot by executing `python rposter.py` in a terminal or command line while in the folder containing rposter.py. If you change the contents of config.json, the bot will need to be restarted.

## Configuration File
There is an example config.json.example included in the repository which shows the format of the file. Feel free to rename it config.json and use it as your configuration file. More submission objects can be created; just make sure they are separated by a comma. The bot will let you know if the is an error parsing your configuration file.

### subreddit
The subreddit in which to post this particular submission.

### username
The username to use to post this submission.

### password
The password for the aforementioned username.

### title
The title of the submission.

### text
The text of the submission. Note that a small credit notice is appended to all submissions. If you don't like it, feel free to remove it (you'll have to dig around in rposter.py).

### date
Either true or false. If true, the current date will be appended to the title of the submission.

### time
The recurring time of the week to post this submission.

#### day
The day of the week where 0 is Monday, 1 is Tuesday, 2 is Wednesday, 3 is Thursday, 4 is Friday, 5 is Saturday, and 6 is Sunday.

#### hour
The hour, a value from 0 to 23.

#### minute
The minute, a value from 0 to 59.

### topics (optional)
The location of a text file containing weekly topics. The text file should contain one topic per line. Each time the submission is submitted, reddit-poster will pop the top topic from the text file (and delete it) and use it in the submission.

## More Configuration
By default, the bot checks for submissions to post every 30 seconds. This value can be changed by editing the `CHECK_INTERVAL` global variable found in rposter.py.

Similarly, if posting a submission fails, the bot tries again in 30 seconds. This value can be changed by editing the `RETRY_WAIT_TIME` global variable found in rposter.py.

## Common Issues
If the account you use to post submissions is new or does not have much karma, you will be forced to type a captcha when the bot submits a submission. The bot will be paused until the captcha is entered. Sometimes, if you post too frequently, you will be barred from posting at all.

Gathering enough karma for your bot account usually fixes this problem.

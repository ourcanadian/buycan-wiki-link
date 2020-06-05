#!/usr/bin/python
import praw
import re
import os
from datetime import datetime, timedelta

def log(msg):
    SLACK_URL = os.environ['SLACK_URL']
    command = os.popen('''curl -X POST -H 'Content-type: application/json' --data '{"text":"'''+msg+'''"}' '''+SLACK_URL)
    print(command.read())
    print(command.close())


def main():
    # Create the Reddit instance and login using ./praw.ini data
    reddit = praw.Reddit('wikireplier')

    # get current time and correct for how far back we want to look
    _now = datetime.now()
    _x_time_ago = _now - timedelta(minutes=30)

    # convert UTC time to a float for comparison
    read_upto_time = _x_time_ago.timestamp()

    # Get the top 10 values from our subreddit
    subreddit = reddit.subreddit('BuyCanadian')
    for submission in subreddit.new(limit=20):
        created_time = submission.created_utc        
        # any post in the past X time will be read
        if created_time > read_upto_time:
            # Read link from post and determine if its external
            link = submission.url
            if("reddit" not in link):
                log("/u/"+str(submission.author)+" posted "+link)
                log("Check it out here "+submission.permalink)
        else:
            break

if __name__ == "__main__":
    main()

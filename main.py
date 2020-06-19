import praw
import re
import os
import sys
from datetime import datetime, timedelta

'''
    Call via: 
        python3 main.py
    To get last 30 minutes by default.

    Or set custom time (e.g. 2 hours)
        python3 main.py 120
'''

def slackify(submission):
    return "/u/"+str(submission.author)+" posted <https://www.reddit.com"+submission.permalink+"|"+submission.title+">"

def postPrint(submission):
    if('BCWB_SLACK_URL' in os.environ.keys()): 
        SLACK_URL = os.environ['BCWB_SLACK_URL']
        command = os.popen('''curl -X POST -H 'Content-type: application/json' --data '{"text":"'''+slackify(submission)+'''"}' '''+SLACK_URL)
        print(command.read())
        print(command.close())
    else:
        print("/u/"+str(submission.author)+" posted \'"+submission.title+"\'")

def main(minu, lim):
    count = 0
    # Create the Reddit instance and login using ./praw.ini or ~/.config/praw.ini
    reddit = praw.Reddit('wikireplier')

    # get current time and correct for how far back we want to look
    _now = datetime.now()
    _x_time_ago = _now - timedelta(minutes=minu)

    # convert UTC time to a float for comparison
    read_upto_time = _x_time_ago.timestamp()

    # Get the top 20 values from our subreddit
    subreddit = reddit.subreddit('BuyCanadian')
    for submission in subreddit.new(limit=lim):
        count += 1
        created_time = submission.created_utc        
        # any post in the past X time will be read
        if created_time > read_upto_time:
            postPrint(submission)
        else:
            break

    print("\nFound", count, "posts from the last", minu, "minutes.")

if __name__ == "__main__":
    if(len(sys.argv) > 2):
        main(int(sys.argv[1]), int(sys.argv[2]))
    elif(len(sys.argv) > 1):
        main(int(sys.argv[1]), 20)
    else:
        main(30, 20)
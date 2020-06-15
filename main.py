import praw
import re
import os
import sys
from datetime import datetime, timedelta

def log(msg, local):
    if(local):
        print(msg)
    else: 
        SLACK_URL = os.environ['SLACK_URL']
        command = os.popen('''curl -X POST -H 'Content-type: application/json' --data '{"text":"'''+msg+'''"}' '''+SLACK_URL)
        print(command.read())
        print(command.close())


def main(minu, local=False):
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
    for submission in subreddit.new(limit=20):
        count += 1
        created_time = submission.created_utc        
        # any post in the past X time will be read
        if created_time > read_upto_time:
            # Read link from post and determine if its external
            link = submission.url
            if("reddit" not in link):
                log("/u/"+str(submission.author)+" posted "+link+", check it out <https://www.reddit.com"+submission.permalink+"|here>", local)
        else:
            break

if __name__ == "__main__":
    '''
    Call via: 
        python3 main.py
    To get last 30 minutes by default.

    Or set custom time (e.g. 2 hours)
        python3 main.py 120
    '''
    
    called = False
    if(len(sys.argv) > 1):
        local = False
        for comm in sys.argv[1:]:
            if comm in ['-l', '--local']:
                local = True
            elif re.match('\d+', comm):
                main(int(comm), local)
                called = True

    if not called:
        main(30, False)
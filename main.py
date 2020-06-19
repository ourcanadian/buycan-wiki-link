import praw
import re
import os
import sys
import json
from datetime import datetime, timedelta

'''
    Call via: 
        python3 main.py
    To get last 30 minutes by default.

    Or set custom time (e.g. 2 hours)
        python3 main.py 120
'''


with open("./database.json") as json_file:
    DATABASE = json.load(json_file)

def slackify(submission, path):
    return "Check out this <https://www.reddit.com"+submission.permalink+"|recent post> by /u/"+str(submission.author)+" and let them know about <https://wiki.ourcanadian.ca/en/"+path+"|this relevant wiki page.>"

def clean(msg):
    return msg.replace('\'', '\\\'')

def slack(msg):
    if('BCWB_SLACK_URL' in os.environ.keys()): 
        SLACK_URL = os.environ['BCWB_SLACK_URL']
        command = os.popen('''curl -X POST -H 'Content-type: application/json' --data '{"text":"'''+clean(msg)+'''"}' '''+SLACK_URL)
        print(command.read())
        print(command.close())
    else:
        print("-No Slakc access-")
        print(msg)

def sectionize(text):
    tagged = pos_tag(word_tokenize(text))
    sections = []
    section = []
    for word in tagged:
        if word[1] in ['NN', 'NNP', 'NNS', 'IN']:
            section.append(word[0])
        elif len(section) > 0:
            sections.append(section)
            section = []
    if len(section) > 0:
        sections.append(section)
    return sections

def windowSearch(sections):
    phrases = []
    for section in sections:
        N = len(section)

        i = 0
        j = 1

        while i+j <= N:
            while i+j <= N:
                phrase = ' '.join(section[i:i+j])
                phrases.append(phrase)
                i += 1
            i = 0
            j += 1
            
    return phrases

def printSections(sections):
    for section in sections:
        print(' '.join(section))

def urlSearch(text): 
    regex = "(?:http[s]?://)?(?:\w+\.)+(?:\w+)(?:/[A-Za-z0-9\.\-]*)*"
    urls = re.findall(regex, text)
    strippedUrls = [stripUrl(url) for url in urls]
    return [url for url in strippedUrls if url]

def stripEtsyUrl(url):
    regex = "shop/(\w+)\?"
    found = re.findall(regex, url)
    if(found):
        return found[0]
    return None

def stripHostUrl(url, base):
    if(base == "etsy"):
        return stripEtsyUrl(url)

    else:
        return "> TODO: "+base
        
def stripUrl(url):
    regex = "(?:http[s]?://)?(?:\w+\.)?(\w+)\."
    found = re.findall(regex, url)
    if(found):
        base = found[0]
    else:
        return None

    knownHosts = [
        'etsy',
        'facebook',
        'shopify',
        'amazon'
    ]

    if(base in knownHosts):
        return stripHostUrl(url, base)
    else:
        return base

def parseAndSearch(text):
    urls = urlSearch(text)
    if(urls):
        searchTerms = urls
    else:
        sections = sectionize(text)
        searchTerms = windowSearch(sections)
    
    results = []
    for term in searchTerms:
        key = term.lower()
        if key in DATABASE.keys():
            results.append(DATABASE[key])

    return results

def stringify(submission):
    return submission.title+"\n"+submission.selftext+"\n"+submission.url

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
        created_time = submission.created_utc        
        # any post in the past X time will be read
        if created_time > read_upto_time:
            submission_string = stringify(submission)
            results = parseAndSearch(submission_string)
            if(results):
                msg = slackify(submission, results[0])
                slack(msg)
        else:
            break
        count += 1

    print("\nFound", count, "posts from the last", minu, "minutes.")

if __name__ == "__main__":
    if(len(sys.argv) > 2):
        main(int(sys.argv[1]), int(sys.argv[2]))
    elif(len(sys.argv) > 1):
        main(int(sys.argv[1]), 20)
    else:
        main(30, 20)
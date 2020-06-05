#!/usr/bin/python
import praw
import re
import os

def main():
    # Create the Reddit instance

    reddit = praw.Reddit('wikireplier')

    # and login
    #reddit.login(REDDIT_USERNAME, REDDIT_PASS)

    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []

    # If we have run the code before, load the list of posts we have replied to
    else:
        # Read the file into a list and remove any empty values
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    # Get the top 5 values from our subreddit
    subreddit = reddit.subreddit('Optimistic_Orca')
    for submission in subreddit.hot(limit=10):
        #print(submission.title)

        if submission.id not in posts_replied_to:


            # Do a case insensitive search
            if re.search("test", submission.title, re.IGNORECASE):
                # Reply to the post
                submission.reply("I love buying local!")
                print("Bot replying to : ", submission.title, "["+str(submission.id)+"]")

                # Store the current id into our list
                posts_replied_to.append(submission.id)
                break

    # Write our updated list back to the file
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

if __name__ == "__main__":
    main()

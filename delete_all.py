#!/usr/bin/python3

import praw
import time
import datetime

if __name__ == "__main__":
    print(datetime.datetime.now())
    reddit = praw.Reddit('dailysaxthreadbot')
    u = reddit.redditor("dailysaxthreadbot")
    counter = 0
    print("Preparing to delete my comments, boss.")
    for comment in u.comments.new(limit=1000):
        counter+=1
        comment.delete()
        print("Deleted {} comments.".format(counter))

    print("Done")


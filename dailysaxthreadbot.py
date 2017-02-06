#!/usr/bin/python3
"""
DailySaxThreadBot
---
Developed by StoneCharioteer, as a gag.
Designed to run on /r/india to reply with the 

'''
D A I L Y

A

I

L

Y
'''
etc. posts to all posts containing sexual content.



---
"""
import os
import praw
import json
import argparse
import time
import re
from datetime import datetime

def check_submission(submission):
    """
    Checks a reddit submission to see if it's about sax.
    
    """
    valid = False
    submission_title = submission.title
    submission_text = submission.selftext
    #First version, hardcoded word list. 
    #Later put these into a file.
    word_list = [
                "sex",
                "sax",
                "girlfriend",
                "marriage",
                "tinder",
                "penis",
                "vagina",
                "dick",
                "condom",
                "pregnant",
                "anal",
                "blowjob",
                "handjob",
                "dildo",
                "vibrator",
                "sex toys"
                ]
    
    #This needs an exclude list mainly because of the 
    #sensitive posts that could exist.
    exclude_list = [
                    "death",
                    "dies",
                    "died", 
                    "medical", 
                    "hospital"
                ]
    for word in word_list:
        re_str = r"\b{}\b".format(word)

        title_valid = re.search(re_str, submission_title, re.I)
        if title_valid:
            valid = True
            break
        else:
            text_valid = re.search(re_str, submission_text, re.I)
            if text_valid:
                valid = True
                break
    
    if valid:
        #Ensure that the exclude is circumvented.
        for word in exclude_list:
            re_str = r"\b{}\b".format(word)
            title_invld = re.search(re_str, submission_title, re.I)
            if title_invld:
                valid = False
            else:
                desc_invld = re.search(re_str, submission_text, re.I)
                if desc_invld:
                    valid = False
    return valid

def reply_daily_sax_thread(submission):
    """
    First, check if there are these nested replies:
        * DAILY
        ** SAX
        *** THREAD
        **** Wah, wah. You beat me to it. 
        (or)
        **** Contact /u/stonecharioteer if this breaks.
    Also, need to track if there's any need to reply in the first place.
    """
    strdaily = "D A I L Y\n\nA\n\nI\n\nL\n\nY"
    strsax = "S A X\n\nA\n\nX"
    strthread = "T H R E A D\n\nH\n\nR\n\nE\n\nA\n\nD"
    for top_comment in submission.comments:
        #Booleans
        found_daily = False
        found_sax = False
        found_thread = False

        daily = "D A I L Y"

        if daily in top_comment.body:
            found_daily = True
            for next_comment in top_comment.replies:
                sax = "S A X"
                if sax in next_comment.body:
                    found_sax = True
                    for next_next_comment in next_comment.replies:
                        thread = "T H R E A D"
                        if thread in next_next_comment.body:
                            found_thread = True
                        if found_thread:
                            print("Found DAILY>SAX>THREAD!")
                            break
                    if not found_thread:
                        print("FOUND DAILY>SAX. Need to reply THREAD.")
                
                if found_sax:
                    break
            if not found_sax:
                print("Found DAILY. Need to reply SAX>THREAD.")
        if found_daily:
            break
    if not found_daily:
        print("Need to reply DAILY>SAX>THREAD")




def main():
    reddit = praw.Reddit('dailysaxthreadbot')
    subreddit = reddit.subreddit('india')
    post_limit = 1000
    print("Retrieving top {} posts for {}.".format(post_limit, subreddit.title))
    posts = subreddit.hot(limit=post_limit)
    reply_counter = 0
    for submission in posts:
        if check_submission(submission):
            title = submission.title
            created_t = submission.created_utc
            created_dt = datetime.fromtimestamp(created_t)
            message = "Replying to {}, posted at {}.".format(title, created_dt)
            print(message)
            reply_counter += 1
            reply_daily_sax_thread(submission)
            print("*")

    print("*"*10)
    print("Replied to {} posts.".format(reply_counter))
    #print(dir(submission))
    

    
if __name__ == "__main__":
    main()


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
        daily = "D A I L Y"
        if daily in top_comment.body:
            print(top_comment.body)
            for next_comment in top_comment.replies:
                sax = "S A X"
                if sax in next_comment.body:
                    print(next_comment.body)


def main():
    #Read the arguments (path to the client details)
    #Login
    #
    #Get list of last 10 /r/india posts
    reddit = praw.Reddit('dailysaxthreadbot')
    subreddit = reddit.subreddit('india')
    
    print(reddit.user.me())
    print(subreddit.display_name)
    print(subreddit.title)
    #print(subreddit.description)
    print("*"*10)
    for submission in subreddit.hot(limit=500):
        if check_submission(submission):
            print(submission.title)
            reply_daily_sax_thread(submission)
            
            #created_t = submission.created_utc
            #created_dt = datetime.fromtimestamp(created_t)
            #now = datetime.now()
            #time_elpsd = (now - created_dt).total_seconds()/60.0
            #print("At {}, {} min. ago.".format(created_dt, time_elpsd))
            #print(submission.id)
            #print(submission.url)
            print("*")
    print("*"*10)
    #print(dir(submission))
    

    
if __name__ == "__main__":
    main()


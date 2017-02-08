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
import string
from datetime import datetime

def check_submission(submission):
    """
    Checks a reddit submission to see if it's about sax.
    
    """
    print("Inspecting {}".format(submission.title))
    valid = False
    locked = submission.locked
    if locked:
        valid = False
    else:
        pattern = r"[{}]".format(string.punctuation)

        submission_title = re.sub(pattern, "", submission.title)
        submission_text = re.sub(pattern, "", submission.selftext)
        #First version, hardcoded word list. 
        #Later put these into a file.
        word_list = [
                    "sex", "sax","saxx","saxxx","saxxxx",
                    "girlfriend","boyfriend","pullout","ipill","contraceptive"
                    "marriage", "tinder","valentine",
                    "penis", "vagina",
                    "dick", "condom",
                    "pregnant", "anal","kiss",
                    "blowjob", "handjob",
                    "dildo", "vibrator",
                    "sex toys", "get laid",
                    "adult movies", "adult movie",
                    "blue film", "pornography",
                    "get laid","got laid", "getting laid",
                    "porn", "pr0n", "porno", "pedophile", 
                    "sexual", "rape"
                    ]
        
        #This needs an exclude list mainly because of the 
        #sensitive posts that could exist.
        exclude_list = [
                        "death", "dies","rape",
                        "died","murder","murdering","murdered","murders" 
                        "medical", "abuse","learn","resources","education",
                        "hospital", "hospitalize", "hospitalized"
                        ]
        #First, check if the words in the include list are present.
        for word in word_list:
            re_str = r"\b{}\b".format(word)
            title_valid = re.search(re_str, submission_title, re.I)
            if title_valid:
                valid = True
            else:
                text_valid = re.search(re_str, submission_text, re.I)
                if text_valid:
                    valid = True
            if valid:
                break
        if valid:
            #Ensure that the words in the exclude list are not present.
            for word in exclude_list:
                re_str = r"\b{}\b".format(word)
                title_invld = re.search(re_str, submission_title, re.I)
                if title_invld:
                    valid = False
                else:
                    text_invld = re.search(re_str, submission_text, re.I)
                    if text_invld:
                        valid = False
    print("Valid for Sax? {}".format(valid))
    return valid

def reply_to_reddit(submission, message, wait=None):
    '''
        This function handles replies to the given submission.
        There is a limit to how long a gap needs to be provided between replies
        for bots/accounts with low rep. 
        I should be able to guess how long this needs based on the error.
    '''
    if wait==None:
        wait=False
    try_to_reply = True
    while try_to_reply:
        try:
            reply = submission.reply(message)
            try_to_reply = False
        except Exception as e:
            reply = None
            try_to_reply = True
            raise e
    return reply

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
    strsignature = ("Courtesy dailysaxthreadbot. "
                    "Contact /u/stonecharioteer if this breaks."
                    "\n\nTop keks guaranteed.\n\nInqilab Zindabad!")
    strawdamn = ("topkek, bhai. You beat me to it.\n\n"
                "Great job. So what are you doing with your other hand?\n\n"
                "/u/stonecharioteer is proud of you. Now scream with me: SAAARE JAHAAN SE ACHCHA~~!")

    found_daily = False
    found_sax = False
    found_thread = False
    
    for top_comment in submission.comments:
        #Keep track of whether or not these have already been posted.
        found_daily = False
        found_sax = False
        found_thread = False
        daily = "D A I L Y"
        poster_daily = None
        poster_sax = None
        poster_thread = None
        if daily in top_comment.body:
            found_daily = True
            daily_comment = top_comment
            poster_daily = daily_comment.author
            sax_comment = None
            
            for next_comment in top_comment.replies:
                sax = "S A X"
                if sax in next_comment.body:
                    found_sax = True
                    sax_comment = next_comment
                    poster_sax = sax_comment.author
                    for next_next_comment in sax_comment.replies:
                        thread = "T H R E A D"
                        if thread in next_next_comment.body:
                            found_thread = True
                            thread_comment = next_next_comment
                            poster_thread = thread_comment.author
                            print("Found {}:DAILY>{}:SAX>{}:THREAD!".format(poster_daily, poster_sax, poster_thread))
                            #Check if the bot has replied to the comment with a signature
                            #or the awdamn message already.
                            replied_sig = False
                            for further_comment in thread_comment.replies:
                                if further_comment.author == "dailysaxthreadbot":
                                    replied_sig = True
                            if not replied_sig:
                                if poster_thread != "dailysaxthreadbot":
                                    reply_to_reddit(thread_comment, strawdamn, wait=True)
                                else:
                                    reply_to_reddit(thread_comment, strsignature, wait=True)
                            break
                    if not found_thread:
                        print("FOUND {}:DAILY>{}:SAX. Need to reply THREAD.".format(poster_daily, poster_sax))
                        get_reply_thread = reply_to_reddit(sax_comment, strthread, wait=True)
                        get_reply_signature = reply_to_reddit(get_reply_thread, strsignature, wait=True)
                        
                if found_sax:
                    break
            if not found_sax:
                print("Found {}:DAILY. Need to reply SAX>THREAD.".format(poster_daily))
                get_reply_sax = reply_to_reddit(daily_comment, strsax, wait=True)
                get_reply_thread = reply_to_reddit(get_reply_sax, strthread, wait=True)
                get_reply_signature = reply_to_reddit(get_reply_thread, strsignature, wait=True)
                
        if found_daily:
            break
    if not found_daily:
        #Reply to the submission.
        print("Replying DAILY>SAX>THREAD.")
        get_reply_daily = reply_to_reddit(submission, strdaily, wait=True)
        get_reply_sax = reply_to_reddit(get_reply_daily, strsax, wait=True)
        get_reply_thread = reply_to_reddit(get_reply_sax, strthread, wait=True)
        get_reply_signature = reply_to_reddit(get_reply_thread, strsignature, wait=True)
        

def delete_all():
    reddit = praw.Reddit('dailysaxthreadbot')
    #subreddit = reddit.subreddit(subreddit)
    user = reddit.redditor('dailysaxthreadbot')
    counter = 0
    for comment in user.comments.new(limit=1000):
        comment.delete()
        counter += 1
        print("Deleted a comment.")
        time.sleep(10)
    print("{} comments by me deleted.".format(counter))

def main():
    reddit = praw.Reddit('dailysaxthreadbot')
    subreddit = reddit.subreddit('india')#dailysaxthreadbot')
    post_limit = 25
    print("Retrieving top {} posts for {}.".format(post_limit, subreddit.title))
    posts = subreddit.new(limit=post_limit)
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
    
    print(datetime.now())
    main()
    #delete_all()


import praw
import my_info
import argparse
from praw.models import MoreComments
import time

# a reddit instance

def bot_login():
    reddit = praw.Reddit(username = my_info.my_username,
                password = my_info.my_password,
                client_id = my_info.my_id,
                client_secret = my_info.my_secret,
                user_agent = "informativekarma bot v 0.1")
    return reddit
            
r = bot_login()


# def run_bot(r):
#     for submission in r.subreddit('all').rising():
#         for comment in submission.comments:
#             if not isinstance(comment, MoreComments):
#                 if check_phrase(comment):
#                     print("--------------------------------------------------------------------------------")
#                     print(comment.body)
#                     print(submission.title)
#                     comment.reply("this is a test by a bot")
#                     # print(submission.title)
#                     print("--------------------------------------------------------------------------------")
#                     break
#                     #time.sleep(600)

def run_bot(r):
    for submission in r.subreddit('all').new():
        if not submission.is_self and not submission.is_video:
            if "i.redd.it" in submission.url:
                print(submission.url)
                time.sleep(5)

def check_phrase(comment):
    phraseList = ['awesome', 'haha', 'cool', 'lol']
    if any(phrase in comment.body.lower() for phrase in phraseList):
        return True
    else:
        return False

while True:
    run_bot(r)




# with incorrect authentication information, this will error with:
# prawcore.exceptions.OAuthException: invalid_grant error processing request

##print(reddit.user.me())
##
### with our reddit instance, get an endless stream of comments
##for comment in reddit.subreddit('all').stream.comments():
##    print(comment.body)
##
##print("Hello World")

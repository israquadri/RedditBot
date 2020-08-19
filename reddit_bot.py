import praw
import my_info
import argparse
from praw.models import MoreComments
import time
import urllib
import requests
from imageai.Detection import ObjectDetection
from imageai.Prediction import ImagePrediction
import sqlite3

# setting up reddit db
connection = sqlite3.connect("submissions.db")
cursor = connection.cursor()

sql_command = '''CREATE TABLE IF NOT EXISTS reddit_posts 
                        (id TEXT PRIMARY KEY,
                         title TEXT)'''

cursor.execute(sql_command)
connection.commit()

def bot_login():
    reddit = praw.Reddit(username = my_info.my_username,
                password = my_info.my_password,
                client_id = my_info.my_id,
                client_secret = my_info.my_secret,
                user_agent = "informativekarma bot v 0.1")
    return reddit
            
r = bot_login()


def run_bot(r):

#setting up ImageAI model
    model_path = "./models/yolo-tiny.h5"
    input_path = "./input/test.jpg"
    output_path = "./output/newimage.jpg"

    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()
    custom = detector.CustomObjects(cow=True)

#starting to stream through r/all, sorting by new
    for submission in r.subreddit('cows').stream.submissions():
        if "i.redd.it" in submission.url: #checking if its a reddit-hosted image

            #requesting image from url
            image = requests.get(submission.url)

            #writing the reddit image to local file
            file = open("./input/test.jpg", "wb")
            file.write(image.content)
            file.close()

            #detecting all objects in image
            detections = detector.detectCustomObjectsFromImage(custom_objects=custom, input_image=input_path, output_image_path=output_path, minimum_percentage_probability=30)

            #if there's a pizza and i haven't already commented on this post
            if pizza_present(detections) and not check_db(submission.id):
                reply_(submission)
                print("replied to a post")
                print("----------------------------------------")
            
            #delay so that i'm not rate limited
            time.sleep(10)

# add the submission id to the set (to avoid replying to the same post) and comment
def reply_(submission):
    cursor.execute('''INSERT INTO reddit_posts (id, title) VALUES (?, ?)''', (submission.id, submission.title,))
    connection.commit()
    submission.reply("Hey there, " + submission.author.name + ". It looks like your post contains a cow. " +
        "I've detected " + str(get_count()) + " cows on Reddit.\n\n\n\n---\n\n^Beep ^boop. ^I ^am ^a ^bot.")


def check_db(submission_id):
    cursor.execute("""SELECT id FROM reddit_posts 
                                WHERE id=?""", (submission_id,))
    result = cursor.fetchone()
    return result #if result is true, then id already exists in database


def pizza_present(detections):
    #if dictionary isn't empty, a pizza was detected so there is a pizza present
    return bool(detections)

#counts # of submissions in table (total pizzas i've detected)
def get_count():
    count = cursor.execute('select * from reddit_posts;')
    return len(count.fetchall())


run_bot(r)
connection.close()




# with incorrect authentication information, this will error with:
# prawcore.exceptions.OAuthException: invalid_grant error processing request

##print(reddit.user.me())
##
### with our reddit instance, get an endless stream of comments
##for comment in reddit.subreddit('all').stream.comments():
##    print(comment.body)
##
##print("Hello World")

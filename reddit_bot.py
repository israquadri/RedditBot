import praw
import my_info
import argparse
from praw.models import MoreComments
import time
import urllib
import requests
from imageai.Detection import ObjectDetection

# a reddit instance

def bot_login():
    reddit = praw.Reddit(username = my_info.my_username,
                password = my_info.my_password,
                client_id = my_info.my_id,
                client_secret = my_info.my_secret,
                user_agent = "informativekarma bot v 0.1")
    return reddit
            
r = bot_login()

def run_bot(r):
    for submission in r.subreddit('cats').new():
        if not submission.is_self and not submission.is_video:
            if "i.redd.it" in submission.url and not submission.over_18:

                image = requests.get(submission.url)

                file = open("./input/test.jpg", "wb")
                file.write(image.content)
                file.close()
                
                print("File downloaded successfully")

                model_path = "./models/yolo-tiny.h5"
                input_path = "./input/test.jpg"
                output_path = "./output/newimage.jpg"

                detector = ObjectDetection()
                detector.setModelTypeAsTinyYOLOv3()
                detector.setModelPath(model_path)
                detector.loadModel()
                detections = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path, minimum_percentage_probability=20)

                print("Image parsed successfully")

                if not bool(detections):
                    print("No objects were detected")
                    print("--------------------------------------------------------------------------")

                for eachItem in detections:
                    print(eachItem["name"], ": ", eachItem["percentage_probability"])
                    print("--------------------------------------------")
                

                time.sleep(30)

                

def check_phrase(comment):
    phraseList = ['awesome', 'haha', 'cool', 'lol']
    if any(phrase in comment.body.lower() for phrase in phraseList):
        return True
    else:
        return False

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

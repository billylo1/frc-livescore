from livescore import Livescore2024
import sys
import cv2
from PIL import ImageGrab
import numpy as np
import firebase_admin
from firebase_admin import db
from firebase_admin import messaging
import json
import time

cred_obj = firebase_admin.credentials.Certificate('./serviceAccount.json')
databaseURL = 'https://frc-livescore-default-rtdb.firebaseio.com/'
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL,
    'messageSenderId': '139040067484'
	})

# Initialize new Livescore instance
frc = Livescore2024(debug=False)
mostRecentMatchDetails = { "Archimedes": {}, "Curie":  {}, "Daly":  {}, "Galileo":  {}, "Hopper":  {}\
                          , "Johnson": {}, "Milstein":  {}, "Newton":  {}, "Einstein":  {}}

def send_team_message(team, match_name, channel):
    try:
        if team is not None:
            print('Sending message to topic: ' + str(team))
            topic = str(team)
            messageBody = match_name + " on " + channel
            message = messaging.Message(
                notification=messaging.Notification(
                    title=topic+" is up next",
                    body=messageBody),
                topic=topic,
            )
            # Send a message to the devices subscribed to the provided topic.
            response = messaging.send(message)
            # Response is a message ID string.
            print('Successfully sent message:', response)
    except Exception as e:
        print(e)
    return


def read_image(pil_image, channel):
    try:
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        data = frc.read(open_cv_image)
        if data is not None:
            print('Channel: {}, Match: {}, Mode: {}, Time: {}, Blue: {}, Red: {}, BlueTeams: {}, RedTeams: {}'.format(
                channel,
                data.match_name,
                data.mode,
                data.time,
                data.blue.score,
                data.red.score,
                data.blue.teams,
                data.red.teams
            ))
            for team in data.red.teams:
                if team is None:
                    return
                
            for team in data.blue.teams:
                if team is None:
                    return

            if not str(data.time).startswith("0") and not str(data.time).startswith("1") and not str(data.time).startswith("2") and len(str(data.time)) != 4:
                return  

            json_object = json.loads(data.toJSON())

            currentMatchName = json_object["match_name"]
            sendMessage = True

            if not mostRecentMatchDetails[channel].__contains__("match_name") or mostRecentMatchDetails[channel]["match_name"] != currentMatchName:
                if sendMessage:                
                    # send message to channel topics for all red teams and blue teams
                    for team in data.red.teams:
                        send_team_message(team, currentMatchName, channel)
                    
                    for team in data.blue.teams:
                        send_team_message(team, currentMatchName, channel)

            if not mostRecentMatchDetails[channel].__contains__("match_name") \
                or mostRecentMatchDetails[channel]["match_name"] != json_object["match_name"] \
                or mostRecentMatchDetails[channel]["mode"] != json_object["mode"] \
                or mostRecentMatchDetails[channel]["time"] != json_object["time"] \
                or mostRecentMatchDetails[channel]["red"]["score"] != json_object["red"]["score"] \
                or mostRecentMatchDetails[channel]["blue"]["score"] != json_object["blue"]["score"]:
                
                mostRecentMatchDetails[channel] = json_object
                ref = db.reference("/events/" + channel)
                ref.set(json_object)
                # print('Updated firebase with match details for channel: ' + channel)

            # save most recent match key to a local variable

        # else:
            # print('Failed to fetch data')
        

    except Exception as e:
        print(e)

    return

def process_frame(): 
    
    try:
        # open_cv_image = cv2.imread('./scenes2024/auto.png')

        pil_image_right = ImageGrab.grab(all_screens=False)  # false = screen 3
        # pil_image = ImageGrab.grab(all_screens=True)  # true = screen 2
        # crop into 8 images
        crop = True
        menuBarHeight = 42
        if crop:
            pil_image0 = pil_image_right.crop((0, 0+menuBarHeight, pil_image_right.width/2, pil_image_right.height/2+menuBarHeight))
            pil_image1 = pil_image_right.crop((0, pil_image_right.height/2+1+menuBarHeight, pil_image_right.width/2+1, pil_image_right.height+menuBarHeight))
            pil_image2 = pil_image_right.crop((pil_image_right.width/2+1, 0+menuBarHeight, pil_image_right.width, pil_image_right.height/2+menuBarHeight))
            pil_image3 = pil_image_right.crop((pil_image_right.width/2+1, pil_image_right.height/2+1+menuBarHeight, pil_image_right.width, pil_image_right.height+menuBarHeight))
            # pil_image4 = pil_image.crop((0, 0+menuBarHeight, pil_image.width/2, pil_image.height/2+menuBarHeight))
            # pil_image5 = pil_image.crop((0, pil_image.height/2+1+menuBarHeight, pil_image.width/2+1, pil_image.height+menuBarHeight))
            # pil_image6 = pil_image.crop((pil_image.width/2+1, 0+menuBarHeight, pil_image.width, pil_image.height/2+menuBarHeight))
            # pil_image7 = pil_image.crop((pil_image.width/2+1, pil_image.height/2+1+menuBarHeight, pil_image.width, pil_image.height+menuBarHeight))

            read_image(pil_image0, 'Archimedes')
            read_image(pil_image1, 'Curie')
            read_image(pil_image2, 'Daly')
            read_image(pil_image3, 'Galileo')
            # read_image(pil_image4, 'Hopper')
            # read_image(pil_image5, 'Johnson')
            # read_image(pil_image6, 'Milstein')
            # read_image(pil_image7, 'Newton')
        # else:
            # read_image(pil_image, 'Einstein')

    except Exception as e:
        print(e)
        return



while True:
    starttime = time.monotonic()
    process_frame()
    sleep_time = 1.0 - (time.monotonic() - starttime)
    if sleep_time > 0:
        time.sleep(sleep_time)

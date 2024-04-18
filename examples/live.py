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
mostRecentMatchKey = { "Archimedes": "", "Curie": "", "Daly": "", "Galileo": "", "Hopper": "", "Johnson": "", "Milstein": "", "Newton": "", "Einstein": ""}

def send_team_message(team, match_key, channel):
    try:
        if team is not None:
            print('Sending message to topic: ' + str(team))
            topic = str(team)
            messageBody = match_key + " on " + channel
            message = messaging.Message(
                notification=messaging.Notification(
                    title=topic+" is up next",
                    body=messageBody),
                topic=topic,
            )
            # Send a message to the devices subscribed to the provided topic.
            response = messaging.send(message)
            # Response is a message ID string.
            # print('Successfully sent message:', response)
    except Exception as e:
        print(e)
    return


def read_image(pil_image, channel):
    try:
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        data = frc.read(open_cv_image)
        if data is not None:
            print('Channel: {}, Match: {}, Mode: {}, Time: {}, Red: {}, Blue: {}, RedTeams: {}, BlueTeams: {}'.format(
                channel,
                data.match_name,
                data.mode,
                data.time,
                data.red.score,
                data.blue.score,
                data.red.teams,
                data.blue.teams
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
            ref = db.reference("/events/" + channel)
            ref.set(json_object)
            # save most recent match key to a local variable
            currentMatchKey = json_object["match_key"]
            sendMessage = False
            if mostRecentMatchKey[channel] != currentMatchKey and sendMessage:
                
                # send message to channel topics for all red teams and blue teams
                
                for team in data.red.teams:
                    send_team_message(team, currentMatchKey, channel)
                
                for team in data.blue.teams:
                    send_team_message(team, currentMatchKey, channel)

                mostRecentMatchKey[channel] = json_object["match_key"]

        else:
            print('Failed to fetch data')
        

    except Exception as e:
        print(e)

    return

def process_frame(): 
    
    try:
        # open_cv_image = cv2.imread('./scenes2024/auto.png')

        pil_image = ImageGrab.grab(all_screens=False)  # true = screen 2
        # crop into 8 images
        crop = False
        menuBarHeight = 42
        if crop:
            pil_image0 = pil_image.crop((0, 0+menuBarHeight, pil_image.width/3, pil_image.height/3+menuBarHeight))
            pil_image1 = pil_image.crop((0, pil_image.height/3+1+menuBarHeight, pil_image.width/3, pil_image.height/3*2+menuBarHeight))
            pil_image2 = pil_image.crop((0, pil_image.height/3*2+1+menuBarHeight, pil_image.width/3, pil_image.height+menuBarHeight))
            pil_image3 = pil_image.crop((pil_image.width/3+1, 0+menuBarHeight, pil_image.width/3*2, pil_image.height/3+menuBarHeight))
            pil_image4 = pil_image.crop((pil_image.width/3+1, pil_image.height/3+1+menuBarHeight, pil_image.width/3*2, pil_image.height/3*2+menuBarHeight))
            pil_image5 = pil_image.crop((pil_image.width/3+1, pil_image.height/3*2+1+menuBarHeight, pil_image.width/3*2, pil_image.height+menuBarHeight))
            pil_image6 = pil_image.crop((pil_image.width/3*2+1, 0+menuBarHeight, pil_image.width, pil_image.height/3+menuBarHeight))
            pil_image7 = pil_image.crop((pil_image.width/3*2+1, pil_image.height/3+1+menuBarHeight, pil_image.width, pil_image.height/3*2+menuBarHeight))

            read_image(pil_image0, 'Archimedes')
            read_image(pil_image1, 'Curie')
            read_image(pil_image2, 'Daly')
            read_image(pil_image3, 'Galileo')
            read_image(pil_image4, 'Hopper')
            read_image(pil_image5, 'Johnson')
            read_image(pil_image6, 'Milstein')
            read_image(pil_image7, 'Newton')
        else:
            read_image(pil_image, 'Einstein')

    except Exception as e:
        print(e)
        return



while True:
    starttime = time.monotonic()
    process_frame()
    sleep_time = 1.0 - (time.monotonic() - starttime)
    if sleep_time > 0:
        time.sleep(sleep_time)

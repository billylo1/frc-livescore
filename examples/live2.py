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
            sendMessage = False

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

        pil_image4 = ImageGrab.grab(windowId=43001)  # hopper
        read_image(pil_image4, 'Hopper')

        pil_image5 = ImageGrab.grab(windowId=43002)  # johnson
        read_image(pil_image5, 'Johnson')

        pil_image6 = ImageGrab.grab(windowId=43003)  # Milstein
        read_image(pil_image6, 'Milstein')

        pil_image7 = ImageGrab.grab(windowId=43004)  # Newton
        read_image(pil_image7, 'Newton') #47296

        # pil_image99 = ImageGrab.grab(windowId=47296)  # Newton
        # read_image(pil_image99, 'Newton') #47296

    except Exception as e:
        print(e)
        return



while True:
    starttime = time.monotonic()
    process_frame()
    sleep_time = 1.0 - (time.monotonic() - starttime)
    if sleep_time > 0:
        time.sleep(sleep_time)

# process_frame()
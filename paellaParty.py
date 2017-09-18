"""
paellaParty!
Notifies user when information is available...
"""

import twitter
import time
from twilio.rest import Client

accountSID = "AC1fa156de65574a2d9d4843cc33924495"
authToken = "f5aa815c32c9fc6035f1d13b89d7e4a9"
myTwilNum = "+13216167352"
myCellNum = "+13217204928"

twilioCli = Client(accountSID, authToken)

api = twitter.Api(consumer_key="vHRc2kmvVGlbSQDCLWPs2ifKL",
                  consumer_secret="skedX80bprCPehS9RMfhDzKlE0ArzUvDs9ZkmlINW6YCAvHo0U",
                  access_token_key="15213778-5WTwUXaba0fwkslchwArg47HjkyMQnwWC723nab8C",
                  access_token_secret="dL9WMpKanfjYX8VutQcMtGudU0r3EHJajxP64ObOsQtAG")

previousTweets = []


def initiate_loop():
	print("Status: Let the Paella Party begin!")
    while True:
        data = api.GetUserTimeline(15213778)
        for status in data:
            tweetText = status.text
            if tweetText[0] != "@":
                if "Paella" in tweetText or "paella" in tweetText:
                    if status.id not in previousTweets:
                        # send twilio text message to phone
                        twilioCli.messages.create(body=status.text, from_=myTwilNum, to=myCellNum)
                        print(status.text)
                        # add tweet id to previousTweets list
                        previousTweets.append(status.id)
                        print("Added status id: ", status.id, "to previousTweets.")
        time.sleep(3600)


if __name__ == "__main__":
    initiate_loop()
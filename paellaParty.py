"""
paellaParty! Rev.1
Monitors a twitter account id for tweets containing a specified keyword and recieve a text message
when/if a match is found.

Originally created
"""

import twitter
import time
from twilio.rest import Client
from keys import *


# keys are specified and imported from keys.py
twilioCli = Client(accountSID, authToken)
api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
previousTweets = []


class PaellaParty():

    def __init__(self):
        self.twittername = input("Enter twitter id to monitor: ")
        self.monitortext = input("Enter keyword to monitor for: ")
        self.initiate_loop(self.twittername, self.monitortext)

    def initiate_loop(self, twittername, monitortext):
        print("Status: Let the paella party begin!")
        while True:
            data = api.GetUserTimeline(twittername)
            for status in data:
                tweetText = status.text
                if tweetText[0] != "@":
                    if monitortext in tweetText:
                        if status.id not in previousTweets:
                            # paella party found - send twilio text message to phone
                            twilioCli.messages.create(body=status.text, from_=myTwilNum, to=myCellNum)
                            print(status.text)
                            # add tweet id to previousTweets list
                            previousTweets.append(status.id)
                            print("Added status id: ", status.id, "to previousTweets.")
            # check again in 5 minutes for new tweet
            time.sleep(300)


if __name__ == "__main__":
    start=PaellaParty()

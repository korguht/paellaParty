"""
paellaParty! Rev.2
Monitors a twitter account id for tweets containing a specified keyword and recieve a text message
when/if a match is found.
"""

import twitter
import time
from twilio.rest import Client
from keys import *


class PaellaParty():

    def __init__(self):
        self.twitter_name = input("Enter twitter id to monitor: ")
        self.monitor_text = input("Enter keyword to monitor for: ")
        self.previous_tweets = self.getoldtweets()
        self.initiate_loop()

    def getdata(self):
        api = twitter.Api(twitter_consumer_key, twitter_consumer_secret, twitter_access_token_key,
                          twitter_access_token_secret)
        data = api.GetUserTimeline(self.twitter_name)
        return data

    def getoldtweets(self):
        tweetids_from_file = []
        file = open("oldtweets.txt", "r")
        for i in file:
            i = i[:-1]
            tweetids_from_file.append(i)
        file.close()
        return tweetids_from_file

    def writeoldtweet(self, tweetid):
        newid = str(tweetid) + "\n"
        file = open("oldtweets.txt", "a")
        file.write(newid)
        file.close()

    def sendsms(self, tweet):
        twilio_cli = Client(twilio_accountSID, twilio_authToken)
        twilio_cli.messages.create(body=tweet, from_=myTwilNum, to=myCellNum)

    def initiate_loop(self):
        print("Status: Let the paella party begin!")
        print("Now monitoring Twitter ID: (" + self.twitter_name + ") for the keyword: (" + self.monitor_text + ").")
        while True:
            data = self.getdata()
            for status in data:
                tweet_text = status.text
                if tweet_text[0] != "@":
                    if self.monitor_text in tweet_text:
                        if str(status.id) not in self.previous_tweets:
                            # paella party found - send twilio text message to phone
                            self.sendsms(status.text)
                            # add tweet id to previousTweets list
                            self.writeoldtweet(status.id)
                            print("Added status id: ", status.id, "to previousTweets.")
            # check again in 5 minutes for new tweet
            time.sleep(300)


start = PaellaParty()
start.getoldtweets()

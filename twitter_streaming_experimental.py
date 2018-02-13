# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

import os

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream



# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '918639046280253440-UJ5I3x4Ru0MhBLyVxyPefNXYq9c7KJg'
ACCESS_SECRET = 'Kj8XelBrq7hS8oR5H0eqfyjJzFNJb4y9pP1pkSOdZnp8R'
CONSUMER_KEY = 'bMdrEm9OEHKYeenT6OXVbsoo7'
CONSUMER_SECRET = 'P6pbJA9MEa2VpDBHvEJ3BBp1XJla66mTOlgdGpMOzPqa8LSsc1'



oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
# iterator = twitter_stream.statuses.filter(track="", language="en")
iterator = twitter_stream.statuses.sample()

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 1000

sample_file = open('twitter_stream_samples3.txt', 'w')

for tweet in iterator:
        tweet_count = tweet_count - 1
       	sample_file.write(json.dumps(tweet))
	sample_file.write("\n")
        if tweet_count <= 0:
		break

sample_file.close()

#We use the file saved from the last step as example
tweets_filename = "twitter_stream_samples3.txt"
tweets_file = open(tweets_filename, "r")

count = 0
for line in tweets_file:
    #total_counts += 1
    try:
        # Read in one line of the file, convert it into a json object 
        tweet = json.loads(line.strip())
        
        # output a new line
        if ('text' in tweet) and (tweet['lang'] == 'en'): # only messages contains 'text' field is a tweet
            count += 1

            print count
            print tweet['user']['screen_name']
            print tweet['created_at']
            print tweet['text']
            
            hashtags = []
            for hashtag in tweet['entities']['hashtags']:
            	hashtags.append(hashtag['text'])
            #output_file.write(str(hashtags))
            if hastags != []:
                print hashtags

    except:
        # read in a line is not in JSON format (sometimes error occured)
        continue












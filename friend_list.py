# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

from datetime import datetime
from time import strptime
import sys
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import requests


# define custom comparator to compare created_at 
def compare_created_at(item1, item2):
	str1 = item1['created_at']
	str2 = item2['created_at']

	year1 = int(str1[26] + str1[27] + str1[28] + str1[29])
	month1 = int(strptime((str1[4] + str1[5] + str1[6]), '%b').tm_mon)
	day1 = int(str1[8] + str1[9])
	hour1 = int(str1[11] + str1[12])
	minute1 = int(str1[14] + str1[15])
	second1 = int(str1[17] + str1[18])

	year2 = int(str2[26] + str2[27] + str2[28] + str2[29])
	month2 = int(strptime((str2[4] + str2[5] + str2[6]), '%b').tm_mon)
	day2 = int(str2[8] + str2[9])
	hour2 = int(str2[11] + str2[12])
	minute2 = int(str2[14] + str2[15])
	second2 = int(str2[17] + str2[18])
	
	date1 = datetime(year1, month1, day1, hour1, minute1, second1)
	date2 = datetime(year2, month2, day2, hour2, minute2, second2)
	if date1 < date2:
		return 1
	if date1 > date2:
		return -1
	return 0

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '918639046280253440-UJ5I3x4Ru0MhBLyVxyPefNXYq9c7KJg'
ACCESS_SECRET = 'Kj8XelBrq7hS8oR5H0eqfyjJzFNJb4y9pP1pkSOdZnp8R'
CONSUMER_KEY = 'bMdrEm9OEHKYeenT6OXVbsoo7'
CONSUMER_SECRET = 'P6pbJA9MEa2VpDBHvEJ3BBp1XJla66mTOlgdGpMOzPqa8LSsc1'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter = Twitter(auth=oauth)

name = raw_input("Please enter name: ")

# user friends count
user_info = twitter.users.lookup(screen_name=name)
friends_count = json.dumps(user_info)
friends_count = json.loads(friends_count)
friends_count = friends_count[0]
friends_count = friends_count['friends_count']
print friends_count

# get list of people that user follows
ids = []
next_cursor = -1

if friends_count > 20:
	while (next_cursor != 0):
		content = twitter.friends.list(screen_name=name, cursor=next_cursor, count=friends_count)
		data = json.dumps(content)
		data = json.loads(data)
		next_cursor = data['next_cursor']

		for x in data['users']:
			if (x['protected'] == False):
				ids.append(x['id_str'])

else:
	content = twitter.friends.list(screen_name=name, cursor=next_cursor, count=friends_count)
	data = json.dumps(content)
	data = json.loads(data)
	for x in data['users']:
		if (x['protected'] == False):
			ids.append(x['id_str'])

# get following people's tweets
count = 20
tweets = []
friends = 0

for x in ids:
    count = 20
    friends += 1


    iterator = twitter.statuses.user_timeline(user_id=x, count=count, exclude_replies=True)

    for tweet in iterator:
        count -= 1

        tweets.append(tweet)

        if count <= 0:
            break

# get own tweets
iterator = twitter.statuses.user_timeline(screen_name=name, count=10, exclude_replies=False)

for tweet in iterator:
    count -= 1

    tweets.append(tweet)
       
    if count <= 0:
        break

# sorting
output_file = open("test_sorted.txt", "w")
sorted_tweets = sorted(tweets, cmp=compare_created_at, reverse=True)

for tweet in sorted_tweets:
	output_file.write(json.dumps(tweet))
	output_file.write('\n \n')


output_file.close()

#JSON_conversion
tweets_file = open("test_sorted.txt", "r")

count = 0
for line in tweets_file:
    try:
        tweet = json.loads(line.strip())
        if ('text' in tweet) and (tweet['lang'] == 'en'): 
            count += 1
          
            print count
            print tweet['user']['screen_name']
            print tweet['created_at']
            print tweet['text']
            print ''
            
            hashtags = []
            for hashtag in tweet['entities']['hashtags']:
            	hashtags.append(hashtag['text'])

            if hastags != []:
                print hashtags

    except:
        continue

tweets_file.close()
print "Total tweets processed: %s"%(count)
print "Total friends processed: %s"%(friends)

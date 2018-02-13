# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# We use the file saved from last step as example
tweets_filename = raw_input("file name: ")
tweets_file = open(tweets_filename, "r")
#output_file = open("test_converted.txt", "w")
#total_counts = 0
count = 0
for line in tweets_file:
    #total_counts += 1
    try:
        # Read in one line of the file, convert it into a json object 
        tweet = json.loads(line.strip())
        

        #output_file.write(str(count))
        #output_file.write("\n")

        # output a new line
        if ('text' in tweet) and (tweet['lang'] == 'en'): # only messages contains 'text' field is a tweet
            count += 1
            #output_file.write(str(tweet['id'])) # This is the tweet's id
            #output_file.write(str(tweet['created_at'])) # when the tweet posted
            #output_file.write(str(tweet['text'])) # content of the tweet
                        
            #output_file.write(str(tweet['user']['id'])) # id of the user who posted the tweet
            #output_file.write(str(tweet['user']['name'])) # name of the user, e.g. "Wei Xu"
            #output_file.write(str(tweet['user']['screen_name'])) # name of the user account, e.g. "cocoweixu"
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

#output_file.write("\n")
#output_file.close()
tweets_file.close()
print "Total tweets processed: %s"%(count)
#print "Total tweets processed: %s"%(total_counts)

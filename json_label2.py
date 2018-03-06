from __future__ import print_function
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import string
import sys

# ----- labeler function ----- #
def labeler_json():
    filename = sys.argv[1]
    inFile = open("%s" %(filename), "r")

    # type_label = conversational (1) / status (2) / phatic (3) / pass-along (4) / emergency (5)
    # pass-along: advertisement, announcement, money-related
    # emergency: natural disaster, hurricane
    type_label_list = []

    # content_label = environmental (1) / politics (2) / sports (3) / technology (4) / media (5) / personal (6) / fact-quote (7) / announcement-living (8):
    # personal: about me, we, you (related to 'my' life or 'me'), opinion
    # fact: fact, statement, objective
    # announcement: Happy --- day!, announcement, something to share (retweet)
    # living: food, furnitures, money-related, incomes, home improvements, tools, hardwares, lifestyle, gardening, location (park), pet
    
    content_label_list = []
    
    # read in the file first
    tweet_list = []
    for line in inFile:
        tweet_list.append(line)
    
    # read in label until "q" label
    labeled_count = 0
    for line in tweet_list:
        tweet = json.loads(line.strip())
        try:
            type_label = tweet["type_label"]
            content_label = tweet["content_label"]
        
            print("count: ", labeled_count, ", type: ", type_label, ", content:", content_label)
        
            if (type_label == "q"):
                break
            else:
                type_label_list.append(type_label)
                content_label_list.append(content_label)
                labeled_count += 1
        except:
            print("no \"q\" label exist in the tweet set")
            break
            # sys.exit(1)
    print("resuming labeling tweets at: ", labeled_count)
    #sys.exit(0)
    # start labeling
    while (labeled_count < len(tweet_list)):
        line = tweet_list[labeled_count]
        tweet = json.loads(line.strip())
        labeled_count += 1
        # read in previous labels until 'q' label
        
        print("\nscreen name: ", tweet['screen_name'])
        print("tweet: ", tweet['text'].encode(encoding="utf-8"))
        type_label = raw_input("type label: ")
        content_label = raw_input("content label: ")
            
        # show bio 
        if (type_label == "bio") or (content_label == "bio"):
            print("\nbio: ", tweet['bio'])
            print("screen name: ", tweet['screen_name'])
            print("tweet: ", tweet['text'].encode(encoding="utf-8"))
            type_label = raw_input("type label: ")
            content_label = raw_input("content label: ")
            
        # quit
        elif (type_label == "quit") or (content_label == "quit"):
            print("exiting labeling")
            type_label_list.append("q")
            content_label_list.append("q")
            
            break
        
        # add to list
        type_label_list.append(type_label)
        content_label_list.append(content_label)
             
    # close inFile
    inFile.close()
    
    # create an output file
    outFile = open("%s" %(filename+"_l"), "w")
    label = open ("%s" %(filename+"_label"), "w")
    count = 0
    for line in tweet_list:
        tweet = json.loads(line.strip())
        try:
            tweet['type_label'] = type_label_list[count]
            tweet['content_label'] = content_label_list[count]
            outFile.write(json.dumps(tweet))
            outFile.write('\n')
            label.write(type_label_list[count])
            label.write(" ")
            label.write(content_label_list[count])
            label.write('\n')
            count += 1
        except:
            outFile.write(json.dumps(tweet))
            outFile.write("\n")
    # close outFile
    outFile.close()
    label.close()
    print("finished label. Total: ", count, " lines read")
        

#    # check if there was a previous labeling
#    already_labeled = 0
#    for line in inFile:
#        tweet = json.loads(line.strip())
#
#        try:
#            if (tweet["category"] != "quit"):
#                category_list.append(tweet["category"])
#                #print(tweet["category"])
#            else: 
#                break
#            already_labeled += 1
#        except:
#            break
#
#    label_count = 0
#    inFile.close()
#    inFile = open("%s" %(filename), "r")
#    for line in inFile:
#        #print("WO")
#        if (already_labeled > 0):
#            already_labeled -= 1
#            continue
#        #print("qo")
#        tweet = json.loads(line.strip())
#        print("\nscreen name: ", tweet['screen_name'])
#        print("tweet: ", tweet['text'].encode(encoding="utf-8"))
#        input_category = raw_input("Label: ")
#
#        if (input_category == "previous") or (input_category == "Previous") \
#            or (input_category == "pervious") or (input_category == "Pervious") \
#            or (input_category == "prev") or (input_category == "perv"):
#            category_list.pop()
#            print("\n", prev_line)
#            new_input = raw_input("New label for previous line: ")
#            icategory_list.append(new_input)
#
#            print("screen name: ", tweet['screen_name'])
#            print("tweet: ", tweet['text'].encode(encoding="utf-8"))
#            input_category = raw_input("Label: ")
#        elif (input_category == "bio"):
#            print("\nbio: ", tweet['bio'])
#            print("screen name: ", tweet['screen_name'])
#            print("tweet: ", tweet['text'].encode(encoding="utf-8"))
#            new_input = raw_input("Label: ")
#            category_list.append(new_input)
#        elif (input_category == "quit"):
#            print("exiting labeling")
#            category_list.append("q")
#            break
#        category_list.append(input_category)
#        prev_line = "previous line: " + tweet['text'].encode(encoding="utf-8")
#        
#        label_count += 1
#
#    inFile.close()
#    inFile = open("%s" %(filename), "r")   
#    filename += "_labeled"
#    outFile = open("%s" %(filename), "w")
#    count = 0
#    print("labeling....")
#    for line in inFile:
#        if (label_count < 0):
#            break
#        label_count -= 1
#        tweet = json.loads(line.strip())
#        tweet['category'] = category_list[count]
#        count += 1
#        outFile.write(json.dumps(tweet))
#        outFile.write('\n')
#
#    inFile.close()
#    outFile.close()
#    print("tweet text saved in file: %s" %(filename))
#    print("%s entries read" %(count))

# ----- main ----- #
def main():
    labeler_json()

# ---------------------- #
if __name__ == "__main__":
    main()

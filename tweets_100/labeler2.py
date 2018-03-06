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
    # category_list1 = conversational (1) / status (2) / phatic (3) / pass-along (4) 
    type_label_list = []
    # possible contents = environmental (5) / politics (6) / sports (7) / technology (8) / media (9) / personal (10) / business (11)
    content_label_list = []
    # read in the file first
    tweet_list = []
    for line in inFile:
        tweet_list.append(line)

    label_count = 0
    # start labeling
    for line in tweet_list:
        tweet = json.loads(line.strip())
        try:
            if(tweet["type_label"] != "q"):
                type_label_list.append(tweet["type_label"])
                content_label_list.append(tweet["content_label"])

                print("category type: ", tweet["type_label"], ", content: ", tweet["content_label"])

            else:
                raise  
        except:
            print("\nscreen name: ", tweet['screen_name'])
            print("tweet: ", tweet['text'].encode(encoding="utf-8"))
            type_label = raw_input("type label: ")
            content_label = raw_input("content label: ")
            
           #if (input_category == "previous") or (input_category == "Previous") \
           #     or (input_category == "pervious") or (input_category == "Pervious") \
           #     or (input_category == "prev") or (input_category == "perv"):
           #     category_list.pop()
           #     print("\n", prev_line)
           #     new_input = raw_input("New label for previous line: ")
           #     category_list.append(new_input)

           #     print("screen name: ", tweet['screen_name'])
           #     print("tweet: ", tweet['text'].encode(encoding="utf-8"))
           #     input_category = raw_input("Label: ")
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

            type_label_list.append(type_label)
            content_label_list.append(content_label)
            #prev_line = "previous line: " + tweet['text'].encode(encoding="utf-8")
             
            label_count += 1
    # close inFile
    inFile.close()
    
    # create an output file
    outFile = open("%s" %(filename+"_l"), "w")
    count = 0
    for line in tweet_list:
        tweet = json.loads(line.strip())
        try:
            tweet['type_label'] = type_label_list[count]
            tweet['content_label'] = content_label_list[count]
            count += 1
            outFile.write(json.dumps(tweet))
            outFile.write('\n')
        except:
            outFile.write(json.dumps(tweet))
            outFile.write("\n")
    # close outFile
    outFile.close()
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

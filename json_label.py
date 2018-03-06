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
    category_list = []

    # check if there was a previous labeling
    already_labeled = 0
    for line in inFile:
        tweet = json.loads(line.strip())

        try:
            if (tweet["category"] != "quit"):
                category_list.append(tweet["category"])
                #print(tweet["category"])
            else: 
                break
            already_labeled += 1
        except:
            break

    label_count = 0
    inFile.close()
    inFile = open("%s" %(filename), "r")
    for line in inFile:
        #print("WO")
        if (already_labeled > 0):
            already_labeled -= 1
            continue
        #print("qo")
        tweet = json.loads(line.strip())
        print("\nscreen name: ", tweet['screen_name'])
        print("tweet: ", tweet['text'].encode(encoding="utf-8"))
        input_category = raw_input("Label: ")

        if (input_category == "previous") or (input_category == "Previous") \
            or (input_category == "pervious") or (input_category == "Pervious") \
            or (input_category == "prev") or (input_category == "perv"):
            category_list.pop()
            print("\n", prev_line)
            new_input = raw_input("New label for previous line: ")
            icategory_list.append(new_input)

            print("screen name: ", tweet['screen_name'])
            print("tweet: ", tweet['text'].encode(encoding="utf-8"))
            input_category = raw_input("Label: ")
        elif (input_category == "bio"):
            print("\nbio: ", tweet['bio'])
            print("screen name: ", tweet['screen_name'])
            print("tweet: ", tweet['text'].encode(encoding="utf-8"))
            new_input = raw_input("Label: ")
            category_list.append(new_input)
        elif (input_category == "quit"):
            print("exiting labeling")
            category_list.append("q")
            break
        category_list.append(input_category)
        prev_line = "previous line: " + tweet['text'].encode(encoding="utf-8")
        

        label_count += 1

    label_file = open("labels.txt", "w")
    inFile.close()
    inFile = open("%s" %(filename), "r")   
    filename += "_labeled"
    outFile = open("%s" %(filename), "w")
    count = 0
    print("labeling....")
    for line in inFile:
        if (label_count < 0):
            break
        label_count -= 1
        tweet = json.loads(line.strip())
        tweet['category'] = category_list[count]
        count += 1
        outFile.write(json.dumps(tweet))
        outFile.write('\n')
        label_file.write(category_list[count])
        label_file.write('\n')

    inFile.close()
    outFile.close()
    print("tweet text saved in file: %s" %(filename))
    print("%s entries read" %(count))

# ----- main ----- #
def main():
    labeler_json()

# ---------------------- #
if __name__ == "__main__":
    main()

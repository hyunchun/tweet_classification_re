from __future__ import print_function
from __future__ import division
import dynet as dy
import sys
import string

# ----- simple Perceptron: using dynet ----- #
# Name: Hyun A Chung

# ----- reading input functions ----- #
# read in necessary files
def read_files():
    train_filename = sys.argv[1]
    train_file = open("%s" %(train_filename), "r")
    test_file = open("test_set", "r")

    # read in train file
    # train_list: list of each lines in train file
    train_list = []
    for line in train_file:
        train_list.append(line)

    # read in test file
    # test_list: list of each lines in test file
    test_list = []
    for line in test_file:
        test_list.append(line)

    train_file.close()
    test_file.close()

    return train_list, test_list


# read in unique words in the sample data and training instances
def read_trainset(train_list):
    inputs = []
    targets = []
    unique_vector = []
    features_total = 0
    count = 0

    for line in train_list:
        count += 1
        line = line.strip().split()

        # add target to targets list
        targets.append(int(line.pop(0)))

        # add the current line to inputs list
        line[:] = [word.strip(string.punctuation) for word in line]
        inputs.append(line)

        # count number of unqiue words in the input
        for word in line:
            if word not in unique_vector:
                features_total += 1
                unique_vector.append(word)

    print("%s lines for train" %(count + 1))
    return inputs, targets, unique_vector, features_total

# create network input vector in respect to number of unique words in the train set
def create_inputVector(word_inputs, unique_vector, features_total):
    network_input = []
    for line in word_inputs:
        # set all entries on the vector to 0
        inputVector = [0] * features_total

        # set position to 1 if the index's unique word exist in the given tweet
        for word in line:
            inputVector[unique_vector.index(word)] = 1

        network_input.append(inputVector)

    return network_input


# ----- create network functions ----- #
# create a network for the given input and output
def create_network(pWeight, inputs, expected_answer):
    # add parameters to graph as expressions
    Weight = dy.parameter(pWeight)
    input_dy = dy.vecInput(len(inputs))
    input_dy.set(inputs)
    target_output = dy.scalarInput(expected_answer)
    output = (Weight*input_dy)
    # print(output.value())

    if (target_output.value() == 1) and (output > 0):   
        return 0
    elif (target_output.value() == 0) and (output < 0): 
        return 0
    else: 
        if (output < 0): 
            return (-output)
        return output

# ----- test network functions ----- #
# test the network for the given input
def test_network(pWeight, input_dy):
    # add parameters to graph as expressions
    Weight = dy.parameter(pWeight)

    # return what the network returns
    output = (Weight*input_dy)
    return output

# run test_network function for the given input
def test(test_list, pWeight, unique_vector, features_total):
    input_dy = dy.vecInput(features_total)
    output_list = []
    for line in test_list:
        test_line = line.split()
        target = test_line[0]
        test_line = test_line[1:]
        test_vector = [0] * features_total
        all_unique = True

        for word in test_line:
            try:
                test_vector[unique_vector.index(word)] = 1
                all_unique = False
            except:
                continue

        input_dy.set(test_vector)

        if all_unique:
            output = 0
            print( "%s: %s" %(target, output))
            output_list.append(output)
        else:
            output = test_network(pWeight, input_dy)
            print( "%s: %s" %(target, output.value()))
            output_list.append(output.value())

    print("softmax version")
    output_list_expression = dy.vecInput(len(unique_vector))
    output_list_expression.set(output_list)
    output_list_softmax = dy.softmax(output_list_expression)
    for index, line in enumerate(test_list):
        target = line[0]
        return_value =  output_list_softmax[index].value()
        print("%s: %s" %(target, return_value))


# ------- main ------- #
def main():
    # new computation graph
    dy.renew_cg()

    word_inputs = [] 
    targets = []
    unique_vector = []
    network_input = []

    # read in input files first
    train_list, test_list = read_files()

    # ----- training ----- #
    # analysis the train_list
    word_inputs, targets, unique_vector, features_total = read_trainset(train_list)
    network_input = create_inputVector(word_inputs, unique_vector, features_total)

    # add features here and increase features_total

    # create parameters
    para_collec = dy.ParameterCollection()
    pWeight = para_collec.add_parameters((1, features_total))
    trainer = dy.SimpleSGDTrainer(para_collec)

    loop = True
    loop_count = 0
    while(loop):
        loop_count += 1
        print("loop count: ", loop_count)
        loop = False
        for line, target in zip(network_input, targets):
            Weight = dy.parameter(pWeight)
            # add parameters to graph as expressions
            input_dy = dy.vecInput(len(line))
            input_dy.set(line)
            target_output = dy.scalarInput(target)
            output = (Weight*input_dy)
            loss_value = (output).value() # forward
            # print(output.value())
            if ((target == 1) and (output.value() < 0)) or ((target == 0) and (output.value() > 0)):
                loop = True
                print("targe is: ", target)
                print("loss before step is: ", loss_value)
                if (loss_value < 0):
                    print(output.value())
                    output = -output
                    print(output.value())
                output.backward()
                trainer.update()
                loss_value = (output).value(recalculate=True)
                print("loss after step is: ", loss_value)
    # loop = True
    # # while(loop):
    # for i in xrange(50):
    #     # loop = False
    #     for line, target in zip(network_input, targets):
    #         loss = create_network(pWeight, line, target)
    #         try:
    #             # print("%s: %s" %(target, loss.value()))
    #             loss.backward()
    #             trainer.update()
    #             # loop = True
    #         except:
    #             # print("%s: %s" %(target, loss))
    #             continue
    #         # if (seen_instances > 1 and seen_instances % 100 == 0):
    #         #     print("average loss is: %s" %(total_loss / seen_instances))

    # ----- testing ----- #
    print("testing...")
    test(test_list, pWeight, unique_vector, features_total)

# ---------------------- #
if __name__ == "__main__":
    main()
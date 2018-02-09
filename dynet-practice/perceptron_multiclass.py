from __future__ import print_function
from __future__ import division
import dynet as dy
import sys
import string
import operator

# ----- simple Perceptron: using dynet ----- #
# Name: Hyun A Chung

# ----- reading input functions ----- #
# read in necessary files
def read_files():
    train_filename = "classed_70_daily547"
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
    unique_class = []
    features_total = 0
    count = 0

    for line in train_list:
        count += 1
        line = line.strip().split()

        # add target to targets list
        targets.append(line.pop(0))
        # print(targets[-1])
        if targets[-1] not in unique_class:
            unique_class.append(targets[-1])

        # add the current line to inputs list
        line[:] = [word.strip(string.punctuation) for word in line]
        inputs.append(line)

        # count number of unqiue words in the input
        for word in line:
            if word not in unique_vector:
                features_total += 1
                unique_vector.append(word)

    print("%s lines for train" %(count))
    return inputs, targets, unique_vector, features_total, unique_class

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


# ----- test network functions ----- #
# test the network for the given input
def test_network(pWeight, input_dy):
    # add parameters to graph as expressions
    weight = dy.parameter(pWeight)

    # return what the network returns
    # target_output = dy.scalarInput(unique_class.index(target))
    e_a = (weight*input_dy)
    # print(e_a.value())
    output_index = max(enumerate(e_a.value()), key=operator.itemgetter(1))
    output_index = output_index[0]
    # print(output_index)
    return output_index

# run test_network function for the given input
def test(test_list, pWeight, unique_vector, features_total, unique_class):
    input_dy = dy.vecInput(features_total)
    output_list = []
    # print(unique_class)
    for line in test_list:
        test_line = line.split()
        target = test_line[0]
        test_line = test_line[1:]
        test_vector = [0] * features_total
        all_unique = True
        # print(unique_vector)
        for word in test_line:
            # print(word)
            try:
                test_vector[unique_vector.index(word)] = 1
                all_unique = False
            except:
                continue

        input_dy.set(test_vector)

        if all_unique:
            print("none")
            # print( "%s: %s" %(unique_class.index(target), output))
            # output_list.append(output)
        else:
            output = test_network(pWeight, input_dy)
            # print( "%s: %s" %(unique_class.index(target), output))
            # output_list.append(output)
            print("target: %s, output: %s" %(target, unique_class[output]))

    # print("softmax version")
    # output_list_expression = dy.vecInput(len(unique_vector))
    # output_list_expression.set(output_list)
    # output_list_softmax = dy.softmax(output_list_expression)
    # for index, line in enumerate(test_list):
    #     target = line[0]
    #     return_value =  output_list_softmax[index].value()
    #     print("%s: %s" %(target, return_value))


# ------- main ------- #
def main():
    # new computation graph
    dy.renew_cg()

    word_inputs = [] u
    targets = []
    unique_vector = []
    network_input = []
    unique_class = []

    # read in input files first
    train_list, test_list = read_files()

    # ----- training ----- #
    # analysis the train_list
    word_inputs, targets, unique_vector, features_total, unique_class = read_trainset(train_list)
    network_input = create_inputVector(word_inputs, unique_vector, features_total)
    # print(unique_class)

    # # add features here and increase features_total

    # create parameters
    para_collec = dy.ParameterCollection()
    height = len(unique_class)
    pWeight = para_collec.add_parameters((height, features_total))
    pClassWeight = para_collec.add_parameters((1, height))
    # weight = dy.parameter(pWeight)
    # print(weight.dim())
    trainer = dy.SimpleSGDTrainer(para_collec)

    loop = True
    loop_count = 0
    while(loop):
    # for i in xrange(10):
        loop_count += 1
        # print("loop count: ", loop_count)
        loop = False
        for line, target in zip(network_input, targets):
            weight = dy.parameter(pWeight)
            classWeight = dy.parameter(pClassWeight)

            # add parameters to graph as expressions
            input_dy = dy.vecInput(len(line))
            input_dy.set(line)
            # print("target is: ", unique_class.index(target))
            target_output = dy.scalarInput(unique_class.index(target))
            output = dy.pickneglogsoftmax((weight*input_dy), unique_class.index(target))
            loss_value = output.value()
            # print((weight*input_dy).value())
            # print(loss_value)

            if (loss_value > 0.3):
                # print("before: ", loss_value)
                loop = True

                output.backward()
                # output.backward()
                trainer.update()

                loss_value = output.value(recalculate=True)
                # print("after: ",loss_value)
            # print(output.value())
            # e_b = (classWeight*e_a)
            # loss_value = e_b.value() # forward
            # output = dy.softmax(e_b)
            # print(e_b.value())
            # print(output.value())
            # picked_e = picked.value()

            # print(output.value())
            # print(output_result)
            # if (target != output_result_index):
            #     # loop = True
            #     print("target is: ", unique_class.index(target))
            #     print("output was: %s, loss before step is: %s" %(output_result_index, picked_e))

            #     if (picked_e < 0):
            #         output = -output

            #     # output[output_result].backward()
            #     trainer.update()
            #     picked_updated = dy.pick(output, output_result_index)
            #     print("loss after step is: ", picked_updated.value())

    # # ----- testing ----- #
    print("testing...")
    test(test_list, pWeight, unique_vector, features_total, unique_class)

# ---------------------- #
if __name__ == "__main__":
    main()


            # # add parameters to graph as expressions
            # input_dy = dy.vecInput(len(line))
            # input_dy.set(line)
            # print("input: ", input_dy.dim())
            # print("weight: ", Weight.dim())
            # target_output = dy.scalarInput(unique_class.index(target))
            # output = (Weight*input_dy)
            # loss_value = max(output.value()) # forward
            # print("output: ", output.dim())
            # # print(output.value())
            # output_result = max(enumerate(output.value()), key=operator.itemgetter(1))
            # output_result = output_result[0]
            # print("target index: ", unique_class.index(target))
            # print(output.value())
            # print(output_result)
            # if (target != output_result):
            #     loop = True
            #     print("target is: ", target)
            #     print("output was: %s, loss before step is: %s" %(output_result, loss_value))
            #     if (loss_value < 0):
            #         print(output.value())
            #         output = -output
            #         print(output.value())
            #     modify = pWeight[output_result]
            #     print(modify.dim())
            #     modify.backward()
            #     trainer.update()
            #     loss_value = (output).value(recalculate=True)
            #     print("loss after step is: ", loss_value)
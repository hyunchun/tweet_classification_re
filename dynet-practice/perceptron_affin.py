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
def test_network(features_total, unique_vector, lookup, pW1, pBias1, pW2, pBias2, input_dy):
    # add parameters to graph as expressions
    # weight = dy.parameter(pWeight)
    w1 = dy.parameter(pW1)
    bias1 = dy.parameter(pBias1)
    w2 = dy.parameter(pW2)
    bias2 = dy.parameter(pBias2)

    inputs = []
    # print(input_dy)
    for word in input_dy:
        inputs.append(lookup[unique_vector.index(word)])
    e_in = sum(inputs)/features_total
    e_a = dy.affine_transform([bias1, w1, e_in])
    e_b = dy.rectify(e_a)
    e_out = dy.affine_transform([bias2, w2, e_b])
    print(e_out.value())
    output_index = max(enumerate(e_out.value()), key=operator.itemgetter(1))

    # return what the network returns
    output_index = output_index[0]

    return output_index

# run test_network function for the given input
def test(test_list, lookup, pW1, pBias1, pW2, pBias2, unique_vector, features_total, unique_class):
    output_list = []

    for line in test_list:
        input_dy = []
        test_line = line.split()
        target = test_line[0]
        test_line = test_line[1:]
        all_unique = True

        for word in test_line:
            if word in unique_vector:
                input_dy.append(word)
                all_unique = False

        if all_unique:
            print("none")

        else:
            output = test_network(features_total, unique_vector, lookup, pW1, pBias1, pW2, pBias2, input_dy)

            print("target: %s, output: %s" %(target, unique_class[output]))



# ------- main ------- #
def main():
    # new computation graph
    dy.renew_cg()

    word_inputs = [] 
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

    # # add features here and increase features_total

    # create parameters
    para_collec = dy.ParameterCollection()
    pW1 = para_collec.add_parameters((features_total, 100))
    pBias1 = para_collec.add_parameters((features_total))
    pW2 = para_collec.add_parameters((len(unique_class), features_total))
    pBias2 = para_collec.add_parameters((len(unique_class)))
    lookup = para_collec.add_lookup_parameters((len(unique_vector), 100))

    w1 = dy.parameter(pW1)
    bias1 = dy.parameter(pBias1)
    w2 = dy.parameter(pW2)
    bias2 = dy.parameter(pBias2)

    trainer = dy.SimpleSGDTrainer(para_collec)

    loop = True
    loop_count = 0
    while(loop):
    # for i in xrange(10):
        loop_count += 1
        # print("loop count: ", loop_count)
        loop = False
        index = 0
        for line, target in zip(word_inputs, targets):
            inputs = []
            for word in line:
                inputs.append(lookup[unique_vector.index(word)])
            # QUESTION ON input tensor
            input_dy = dy.inputTensor(inputs)
            e_in = dy.sum_elems(input_dy)/features_total
            e_a = dy.affine_transform([bias1, w1, e_in])
            e_b = dy.rectify(e_a)
            e_out = dy.affine_transform([bias2, w2, e_b])
            output = dy.pickneglogsoftmax(e_out, unique_class.index(target))
            loss_value = output.scalar_value()

                # every time we finish a loop in training and measure performance of developing set -> person
                # loop until performance is stable (not much difference)
                # if accuracy of developing performace haven't changed, stop
                # print("\nbefore: ", loss_value)
                loop = True

                output.backward()
                trainer.update()

                loss_value = output.value(recalculate=True)
                # print("after : ", loss_value)

    # ----- testing ----- #
    print("testing...")
    test(test_list, lookup, pW1, pBias1, pW2, pBias2, unique_vector, features_total, unique_class)

# ---------------------- #
if __name__ == "__main__":
    main()
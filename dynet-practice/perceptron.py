from __future__ import print_function
from __future__ import division
import dynet as dy
import sys
import string

# ----- simple Perceptron: using dynet ----- #
# Name: Hyun A Chung

# ----- reading input functions ----- #
# read in unique words in the sample data and training instances
def readInput():
    inputs = []
    targets = []
    unique_vector = []
    unique_total = 0

    filename = sys.argv[1]
    input_file = open("%s" %(filename), "r")

    for line in input_file:
        line = line.strip().split()

        # add target to targets list
        targets.append(int(line.pop(0)))

        # add the current line to inputs list
        line[:] = [word.strip(string.punctuation) for word in line]
        inputs.append(line)

        # count number of unqiue words in the input
        for word in line:
            if word not in unique_vector:
                unique_total += 1
                unique_vector.append(word)

    input_file.close()
    return inputs, targets, unique_vector, unique_total

# ----- create network functions ----- #
# create a network for the given input and output
def create_network(pWeight, inputs, expected_answer):
    # new computation graph
    dy.renew_cg()

    # add parameters to graph as expressions
    Weight = dy.parameter(pWeight)
    input_dy = dy.vecInput(len(inputs))
    input_dy.set(inputs)
    target_output = dy.scalarInput(expected_answer)
    output = dy.logistic(dy.tanh(Weight*input_dy))
    loss =  dy.binary_log_loss(output, target_output)
    return loss

# ----- test network functions ----- #
# test the network for the given input
def test_network(pWeight, input_dy):
    # add parameters to graph as expressions
    Weight = dy.parameter(pWeight)

    # return what the network returns
    output = dy.logistic(dy.tanh(Weight*input_dy))
    return output

# run test_network function for the given input
def test(pWeight, unique_vector, unique_total):
    input_dy = dy.vecInput(unique_total)
    test_file = open("test_set", "r")
    for line in test_file:
        test_line = line.split()
        target = test_line[0]
        test_line = test_line[1:]
        test_vector = [0] * unique_total
        for word in test_line:
            try:
                test_vector[unique_vector.index(word)] = 1
            except:
                continue
        input_dy.set(test_vector)
        output = test_network(pWeight, input_dy)
        print( "%s: %s" %(target, output.value()))


# ------- main ------- #
def main():
    word_inputs = [] 
    targets = []
    unique_vector = []
    word_inputs, targets, unique_vector, unique_total = readInput()
    network_input = []

    for line in word_inputs:
        # print(line)
        inputVector = [0] * unique_input

        for word in line:
            inputVector[unique.index(word)] = 1

        network_input.append(inputVector)
        # print(inputVector)
    # print(network_input)
    # print(len(network_input))
    # print(len(targets))
    m2 = dy.ParameterCollection()
    pW = m2.add_parameters((1, unique_input))
    trainer = dy.SimpleSGDTrainer(m2)

    seen_instances = 0
    total_loss = 0

    for line, target in zip(network_input, targets):
        loss = create_network(pW, line, target)
        seen_instances += 1
        total_loss += loss.value()
        loss.backward()
        trainer.update()
        if (seen_instances > 1 and seen_instances % 100 == 0):
            print("average loss is: %s" %(total_loss / seen_instances))

    print("testing...")
    test(pW, unique, unique_input)



















    # weight is parameter 
    # create presence vector of 0 and 1 (vector size: number of unique words, 1 if it is in sentence, 0 otherwise) 
    # multiply the presence vector with weight (expression)
    # for line in inputs:
    #   print(*line)
    # print(unique_input)
    # # for index, line in enumerate(inputs):
    # #     print line

    # things that are needed for dynet:
        # 1. input vector -> DONE
        # 2. weight
        # 3. expression



# ---------------------- #
if __name__ == "__main__":
    main()
import dynet as dy
print dy.__version__

#create training instances, as before
def create_xor_instances(num_rounds=2000):
	questions = []
	answers = []
	for round in xrange(num_rounds):
		for x1 in 0,1:
			for x2 in 0,1:
				answer = 0 if x1==x2 else 1
				questions.append((x1, x2))
				answers.append(answer)
	return questions, answers

questions, answers = create_xor_instances()

# create a network for the xor problem given input and output
def create_xor_network(pW, pV, pb, inputs, expected_answer):
	dy.renew_cg() # new computation graph
	W = dy.parameter(pW) # add parameters to graph as expressions
	V = dy.parameter(pV)
	b = dy.parameter(pb)
	x = dy.vecInput(len(inputs))
	x.set(inputs)
	y = dy.scalarInput(expected_answer)
	output = dy.logistic(V*(dy.tanh((W*x)+b)))
	loss =  dy.binary_log_loss(output, y)
	return loss

m2 = dy.ParameterCollection()
pW = m2.add_parameters((8,2))
# example = dy.parameter(pW)
# print(example.dim())
pV = m2.add_parameters((1,8))
pb = m2.add_parameters((8))
trainer = dy.SimpleSGDTrainer(m2)

seen_instances = 0
total_loss = 0
for question, answer in zip(questions, answers):
	loss = create_xor_network(pW, pV, pb, question, answer)
	seen_instances += 1
	total_loss += loss.value()
	loss.backward()
	trainer.update()
	if (seen_instances > 1 and seen_instances % 100 == 0):
		print "average loss is:",total_loss / seen_instances

# testing process

# test the network for the xor problem given input
def test_xor_network(pW, pV, pb, x):
	W = dy.parameter(pW) # add parameters to graph as expressions
	V = dy.parameter(pV)
	b = dy.parameter(pb)
	output = dy.logistic(V*(dy.tanh((W*x)+b)))
	return output

x = dy.vecInput(2) # an input vector of size 2. Also an expression
x.set([0, 1])
output = test_xor_network(pW, pV, pb, x)
print "0, 1", output.value()
x.set([1, 1])
output = test_xor_network(pW, pV, pb, x)
print "1, 1", output.value()
x.set([1, 0])
output = test_xor_network(pW, pV, pb, x)
print "1, 0", output.value()
x.set([0, 0])
output = test_xor_network(pW, pV, pb, x)
print "0, 0", output.value()
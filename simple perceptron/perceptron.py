import sys
import string

# ----- sign function ----- #
# returns 1 and -1 depending on n (sum)
def sign(n):
	if (n >= 0):
		return 1
	else:
		return -1


# ----- class Perceptron ----- #
class Perceptron:
	weights = {}

	# return guessed target value (1 or -1)
	def guess_target(self, inputs):
		weight_sum = 0
		all_weight_zero = True
		for idx, word in enumerate(inputs):
			if word in self.weights:
				weight_sum = weight_sum + self.weights[word]
				all_weight_zero = False
			else:
				self.weights[word] = 0
				weight_sum = weight_sum + self.weights[word]

		# if we haven't seen all the words in a line, return -1
		if (all_weight_zero):
			return -1

		return sign(weight_sum)

	# train according to the input
	def train(self, inputs):
		target = inputs[0]
		inputs = inputs[1:]
		guess_target_by_preceptron = self.guess_target(inputs)
		error = target - guess_target_by_preceptron	
		trained = False

		if (abs(error) > 0):
				trained = True

		for word in inputs:
				self.weights[word] = self.weights[word] + (error / 2)

		return trained

	# prints the weights in the perceptron weights list
	def print_weights(self):
		for word in self.weights:
			print ("%s: %s") %(word, self.weights[word])

# ----- main ----- #
def main():
	# inputs = list of tuples in the given line of the stdin
	inputs = []
	# p = Perceptron object
	p = Perceptron()
	# target = 1 or -1 depending on whether it is in category or not
	target = 0

	read_train = True
	# for each line in stdin
	while (read_train):
		for line in sys.stdin:
			if (line[0] == 'q'):
				read_train = False
				break
			else:
				line = line.split()

				# pair_input = tuple of int and list of strings
				pair_input = []
				pair_input.append(int(line[0]))

				line = line[1:]

				# append rest into the string_input
				for word in line:
					pair_input.append(word)
				
				# add pair_input to inputs
				inputs.append(pair_input)

# ----- training ----- #
	# start training
	need_train = True

	while (need_train):
		need_train = False

		entry = 0
		for input_line in inputs:
			entry = entry + 1
			if (p.train(input_line)):
				need_train = True

# ----- testing ----- #
	# starting testing
	test = True
	total_correct = 0
	total_input = 0
	while (test):
		for test_line in sys.stdin:
			# remove \n at the end of the line
			test_line = test_line[0:(len(test_line) - 1)]
			if ((len(test_line) == 0)
				or (len(test_line) == 1 and test_line[0] == 'q')):
				test = False
			else:
				total_input = total_input + 1
				test_input = []

				# split and get the target from input
				test_input = test_line.split() 
				target = int(test_input[0])
				test_input = test_input[1:]

				for index, word in enumerate(test_input):
					word = word.lstrip(string.punctuation)
					word = word.rstrip(string.punctuation)
					word = (word.lower())
					test_input[index] = word
							

				guess_by_p = p.guess_target(test_input)

				if (guess_by_p == target):
					total_correct = total_correct + 1

# ----- conclusion ----- #
	print ("Simple perceptron has guessed %s out of %s correctly" %(total_correct, total_input))
	print ("Ratio: %.2f" %(float(total_correct) / float(total_input)))


# ---------------------- #
if __name__ == "__main__":
	main()

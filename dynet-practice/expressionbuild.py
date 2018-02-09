import dynet as dy

# ==== create a new computation graph
# dy.renew_cg() clears the current one and starts anew
dy.renew_cg()

# ==== creating expressions from user input / constants
value = 5.0
dimension = 4
dim1 = 2
dim2 = 2

x = dy.scalarInput(value)

v = dy.vecInput(dimension)
v.set([1, 2, 3, 4])

# Causes deprecated error: DeprecationWarning: matInput is now deprecated. Use dynet.inputTensor instead
# z = dy.matInput(dim1, dim2)
# # for example:
# z1 = dy.matInput(2, 2)
# z1.set([1, 2, 3, 4]) # Column major

# Or directly from a numpy array
z = dy.inputTensor([[1, 2], [3, 4]]) # Row major

# ==== We can take the value of an expression
# For complex expressions, this will run forward propagation
print "\nTesting different complex expression"
print "z.value(): %s" %(z.value())
print "z.npvalue(): %s" %z.npvalue()				# as numpy array
print "v.vec_value(): %s" %v.vec_value()			# as vector, if vector
print "x.scalar_value(): %s" %x.scalar_value()		# as scalar, if scalar
print "x.value(): %s" %x.value()					# choose the correct format

# ==== Parameters
# Parameters are things we tune during training. It is usually a matrix or a vector
# e.g. weights

# First we create a parameter collection and add the parameters to it
m = dy.ParameterCollection()
pW = m.add_parameters((8, 8)) # an 8 x 8 matrix
# pb = m.add_parameters(8) # a scalar parameter

# then we create an Expression out of the paramter collection's parameters
W = dy.parameter(pW)
# b = dy.parameter(pb)

# ==== Lookup parameters
# Similar to parameters, but are representing a "lookup table"
# that maps numbers to vectors
# These are used for embedding matrices
# for example, this will have VOCAB_SIZE rows, each of DIM dimension
## lp = m.add_lookup_parameters((VOCAB_SIZE, DIM))
lp = m.add_lookup_parameters((2, 1))

# lookup parameters can be initialized from an exisiting array, i.e:
# m["Lookup"].init_from_array(wv)

e5 = dy.lookup(lp, 1)					# create an Expression from row 1
e5 = lp[1]								# same as above
e5c = dy.lookup(lp, 1, update=False) 	# as before, but don't update when optimizing

e5 = dy.lookup_batch(lp, [0, 1])		# create a batched Expression from rows 4 and 5
e5 = lp.batch([0, 1])					# same

e5.set([1])		# now the e5 expression contains row 1
e5c.set(1)		# ditto

# ==== Combine expression into complex expressions
# # Math
# e = e1 + e2
# e = e1 * e2 # for vectors/matrices: matrix multiplication 
# e = e1 - e2
# e = -e1
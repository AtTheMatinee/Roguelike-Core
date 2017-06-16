'''
randomChoice.py
'''
import random
'''
====================
Random Choice
====================

When fed a dictionary of choice:odds pairs, chooses and returns a key
'''

def choose(oddsTable):
	choices = oddsTable.keys()
	odds = oddsTable.values()

	rng = random.randint(1,sum(odds))

	runningSum = 0
	choice = 0
	for n in odds:
		runningSum += n

		if rng <= runningSum:
			return choices[choice]

		choice += 1

if __name__ == '__main__':
	test = {'result1':1,'result2':2,'result3':3,'result4':4}
	
	result1counter = 0
	result2counter = 0
	result3counter = 0
	result4counter = 0


	repeatTest = 10000
	for i in xrange(repeatTest):
		counter = choose(test)

		if counter == 'result1':
			result1counter += 1

		elif counter == 'result2':
			result2counter += 1

		elif counter == 'result3':
			result3counter += 1

		elif counter == 'result4':
			result4counter += 1

	print "result 1 = ",result1counter/float(repeatTest)
	print "result 2 = ",result2counter/float(repeatTest)
	print "result 3 = ",result3counter/float(repeatTest)
	print "result 4 = ",result4counter/float(repeatTest)
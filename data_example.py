def getTrainingData():
    return trainingData

def generateRules():
	return rules

def subsets(l):
	for i in range(2**len(l)):
		yield [l[x] for x in range(len(l)) if i & (2**x)]



trainingData = """
	Man = {Socrates; Plato; Aristotle}
	Bird = {Tweety; Tux}
	Mortal = {Socrates; Plato; Aristotle; Tweety; Tux}
	Flies = {Tweety}

"""

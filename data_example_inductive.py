def getTrainingData():
    return trainingData

def generateRules():
	return rules

def subsets(l):
	for i in range(2**len(l)):
		yield [l[x] for x in range(len(l)) if i & (2**x)]

{}

trainingData = """
	Odd = { One; Three; Five; Seven }
	Even = { Zero; Two; Four; Six }
	IsZero = { Zero }
	PlusOne = {
		Zero, One;
		One, Two;
		Two, Three;
		Three, Four;
		Four, Five;
		Five, Six;
		Six, Seven;
	}
	PlusTwo = {
		Zero, Two;
		Two, Four;
		Four, Six;
		One, Three;
		Three, Five;
		Five, Seven;
	}
"""

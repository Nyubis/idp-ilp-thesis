def getTrainingData():
    return trainingData

def generateRules():
	return rules

def subsets(l):
	for i in range(2**len(l)):
		yield [l[x] for x in range(len(l)) if i & (2**x)]

{}

trainingData = """
	Car = { Ford }
	Bike = { Minerva }
	HasWheels = {
		Ford, LeftFront;
		Ford, RightFront;
		Ford, LeftBack;
		Ford, RightBack;
		Minerva, Front;
		Minerva, Back;
	}
"""

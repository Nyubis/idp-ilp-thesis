def getTrainingData():
    return trainingData

def generateRules():
	return rules

def subsets(l):
	for i in range(2**len(l)):
		yield [l[x] for x in range(len(l)) if i & (2**x)]



trainingData = """
	num = {1..99}

	Neighbour = {
		Albania, Greece;
		Albania, Kosovo;
		Albania, Macedonia;
		Albania, Montenegro;

		Austria, Czechia;
		Austria, Germany;
		Austria, Hungary;
		Austria, Italy;
		Austria, Slovakia;
		Austria, Slovenia;
		Austria, Switzerland;

		Belarus, Latvia;
		Belarus, Lithuania;
		Belarus, Poland;
		Belarus, Russia;
		Belarus, Ukraine;

		Belgium, France;
		Belgium, Germany;
		Belgium, Netherlands;

		Bosnia, Croatia;
		Bosnia, Montenegro;
		Bosnia, Serbia;

		Bulgaria, Greece;
		Bulgaria, Macedonia;
		Bulgaria, Romania;
		Bulgaria, Serbia;

		Croatia, Bosnia;
		Croatia, Hungary;
		Croatia, Serbia;
		Croatia, Slovenia;

		Czechia, Austria;
		Czechia, Germany;
		Czechia, Hungary;
		Czechia, Poland;
		Czechia, Slovakia;

		Denmark, Germany;
		Denmark, Sweden;

		Estonia, Latvia;
		Estonia, Russia;

		Finland, Norway;
		Finland, Russia;
		Finland, Sweden;

		France, Belgium;
		France, Germany;
		France, Italy;
		France, Spain;
		France, Switzerland;

		Germany, Austria;
		Germany, Belgium;
		Germany, Czechia;
		Germany, Denmark;
		Germany, France;
		Germany, Netherlands;
		Germany, Poland;
		Germany, Switzerland;

		Greece, Albania;
		Greece, Bulgaria;
		Greece, Macedonia;

		Hungary, Austria;
		Hungary, Croatia;
		Hungary, Czechia;
		Hungary, Romania;
		Hungary, Serbia;
		Hungary, Slovakia;
		Hungary, Slovenia;
		Hungary, Ukraine;

		Ireland, United_Kingdom;

		Italy, Austria;
		Italy, France;
		Italy, Slovenia;
		Italy, Switzerland;

		Kosovo, Albania;
		Kosovo, Macedonia;
		Kosovo, Montenegro;
		Kosovo, Serbia;

		Latvia, Belarus;
		Latvia, Estonia;
		Latvia, Lithuania;
		Latvia, Russia;

		Lithuania, Belarus;
		Lithuania, Latvia;
		Lithuania, Poland;

		Macedonia, Albania;
		Macedonia, Bulgaria;
		Macedonia, Greece;
		Macedonia, Kosovo;
		Macedonia, Serbia;

		Moldova, Romania;
		Moldova, Ukraine;

		Montenegro, Albania;
		Montenegro, Bosnia;
		Montenegro, Kosovo;
		Montenegro, Serbia;

		Netherlands, Belgium;
		Netherlands, Germany;

		Norway, Finland;
		Norway, Russia;
		Norway, Sweden;

		Poland, Belarus;
		Poland, Czechia;
		Poland, Germany;
		Poland, Lithuania;
		Poland, Slovakia;
		Poland, Ukraine;

		Portugal, Spain;

		Romania, Bulgaria;
		Romania, Hungary;
		Romania, Moldova;
		Romania, Serbia;
		Romania, Ukraine;

		Russia, Belarus;
		Russia, Estonia;
		Russia, Finland;
		Russia, Latvia;
		Russia, Norway;
		Russia, Ukraine;

		Serbia, Bosnia;
		Serbia, Bulgaria;
		Serbia, Croatia;
		Serbia, Hungary;
		Serbia, Kosovo;
		Serbia, Macedonia;
		Serbia, Montenegro;
		Serbia, Romania;

		Slovakia, Austria;
		Slovakia, Czechia;
		Slovakia, Hungary;
		Slovakia, Poland;
		Slovakia, Ukraine;

		Slovenia, Austria;
		Slovenia, Croatia;
		Slovenia, Hungary;
		Slovenia, Italy;

		Spain, France;
		Spain, Portugal;

		Sweden, Denmark;
		Sweden, Finland;
		Sweden, Norway;

		Switzerland, Austria;
		Switzerland, France;
		Switzerland, Germany;
		Switzerland, Italy;

		Ukraine, Belarus;
		Ukraine, Hungary;
		Ukraine, Moldova;
		Ukraine, Poland;
		Ukraine, Romania;
		Ukraine, Russia;
		Ukraine, Slovakia;

		United_Kingdom, Ireland;
	}
	Island = {
		Cyprus;
		Iceland;
		Ireland;
		Malta;
		United_Kingdom;
	}
"""

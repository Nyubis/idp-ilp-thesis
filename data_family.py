def getTrainingData():
	return trainingData

def generateRules():
	return rules

def subsets(l):
	for i in range(2**len(l)):
		yield [l[x] for x in range(len(l)) if i & (2**x)]



trainingData = """
	Parent = {
		Albert_II, Filip;
		Paola, Filip;
		Astrid, Albert_II;
		Leopold_III, Albert_II;
		Astrid, Boudewijn;
		Leopold_III, Boudewijn;
		Albert_I, Leopold_III;
		Elisabeth, Leopold_III;
		Juliana, Beatrix;
		Bernhard, Beatrix;
		Beatrix, Willem_Alexander;
		Claus, Willem_Alexander;
		Willem_Alexander, Catharina;
		Maxima, Catharina;
	}
	Ancestor = {
		Astrid, Filip;
		Leopold_III, Filip;
		Albert_I, Filip;
		Elisabeth, Filip;
		Albert_I, Boudewijn;
		Elisabeth, Boudewijn;
		Albert_I, Albert_II;
		Elisabeth, Albert_II;
		Albert_II, Filip;
		Paola, Filip;
		Astrid, Albert_II;
		Leopold_III, Albert_II;
		Astrid, Boudewijn;
		Leopold_III, Boudewijn;
		Albert_I, Leopold_III;
		Elisabeth, Leopold_III;
		Juliana, Beatrix;
		Juliana, Willem_Alexander;
		Juliana, Catharina;
		Bernhard, Beatrix;
		Bernhard, Willem_Alexander;
		Bernhard, Catharina;
		Beatrix, Willem_Alexander;
		Beatrix, Catharina;
		Claus, Willem_Alexander;
		Claus, Catharina;
		Willem_Alexander, Catharina;
		Maxima, Catharina;
	}
"""

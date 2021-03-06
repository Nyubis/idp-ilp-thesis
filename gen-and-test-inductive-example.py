#!/usr/bin/python3
import data_example_inductive as dummy
from refiner import *
import subprocess
import threading
import queue
import re

filename = "tmp%d.idp"
timeout = 2

def main():
	odd = Pred("Odd", 1)
	even = Pred("Even", 1)
	iszero = Pred("IsZero", 1)
	plustwo = Pred("PlusTwo", 2)
	refiner = Refiner(odd, even, iszero, plustwo)
	refiner.max_atoms = 2
	refiner.do_aggregates = False
	refiner.do_inductive_definitions = True
	rules = [refiner.generate_rule(1)] # the 1 means we try to define even, the first predicate.
	foundRules = 0
	index = 0
	checked_rules = set()
	while foundRules < 5:
		res_queue = queue.Queue()
		threads = []
		for i, rule in enumerate(rules):
			if str(rule) in checked_rules:
				continue
			checked_rules.add(str(rule))
			if checkTautology(rule):
				continue
			training_data = dummy.getTrainingData()
			approx = rule.copy()
			approx.setApproximate(True)
			_index = len(refiner.generated_rules) - len(rules) + i # terrible hack to get this rule's index in generated_rules
			t = threading.Thread(target=checkRule,
					args=(res_queue, _index, approx, training_data))
			print("[%d] Testing %s" % (_index, str(rule)))
			t.start()
			threads.append(t)

		# wait until all threads have finished
		for t in threads:
			t.join()
		while not res_queue.empty():
			i, rule, accuracy = res_queue.get()
			if accuracy > 0.7:
				foundRules += 1
				print("Potential rule found: (%d %% accuracy)" % (accuracy*100))
				print('[%d] %s' % (i, str(rule)), end="\n*********\n")
		rules = refiner.specialize(index)
		index+=1

def checkRule(result_queue, index, rule, training_data):
	fname = filename % index
	with open(fname, 'w') as f:
		f.write(skeleton % (rule, training_data))
	try:
		output = subprocess.check_output(['idp', fname], timeout=timeout,
				universal_newlines=True, stderr=subprocess.DEVNULL)
	except subprocess.TimeoutExpired:
		result_queue.put((index, rule, 0))
		return

	hit = re.search("Correct = { (.*) }", output).group(1)
	missed = re.search("Different = { (.*) }", output).group(1)
	hitcount = 0 if hit == '' else len(hit.split("; "))
	misscount = 0 if missed == '' else len(missed.split("; "))
	accuracy = (2 * hitcount) / (2 * hitcount + misscount)
	result_queue.put((index, rule, accuracy))

# Check whether a rule is a tautology, e.g. p(x) <- p(x)
# These rules are obvious and do not actually need to be tested
def checkTautology(r):
	h = r.head_atom
	for t in r.body_atoms:
		if t.name == h.name and t.variables == h.variables:
			return True
	return False

skeleton = """
vocabulary V {
	type Number constructed from {Zero, One, Two, Three, Four, Five, Six, Seven}
	IsZero(Number)
	Odd(Number)
	Even(Number)
	PlusOne(Number, Number)
	PlusTwo(Number, Number)
	ApproxEven(Number)
	Different(Number)
	Correct(Number)
}

theory T: V {
	{
		%s
		! x: Different(x) <- (ApproxEven(x) & ~Even(x)) | (~ApproxEven(x) & Even(x)).
		! x : Correct(x) <- ApproxEven(x) & Even(x).
	}
}

structure S:V {
	%s
}

procedure main() {
	printmodels(modelexpand(T,S))
}
"""

if __name__=='__main__':
	main()

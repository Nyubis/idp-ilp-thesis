#!/usr/bin/env python3
import random
import string
import math
from itertools import combinations

# predicate class, when placed in a rule may also represent an atom
class Pred():
	def __init__(self, name="", arity=0, variables=[]):
		self.name = name
		self.arity = arity
		self.variables = variables
	def __str__(self):
		return "%s(%s)" % (self.name, ", ".join(self.variables))
	def copy(self):
		return Pred(self.name, self.arity, self.variables)

# this represents a cardinality aggregate applied to an atom, has Pred in the name because the structure is really similar to the above
# looks like e.g. "#{x : P(a, x)} < n" when __str__ is called.
class CardPred(Pred):
	def __init__(self, name, arity, variables, inner_vars, cons):
		super().__init__(name, arity, variables)
		self.inner_vars = inner_vars
		self.cons = cons
	def __str__(self):
		return "#{%s : %s(%s)} < %d" % (", ".join(self.inner_vars),
				self.name, ", ".join(self.variables), self.cons)
	def copy(self):
		return CardPred(self.name, self.arity, self.variables, self.inner_vars, self.cons)

# rule of the form e.g. ∀x,y: P(x, y) ← ∃ z: Q(z, x).
class Rule():
	def __init__(self):
		self.universal_vars = []
		self.existential_vars = []
		self.used_vars = [] # more than just the sum of universal and existential, also contains vars that were unified away
		self.unification_pointers = ('a', 'a') # means that var a can be unified with anything that comes after a; we remember this to avoid getting to the same unification twice from different brances
		self.head_atom = Pred()
		self.body_atoms = []
		self.disjunct_body_atoms = [] # only used when refiner.do_inductive_definitions is True
		self.final = False
		self._approx_string = "Approx" # used for generating the idp code where we check our hypothesis vs. the data, hypotheses get Approx prefix
		self.parent = ""
	def __str__(self):
		builder = ""
		if len(self.universal_vars) > 0:
			builder += "! %s: " % " ".join(self.universal_vars)
		builder += str(self.head_atom) + " <- "
		if len(self.existential_vars) > 0:
			builder += "? %s: " % " ".join(self.existential_vars)
		builder += "%s" % " & ".join(map(str, self.body_atoms))
		if len(self.disjunct_body_atoms) > 0:
			builder += " | %s" % " & ".join(map(str, self.disjunct_body_atoms))
		builder += "."
		return builder
	# used for testing our hypothesis vs data, predicate names in hypothesis get Approx prefix
	# parameter yes=True means we include the prefix, False means we remove it
	def setApproximate(self, yes):
		if yes and not self.head_atom.name.startswith(self._approx_string):
			pred_name = self.head_atom.name
			self.head_atom.name = self._approx_string + pred_name
			for t in filter(lambda x: x.name == pred_name, self.body_atoms):
				t.name = self._approx_string + pred_name
		elif not yes and self.head_atom.name.startswith(self._approx_string):
			approx_pred_name = self.head_atom.name
			self.head_atom.name = approx_pred_name[:len(self._approx_string)]
			for t in filter(lambda x: x.name == approx_pred_name, self.body_atoms):
				t.name = self.head_atom.name

	def copy(self):
		r = Rule()
		r.universal_vars = self.universal_vars.copy()
		r.existential_vars = self.existential_vars.copy()
		r.used_vars = self.used_vars.copy()
		r.head_atom = self.head_atom.copy()
		r.body_atoms = list(map(lambda x: x.copy(), self.body_atoms))
		r.disjunct_body_atoms = list(map(lambda x: x.copy(), self.disjunct_body_atoms))
		r.parent = self.parent
		return r

class Refiner():
	# these are defaults, any script that instantiates a refiner will probably overwrite them
	predicates = []
	generated_rules = []
	max_atoms = 999
	cardinality_constant = 3 # used for cardinality aggregates, the value that "n" in the example above starts at
	do_aggregates = True
	do_inductive_definitions = False

	def __init__(self, *preds):
		self.preds = preds
	def generate_rule(self, index=0):
		r = Rule()
		r.head_atom = self.preds[index].copy()
		r.universal_vars = get_free_vars([], r.head_atom.arity)
		r.used_vars = r.universal_vars.copy()
		r.head_atom.variables = r.universal_vars.copy()
		self._add_atom(r)
		self.generated_rules = [r]
		return r

	def specialize(self, index):
		r = self.generated_rules[index]
		# Rules that are final don't need to be specialized further
		if r.final:
			return []
		# Specilazation 1: add an atom to the body
		if len(r.body_atoms) < self.max_atoms:
			more_atoms = self._add_atom(r)
		else:
			more_atoms = []
		# Specialization 2: unify two variables
		less_vars = self._unify_vars(r)
		# Specialization 3: apply the bias to an atom so it counts matching elements
		if self.do_aggregates:
			cardinalized = self._cardinalize(r)
		else:
			cardinalized = []
		# Specialization 4: add a disjunction with some more atoms so inductive definitions can work
		if self.do_inductive_definitions \
				and len(r.disjunct_body_atoms) < self.max_atoms \
				and r.head_atom.name in map(lambda x: x.name, r.body_atoms):
			disjunctive = self._add_disjunct_atom(r)
		else:
			disjunctive = []

		# add them all together
		self.generated_rules.extend(more_atoms)
		self.generated_rules.extend(less_vars)
		self.generated_rules.extend(cardinalized)
		self.generated_rules.extend(disjunctive)
		return more_atoms + less_vars + cardinalized + disjunctive

	def _add_atom(self, rule):
		if rule.unification_pointers != ('a', 'a'):
			return []
		results = []
		pred_order = list(map(lambda x: x.name, self.preds))
		order_index = 0
		if len(rule.body_atoms) > 0:
			# order_index is to find which predicates are ordered later than this one so we don't create dupes
			# we want to avoid P(…) & A(…) in addition to A(…) & P(…)
			order_index = pred_order.index(rule.body_atoms[-1].name)
		# iterate through a copy of the predicates that come after order_index
		for pred in map(lambda x: x.copy(), self.preds[order_index:]):
			r = rule.copy()
			new_vars = get_free_vars(r.used_vars, pred.arity)
			pred.variables = new_vars
			r.existential_vars += new_vars
			r.used_vars += new_vars
			r.body_atoms.append(pred) # this predicate is effectively an atom now
			r.parent = str(rule)
			results.append(r)
		return results
	def _add_disjunct_atom(self, rule):
		# this is like _add_atom, but adds the atom to the disjunct body instead, i.e. it comes after the ∨
		results = []
		target_preds = filter(lambda x: x.name != rule.head_atom.name, self.preds)
		for pred in map(lambda x: x.copy(), target_preds):
			r = rule.copy()
			pred.variables = (r.universal_vars + r.existential_vars)[:pred.arity]
			r.disjunct_body_atoms.append(pred)
			r.parent = str(rule)
			results.append(r)
		return results
	def _unify_vars(self, rule):
		results = []
		for v, w in combinations(rule.universal_vars + rule.existential_vars, 2):
			if (v, w) < rule.unification_pointers:
				continue # this should have been covered in a previous branch of the lattice, don't do the same work twice.
			r = rule.copy()
			# unify v and w, in other words:
			# replace the variable w by v

			#replacing in the quantifiers ! and ?
			if w in r.universal_vars:
				r.universal_vars.remove(w)
				# if v was only existential and we removed the w in universal, we need to move the existential v to universal
				if v in r.existential_vars:
					r.existential_vars.remove(v)
					r.universal_vars.append(v)
			if w in r.existential_vars:
				r.existential_vars.remove(w)

			# replacing in the atoms
			repl = lambda x: v if x == w else x
			for atom in (r.body_atoms + r.disjunct_body_atoms + [r.head_atom]):
				atom.variables = list(map(repl, atom.variables))

			r.unification_pointers = (v, w)
			r.parent = str(rule)
			results.append(r)
		return results

	def _cardinalize(self, rule):
		# transform an atom into a cardinality aggregate of this predicate
		results = []
		for a_i, a in enumerate(filter(lambda x: type(x) != CardPred, rule.body_atoms)):
			for v_i, v in enumerate(a.variables):
				if v in rule.universal_vars or v in [x for atom in rule.body_atoms if atom != a for x in atom.variables]:
					# we only want to do this for existential vars that are unique to this atom
					# so, continue otherwise
					continue
				othervars = a.variables[:v_i] + a.variables[v_i+1:]
				card_atom = CardPred(a.name, a.arity, a.variables, [v], self.cardinality_constant)
				r = rule.copy()
				r.body_atoms[a_i] = card_atom
				r.existential_vars.remove(v)
				r.final = True
				r.parent = str(rule)
				results.append(r)
		return results

	def vary_constants(self, index):
		# Specialization on rules with a cardinality, vary the cardinality constant
		# to potentially discover more precise results
		rule = self.generated_rules[index]
		results = []
		for i, a in enumerate(rule.body_atoms):
			if type(a) == CardPred:
				rule_more = rule.copy()
				rule_less = rule.copy()
				rule_more.body_atoms[i].cons += 1
				rule_less.body_atoms[i].cons -= 1
				results.extend([rule_more, rule_less])
		self.generated_rules.extend(results)
		return results



def get_free_vars(used, n):
	# no safety for when we run out yet...
	return list(filter(lambda x: x not in used, string.ascii_lowercase))[:n]

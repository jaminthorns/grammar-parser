from Symbols import *
from ProductionRule import *

class ContextFreeGrammar():
	"""Represents a context-free grammar."""
	
	def __init__(self, nonterminals, terminals, rules, start):
		# List of Nonterminal objects
		self.nonterminals = nonterminals
		# List of Terminal objects
		self.terminals = terminals
		# List of Rule objects
		self.rules = rules
		# Nonterminal that is this language's start symbol
		self.start = start
	
	def __str__(self):
		"""Return a readable string representation of this grammar."""
		string = ""
		
		for nonterminal in self.nonterminals:
			string += str(nonterminal) + " -> "
			
			rules = self.getRules(nonterminal)
			
			for rule in rules:
				for symbol in rule.RHS:
					string += str(symbol)
				
				if rule is not rules[-1]:
					string += " | "
			
			if nonterminal is not self.nonterminals[-1]:
				string += "\n"
		
		return string
	
	def __repr__(self):
		"""Return a parsable string representation of this grammar."""
		string = ""
		
		for nonterminal in self.nonterminals:
			string += repr(nonterminal) + " ::="
			
			rules = self.getRules(nonterminal)
			
			for rule in rules:
				for symbol in rule.RHS:
					string += " " + repr(symbol)
				
				if rule is not rules[-1]:
					string += " |"
			
			if nonterminal is not self.nonterminals[-1]:
				string += "\n"
		
		return string
	
	def getRules(self, nonterminal):
		"""Return a list of rules associated with a nonterminal."""
		rules = []
		
		for rule in self.rules:
			if nonterminal == rule.LHS:
				rules.append(rule)
		
		return rules
	
	def derive(self, string, separator=""):
		"""Derive a string using this grammar.
		
		string -- the string to derive using this grammar
		separator -- the token used to separate symbols in string (default None)
		"""
		if separator:
			string = string.split(separator)
		
		# Transform the input string into a sentential form
		string = [Terminal(symbol) for symbol in string] if string else [Terminal("")]
		derivation = []
		
		# Derive the string if possible
		success = self._derive(string, [self.start], derivation, 0, 0)
		
		return [[self.start]] + list(reversed(derivation)) if success else None
	
	def _derive(self, string, prediction, derivation, current, recursion):
		"""Recursive algorithm to derive a string using this grammar.
		
		string -- the string to derive using this grammar
		prediction -- the current prediction for the string
		derivation -- list of sentential forms making up the leftmost derivation
		current -- the position in string and prediction
		recursion -- the depth of recursion while deriving left recursive rules
		"""
		# String derived
		if string == prediction:
			return True
		# String not derived, backtrack
		elif current >= len(prediction) or recursion > len(string):
			return False
		
		# Current symbol matches, increment current position
		if current < len(string) and prediction[current] == string[current]:
			return self._derive(string, prediction, derivation, current + 1, recursion)
		# Current symbol in prediction is a nonterminal
		elif isinstance(prediction[current], Nonterminal):
			for rule in self.rules:
				# Derive nonterminal in the current position
				if prediction[current] == rule.LHS:
					# Create new prediction by deriving current rule
					newPrediction = list(prediction)
					newPrediction[current:current + 1] = rule.RHS
					
					# Remove the lambda if present
					hasLambda = rule.RHS[0] == Terminal("") and len(prediction) > 1
					originalPrediction = list(newPrediction)
					
					if hasLambda:
						newPrediction.remove(Terminal(""))
					
					# Increment recursion if current rule is left recursive
					newRecursion = recursion + 1 if rule.recursive else recursion
					
					derived = self._derive(string, newPrediction, derivation, current, newRecursion)
					
					if derived:
						# Add sentential form to derivation
						derivation.append(newPrediction)
						
						# Add sentential form with lambda if necessary
						if hasLambda:
							derivation.append(originalPrediction)
						
						return derived
		
		# String not derived, backtrack
		return False
	
	def setRecursive(self):
		"""Find and mark all of the left recursive rules in this grammar."""
		recursive = []
		
		# Get the set of possible left recursive rules
		for nonterminal1 in self.nonterminals:
			for nonterminal2 in self.nonterminals:
				for rule in self.rules:
					if rule.LHS == nonterminal1 and rule.RHS[0] == nonterminal2:
						recursive.append(rule)
		
		# Mark all of the left recursive rules
		for rule in recursive:
			self._setRecursive(rule, rule, recursive)
	
	def _setRecursive(self, start, rule, recursive):
		"""Recursive algorithm to find left recursive rules.
		
		start -- the starting rule of the recursive loop
		rule -- the current rule of the recursive loop
		recursive -- the list of possible left recursive rules
		"""
		# Exit the recursive loop if the rule is already recursive
		if rule.recursive:
			return
		
		# Recursive loop is completed, mark start rule as recursive and exit
		if start.LHS == rule.RHS[0]:
			start.recursive = True
			return
		
		# Continue along recursive loop
		for newRule in recursive:
			if newRule.LHS == rule.RHS[0]:
				return self._setRecursive(start, newRule, recursive)
	
	@staticmethod
	def readGrammar(filename):
		"""Read a context-free grammar (in Backus-Naur Form) from a file."""
		input = open(filename)
		lines = [line.strip() for line in input.readlines()]
		input.close()
		
		rules = []
		nonterminals = []
		terminals = []
		
		# Parse all of the production rules
		for line in lines:
			# Strip out comments
			if ";" in line:
				line = line.split(";")[0]
			
			# Skip blank lines
			if line == "":
				continue
			
			left = line.split(" ::= ")[0]
			right = line.split(" ::= ")[1].split("|")
			
			# Parse the left-hand side of the rule(s)
			LHS = Nonterminal(left.strip("<>"))
			
			# Parse the right-hand side of the rule(s)
			for rule in right:
				RHS = []
				
				for symbol in rule.split():
					if "\"" in symbol:
						RHS.append(Terminal(symbol.strip("\"")))
					elif "<" in symbol:
						RHS.append(Nonterminal(symbol.strip("<>")))
				
				rules.append(ProductionRule(LHS, RHS))
		
		# Get the nonterminals
		for rule in rules:
			if rule.LHS not in nonterminals:
				nonterminals.append(rule.LHS)
		
		# Get the terminals
		for rule in rules:
			for symbol in rule.RHS:
				if symbol not in terminals and symbol not in nonterminals:
					terminals.append(symbol)
		
		# Get the start symbol
		start = rules[0].LHS
		
		# Create new grammar and mark left recursive rules
		grammar = ContextFreeGrammar(nonterminals, terminals, rules, start)
		grammar.setRecursive()
		
		return grammar
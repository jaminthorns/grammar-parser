class ProductionRule():
	"""Represents a production rule in a context-free grammar."""
	
	def __init__(self, LHS, RHS):
		# Nonterminal representing the left-hand side of this production rule
		self.LHS = LHS
		# List of Symbols that represent the right-hand side of this rule
		self.RHS = RHS
		# Boolean indicating whether this rule is left recursive
		self.recursive = self.LHS == self.RHS[0]
	
	def __str__(self):
		"""Return a readable string representation of this production rule."""
		return str(self.LHS) + " -> " + "".join([str(symbol) for symbol in self.RHS])
	
	def __repr__(self):
		"""Return a parsable string representation of this production rule."""
		return repr(self.LHS) + " ::=" + "".join([" " + repr(symbol) for symbol in self.RHS])
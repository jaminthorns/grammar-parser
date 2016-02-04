class Symbol():
	"""Abstract class for Nonterminal and Terminal classes."""
	
	def __init__(self, symbol):
		# String that represents this Symbol
		self.symbol = symbol
	
	def __str__(self):
		"""Return a readable string representation of this symbol."""
		return self.symbol if self.symbol != "" else "_"
	
	def __eq__(self, symbol):
		"""Test whether this symbol and another symbol are equal."""
		return self.symbol == symbol.symbol and self.__class__ == symbol.__class__

class Nonterminal(Symbol):
	"""Represents a nonterminal symbol of a context-free grammar."""
	
	def __repr__(self):
		"""Return a parsable string representation of this symbol."""
		return "<" + self.symbol + ">"

class Terminal(Symbol):
	"""Represents a terminal symbol of a context-free grammar."""
	
	def __repr__(self):
		"""Return a parsable string representation of this symbol."""
		return "\"" + self.symbol + "\""
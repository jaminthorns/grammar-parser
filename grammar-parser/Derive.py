import sys
from ContextFreeGrammar import *

def readFile(filename):
	"""Read the context-free grammar from an input file with error checking."""
	try:
		return ContextFreeGrammar.readGrammar(filename)
	except IOError:
		print("Error: The file \"{}\" does not exist".format(filename))
	except Exception:
		print("Error: There is something wrong with the grammar in the file \"{}\"".format(filename))

# Read the grammar from an input file
if len(sys.argv) == 2:
	grammar = readFile(sys.argv[1])
	
	if not grammar:
		exit()
else:
	success = False
	
	while not success:
		filename = input("Enter a file containing a context-free grammar (press Enter to quit): ")
		
		if not filename:
			exit()
		
		grammar = readFile(filename)
		
		if grammar:
			success = True

# Display the grammar
print("\n", grammar, "\n", sep="")

# Derive strings from the grammar
while True:
	string = input("String to be derived (type \"_\" for lambda or press Enter to quit): ")
	
	if not string:
		exit()
	elif string == "_":
		string = ""
	
	separator = input("Separator that divides terminals (press Enter for none): ") if len(string) > 1 else ""
	
	derivation = grammar.derive(string, separator)
	
	print()
	
	if derivation:
		print(" => ".join([separator.join([str(symbol) for symbol in form]) for form in derivation]))
	else:
		print("The string \"" + string + "\"" if string else "Lambda", "is not derivable from this grammar.")
	
	print()
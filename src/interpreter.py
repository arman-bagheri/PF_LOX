from .loxast import *
from .lexer import *
from .parser import *



def run(script):

	hadError = lex(script)

	if hadError:
		print("Fix Lexical errors before continuing.")
		exit()

	try:
		program()

	except SyntaxException:
		print("Syntax error(s) found. Fix them before execution")
		return


	for node in stmtList:
		try:
			node.interpret()
		except RuntimeException:
			print("Runtime exception, error handling not yet good.")
			exit()	


	print("-- The End --")	


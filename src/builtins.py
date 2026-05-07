from .lexer import token

class BuiltinFunction:
	pass

class Println(BuiltinFunction):
	def __init__(self):
		self.argcount = 1
		self.parentenv = curEnv
		self.parameters = [token("IDENTIFIER", "x", None, None)]
	def interpret(self):
		print(getValue("x"))

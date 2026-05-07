from .lexer import token

class BuiltinFunction:
	pass

class Println(BuiltinFunction):
	def __init__(self):
		self.argcount = 1
		self.parentenv = curEnv
		self.parameters = [token("IDENTIFIER", "x", None, None)]
	def interpret(self):
		val = getValue("x")
		if val==None:
			print("nil")
		elif type(val) == FunctionValue:
			print("Function type.")
		else:
			print(value)

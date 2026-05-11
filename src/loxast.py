from .lexer import *
from .environment import *
import pdb


stmtList = []

#
#	values in lox
#		float numbers		-> float number
#		strings				-> strings
#		true and false		-> True and False
#		nil					->    None
#		functions 			-> FunctionValue
#		array				-> list
#	only nil and false ara falsy rest are truthy


def isFalsy(value):
	if(value == False or value == None):
		return True
	return False	

# Environment functions


##


class AstNode:
	pass


class ReturnNode(AstNode):
	def __init__(self, expr, token):
		self.expr = expr
		self.token = token
	def interpret(self):
		if envStack == []:
			getMessage("Return statement outside a function.", self.token.line)
			raise RuntimeException
		self.expr.evaluate()
		raise Return(self.expr.value)



class FunctionNode(AstNode):
	def __init__(self, idToken, parameters, stmts):
		self.stmts = stmts
		self.id = idToken
		self.parameters = parameters
		self.argcount = len(self.parameters)

	def interpret(self):
		function = FunctionValue(self.parameters, self.stmts)
		function.evaluate()
		getEnv()[self.id.text] = function
		#printEnv()

class WhileNode(AstNode):
	def __init__(self, expr, stmtnode):
		self.expr = expr
		self.stmtnode = stmtnode
	def interpret(self):
		self.expr.evaluate()
		while not isFalsy(self.expr.value):
			self.stmtnode.interpret()
			self.expr.evaluate()

class IfNode(AstNode):
	def __init__(self, expr, stmtnode, elsenode):
		self.expr = expr
		self.stmtnode = stmtnode
		self.elsenode = elsenode
	def interpret(self):
		self.expr.evaluate()
		if not isFalsy(self.expr.value):
			self.stmtnode.interpret()
		elif self.elsenode != None:
			self.elsenode.interpret()			

class ExpressionNode(AstNode):
	def __init__(self, expr):
		self.expr = expr

	def interpret(self):
		self.expr.evaluate()
		#print(self.expr.value)

class BlockNode(AstNode):
	def __init__(self):
		self.stmts = []
	def interpret(self):
		newEnv = Environment(getEnv())
		setEnv(newEnv)
		for stmt in self.stmts:
			stmt.interpret()
		setEnv(newEnv.parent)

class VarDecNode(AstNode):
	def __init__(self, var, initexpr):
		self.var = var
		self.initexpr = initexpr
	def interpret(self):
		
		if self.initexpr == None:
			defVariable(self.var.token.text, None)
		
		else:	
			self.initexpr.evaluate()
			defVariable(self.var.token.text, self.initexpr.value)





#EXPRESSION AST NODES

class Expression:
	pass


class Call(Expression):
	def __init__(self, kallable, arglist, token):
		self.kallable = kallable
		self.arglist = arglist
		self.token = token
	def evaluate(self):	

		for expr in self.arglist:
			expr.evaluate()
		self.kallable.evaluate()
		if type(self.kallable.value) != FunctionValue and not isinstance(self.kallable.value, BuiltinFunction):
			print("Token is not callable.", self.token.line)
			raise RuntimeException

		function = self.kallable.value
		
		#arity check
		if len(self.arglist) != function.argcount:
			print("arity error.", self.kallable.token.line)
			raise RuntimeException

		## setting up parameters in the environment
		self.env = Environment(function.closure)
		i = 0
		while i < len(self.arglist):
			self.env[function.parameters[i].text] = self.arglist[i].value
			i += 1


		switchEnv(self.env)


		## calling the function
		if isinstance(function, BuiltinFunction):
			try:
				function.interpret()
			except Return as e:
				self.value = e.value
				returnEnv()	
		else:
			try:
				for stmt in function.stmts:
					stmt.interpret()
				self.value = None
				returnEnv()
			except Return as e:
				self.value = e.value
				returnEnv()
	



class Binary(Expression):
	def __init__(self, left, token, right):
	
		self.right = right
		self.token = token
		self.left = left
	
	def evaluate(self):
		
		self.right.evaluate()
		temp = self.right.value
		self.left.evaluate()
		self.right.value = temp


		if self.token.type == tokenType["EQUAL_EQUAL"]:
			self.value = (self.left.value == self.right.value)

		elif self.token.type == tokenType["BANG_EQUAL"]:
			self.value = (self.left.value != self.right.value)
	
		elif self.token.type == tokenType["EQUAL"]:
			self.value = self.right.value
			setValue(self.left.token.text, self.value)
	
		elif self.token.type == tokenType["OR"]:
			self.value = not (isFalsy(self.left.value) and isFalsy(self.right.value))
	
		elif self.token.type == tokenType["AND"]:
			self.value = not (isFalsy(self.left.value) or isFalsy(self.right.value))


		elif type(self.right.value) != float or type(self.left.value) != float:
			print("Type error at " + str(self.expr.token.line))
			raise RuntimeException

		if self.token.type == tokenType["PLUS"]:
			self.value = self.right.value + self.left.value

		elif self.token.type == tokenType["MINUS"]:
			self.value = self.left.value - self.right.value
		
		elif self.token.type == tokenType["STAR"]:
			self.value = self.left.value * self.right.value

		elif self.token.type == tokenType["SLASH"]:
			self.value = self.left.value / self.right.value

		elif self.token.type == tokenType["LESS"]:
			self.value = (self.left.value < self.right.value)

		elif self.token.type == tokenType["LESS_EQUAL"]:
			self.value = (self.left.value <= self.right.value)

		elif self.token.type == tokenType["GREATER"]:
			self.value = (self.left.value > self.right.value)

		elif self.token.type == tokenType["GREATER_EQUAL"]:
			self.value = (self.left.value >= self.right.value)


class Unary(Expression):
	def __init__(self, token, expr):
		self.token = token
		self.expr = expr
	def evaluate(self):	
		self.expr.evaluate()
	
		if self.token.type == tokenType["BANG"]:	
			self.value = isFalsy(self.expr.value)
	
		elif type(self.expr.value) != float:
			print("Type error at " + str(self.expr.token.line))
			raise RuntimeException

		elif self.token.type == tokenType["MINUS"]:	  
			self.value = - self.expr.value

class Literal(Expression):

	def __init__(self, token):
		self.token = token

	def evaluate(self):
		self.value = self.token.literal	


class Variable(Expression):

	def __init__(self, token):
		self.token = token

	def evaluate(self): 
		try:
			val = getValue(self.token.text)
			self.value = val
		except UndefinedVar:
			print("Undefined variable " + self.token.text + " at: " + str(self.token.line))
			raise RuntimeException

class Grouping(Expression):

	def __init__(self, expr):
		self.expr = expr

	def evaluate(self):
		self.expr.evaluate()
		self.value = self.expr.value



class FunctionValue(Expression):
	def __init__(self, parameters, stmts):
		self.stmts = stmts
		self.parameters = parameters
		self.argcount = len(parameters)
	def __str__(self):
		return "<Function Type>"

	def evaluate(self):
		self.closure = getEnv()
		self.value = self


class ArrayValue(Expressison):
	def __init__(self, exprs):
		self.exprs = exprs
	def __str__(self):
		string = "["
		for v in self.values:
			if(type(v)==FunctionValue):
				string += ", " + v.__str__()
			elif(type(v)==ArrayValue):
				string += ", " + v.__str__()
			elif(v==None):
				string += ", nil"
			else:
				string += str(v)
		return string	
	def evaluate(self):
		self.values = []
		for expr in self.exprs:
			expr.evaluate()
			self.values.append(expr.value)
		self.value = self		


## builtin functions

class BuiltinFunction:
	pass

class Println(BuiltinFunction):
	def __init__(self):
		self.argcount = 1
		self.closure = getEnv()
		self.parameters = [token("IDENTIFIER", "x", None, None)]
	def interpret(self):
		val = getValue("x")
		if val==None:
			print("nil")
		else:
			print(val)
		raise Return(None)	



defVariable("println", Println())


###


class ENVNODE(AstNode):
	def interpret(self):
		printEnv()

def printEnv():
	temp = getEnv()
	print("****LOG:****")
	print("current environment:")
	print(temp)
	print("parents:")
	while temp.parent!=None:
		temp = temp.parent
		print(temp)
	print("the stack:")
	print(envStack)
	print("****End****")
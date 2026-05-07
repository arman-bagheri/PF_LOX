
class UndefinedVar(Exception):
	pass

class SyntaxException(Exception):
	pass

class RuntimeException(Exception):
	pass


class Return(Exception):
	def __init__(self, value):
		self.value = value





envStack = []


class Environment(dict):
	def __init__(self, parent):
		super()
		self.parent = parent

curEnv = Environment(None)


def getEnv():
	global curEnv
	return curEnv

def setEnv(env):
	global curEnv
	curEnv = env


def switchEnv(env):
	global curEnv
	envStack.append(curEnv)
	curEnv = env

def returnEnv():
	global curEnv
	curEnv = envStack.pop()

def getValue(name):
	global curEnv
	tempEnv = curEnv
	while True:
		try:
			value = tempEnv[name]
			return value
		except KeyError:
			if tempEnv.parent == None:
				raise UndefinedVar		
		tempEnv = tempEnv.parent

def setValue(name, value):
	global curEnv
	tempEnv = curEnv
	while True:
		try:
			testing = tempEnv[name]
			tempEnv[name] = value
			return
		except KeyError:
			if tempEnv.parent == None:
				raise UndefinedVar	
		tempEnv = tempEnv.parent


def defVariable(name, value):
	curEnv[name] = value
from .loxast import *
from .lexer import *

current = 0

def sync():
	
	if matchToken("EOF"):
		return

	elif matchToken("SEMICOLON"):
		advance()
		return
	
	elif matchToken("CLASS"):
		return
	
	elif matchToken("FUN"):
		return

	elif matchToken("VAR"):
		return

	elif matchToken("FOR"):
		return	

	elif matchToken("WHILE"):
		return

	elif matchToken("RETURN"):
		return		

	elif matchToken("IF"):
		return

	else:
		advance()
		sync()
		return	


def program():
	global current
	current = 0
	syntaxError = False
	while not matchToken("EOF"):
		try:
			node = statement()
			stmtList.append(node)
		except SyntaxException:
			syntaxError = True
			sync()
	if syntaxError:
		raise SyntaxException
		

def statement():
	if matchToken("VAR"):
		return varStmt()
	elif matchToken("LEFT_BRACE"):
		return blockStmt()
	elif matchToken("IF"):
		return ifStmt()
	elif matchToken("WHILE"):
		return whilestmt()
	elif matchToken("FOR"):
		return forstmt()
	elif matchToken("ENV"):
		advance()
		return ENVNODE()
	elif matchToken("FUN"):
		return funcDecl()
	elif matchToken("RETURN"):
		return returnstmt()	
	else:
		return expressionStmt()

def returnstmt():
	advance()
	token = tokenList[current-1]
	expr = expression()
	consume("SEMICOLON", "Expected semicolon at the end of return statement")
	return ReturnNode(expr, token)




def funcDecl():
	advance()
	consume("IDENTIFIER", "Missing function name at function declaration statement.")
	funcId = tokenList[current-1]
	consume("LEFT_PAREN", "Missing left parenthesis at function declaration.")
	#parameters
	paramList = []
	while(matchToken("IDENTIFIER")):
		paramList.append(tokenList[current])
		advance()
		if matchToken("RIGHT_PAREN"):
			break
		consume("COMMA", "Missing comma after parameter identifier.")
	consume("RIGHT_PAREN", "Missing right parenthesis at function declaration.")
	#the block
	blocknode = blockStmt()

	return FunctionNode(funcId, paramList, blocknode.stmts) 

def forstmt():	#rewrite this one
	advance()


	initializer = None  #var declaration or expression statement
	condition = None    #expression
	increment = None    #expression
	consume("LEFT_PAREN", "Missing left parenthesis before for loop expressions")

	if matchToken("VAR"):
		initializer = varStmt()
	elif matchToken("SEMICOLON"):
		advance()	
	else:
		initializer = expressionStmt()

	if not matchToken("SEMICOLON"):
		condition = expression()
		consume("SEMICOLON", "Missing semicolon after condition expression in for loop")
	else:
		advance()

	if not matchToken("SEMICOLON"):
		increment = expression()
		increment = ExpressionNode(increment)
	else:
		advance()

	consume("RIGHT_PAREN", "Missing right parenthesis after for loop expressions")
	stmtnode = statement()


	myblock = BlockNode()
	myblock.stmts.append(stmtnode)
	if increment != None:
		myblock.stmts.append(increment)

	if initializer != None:
		stmtList.append(initializer)

	if condition == None:
		condition = Literal("TRUE", "true", True, 0)


	whilestmt = WhileNode(condition, myblock)

	block = BlockNode()
	block.stmts.append(whilestmt)
	return whilestmt


def whilestmt():
	advance()
	consume("LEFT_PAREN", "missing left parenthesis befor while expression")
	expr = expression()
	consume("RIGHT_PAREN", "missing right parenthesis after while expression")
	stmtnode = statement()
	return WhileNode(expr, stmtnode)

def ifStmt():
	advance()
	consume("LEFT_PAREN", "Missing left parenthesis for if statement expression.")
	expr = expression()
	consume("RIGHT_PAREN", "Missing right parenthesis for if statement expression.")
	stmtnode = statement()
	elsenode = None
	if matchToken("ELSE"):
		advance()
		elsenode = statement()
	return IfNode(expr, stmtnode, elsenode)

def blockStmt():
	advance()
	block = BlockNode()
	while not matchToken("RIGHT_BRACE") and not matchToken("EOF"):
		block.stmts.append(statement())
	consume("RIGHT_BRACE", "Missing right braces at the end of a block.")
	return block

def varStmt():
	advance()
	consume("IDENTIFIER", "Expected variable name.")
	variable = Variable(tokenList[current-1])
	value = None
	if matchToken("EQUAL"):
		advance()
		expr = expression()
		value = expr

	consume("SEMICOLON", "Missing semicolon at the end of a statement.")
	return VarDecNode(variable, value)

def expressionStmt():
	expr = expression()
	consume("SEMICOLON", "Missing semicolon at the end of a statement.")
	return ExpressionNode(expr)


#Expression Grammar

def expression():
	expr = assignment()
	return expr

def assignment():
	if matchToken("IDENTIFIER") and tokenList[current+1].type == tokenType["EQUAL"]:
		advance()
		advance()
		left = Variable(tokenList[current-2])
		expr = Binary(left, tokenList[current-1], assignment())
		return expr
	else:
		return logic_or()

def logic_or():
	expr = logic_and()
	while matchToken("OR"):
		token = tokenList[current]
		advance()
		right = logic_and()
		expr = Binary(expr, token, right)
	return expr

def logic_and():
	expr = equality()
	while matchToken("AND"):
		token = tokenList[current]
		advance()
		right = equality()
		expr = Binary(expr, token, right)
	return expr	

def equality():
	expr = comparison()		
	while matchToken("EQUAL_EQUAL") or matchToken("BANG_EQUAL"):
		operator = tokenList[current]
		advance()
		right = comparison()
		expr = Binary(expr, operator, right)
	return expr	

def comparison():
	expr = term()
	while matchToken("LESS") or matchToken("LESS_EQUAL") or matchToken("GREATER") or matchToken("GREATER_EQUAL"):
		operator = tokenList[current]
		advance()
		right = term()
		expr = Binary(expr, operator, right)
	return expr	

def term():
	expr = factor()		
	while matchToken("PLUS") or matchToken("MINUS"):
		operator = tokenList[current]
		advance()
		right = factor()
		expr = Binary(expr, operator, right)
	return expr	


def factor():
	expr = unary()		
	while matchToken("STAR") or matchToken("SLASH"):
		operator = tokenList[current]
		advance()
		right = unary()
		expr = Binary(expr, operator, right)
	return expr	

def unary():
	if matchToken("BANG") or matchToken("MINUS"):
		operator = tokenList[current]
		advance()
		child = unary()
		return Unary(operator, child)
	else:
		return funCall()

def funCall():

	token = tokenList[current]		#helper token for locating the function call
	kallable = primary()
	arglist = []
	while matchToken("LEFT_PAREN"):
		consume("LEFT_PAREN", "Missing left parenthesis.")
		arglist.clear()
		if not matchToken("RIGHT_PAREN"):
			arg = expression()
			arglist.append(arg)
			while matchToken("COMMA"):
				advance()
				arg = expression()
				arglist.append(arg)
		consume("RIGHT_PAREN", "Missing right parenthesis after function parameters")
		kallable = Call(kallable, arglist, token)
	return kallable


def primary():
	if matchToken("STRING") or matchToken("NUMBER") or matchToken("TRUE") or matchToken("FALSE") or matchToken("NIL"):
		advance()
		return Literal(tokenList[current-1])

	elif matchToken("IDENTIFIER"):
		advance()
		return Variable(tokenList[current-1])

	elif matchToken("LEFT_PAREN"):
		advance()
		expr = expression()
		consume("RIGHT_PAREN", "Missing right parenthesis at expression.")
		return Grouping(expr)
	else:
		getMessage("Malformed Expression", tokenList[current].line)
		raise SyntaxException		



#helper functions

def matchToken(token):
	return tokenList[current].type == tokenType[token]


def consume(tokenName, messg):
	if not matchToken(tokenName):
		getMessage(messg, tokenList[current].line)
		raise SyntaxException
	else:
		advance()	

def advance():
	global current
	current += 1

def getMessage(message, line):
		print("Invalid syntax at line " + str(line) + ": " + message)


def prettyPrinter(stmt):
	messg=""
	if isinstance(stmt, FunctionNode):
		pass
	elif isinstance(stmt, VarDecNode):
		messg += "( VAR " + prettyPrinter(stmt.var) + " " + prettyPrinter(stmt.initexpr) + " )"
	elif isinstance(stmt, PrintNode):
		messg += "( PRINT "
		messg += prettyPrinter(stmt.expr)
		messg += " )" 
	elif isinstance(stmt, ReturnNode):
		messg += "( RETURN " + prettyPrinter(stmt.expr) + " )"
	elif isinstance(stmt, IfNode):
		pass
	elif isinstance(stmt, WhileNode):
		pass
	elif isinstance(stmt, BlockNode):
		messg += "BLOCK\n"
		for statement in stmt.stmts:
			messg += "\t"
			messg += prettyPrinter(statement)
			#expressions
	elif isinstance(stmt, Binary):
		messg += "( "
		messg += stmt.token.text
		messg += " " + prettyPrinter(stmt.right)
		messg += " " + prettyPrinter(stmt.left)
		messg += " )"
	elif isinstance(stmt, Unary):
		messg += "( "
		messg += stmt.token.text + " "
		messg += prettyPrinter(stmt.expr) + " )"
	elif isinstance(stmt, Literal):
		messg = stmt.token.text
	elif isinstance(stmt, Variable):
		messg = stmt.token.text
	elif isinstance(stmt, Grouping):
		messg = "( " + prettyPrinter(stmt.expr) + " )"
	elif isinstance(stmt, Call):
		messg = "( " + prettyPrinter(stmt.callAble) + " "
		for arg in stmt.arglist:
			messg += prettyPrinter(arg) + " "
		messg += " )"
	return messg	

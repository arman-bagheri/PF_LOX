import sys

#lexical analysis

numbers = ['0','1','2','3','4','5','6','7','8','9']
#variable letters
firstLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
otherLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"

keywords = ["and", "class", "else", "false", "fun", "for", "if", "nil", "or", "return", "super", "this", "true", "var", "while", "env"]

tokenType = {
	#ONE CHARACTER
	"LEFT_PAREN": 0,
	"RIGHT_PAREN": 1,
	"LEFT_BRACE": 2,
	"RIGHT_BRACE": 3,
	"COMMA": 4,
	"DOT": 5,
	"MINUS": 6,
	"PLUS": 7,
	"SEMICOLON": 8,
	"SLASH": 9,
	"STAR": 10,
	#ONE OR TWO CHARACTER
	"BANG": 11,
	"BANG_EQUAL": 12,
	"EQUAL": 13,
	"EQUAL_EQUAL": 14,
	"GREATER": 15,
	"GREATER_EQUAL": 16,
	"LESS":17,
	"LESS_EQUAL":18,
	#LITERALS
	"IDENTIFIER":19,
	"STRING":20,
	"NUMBER":21,
	
	#KEYWORDS
	"AND":22,
	"CLASS":23,
	"ELSE":24,
	"FALSE":25,
	"FUN":26,
	"FOR":27,
	"IF":28,
	"NIL":29,
	"OR":30,
	"RETURN":32,
	"SUPER":33,
	"THIS":34,
	"TRUE":35,
	"VAR":36,
	"WHILE":37,

	"EOF":38,

	#LOGING purposes
	"ENV":39,
}


index = 0


def tokenName(num):
	for key in tokenType:
		if tokenType[key] == num:
			return key
	return "undefined token"		

class token:
	def __init__(self, tokenTypeStr, text, literal, line):
		self.type = tokenType[tokenTypeStr]
		self.text = text
		self.literal = literal
		self.line = line

	def printToken(self):
		print(tokenName(self.type) + " " + self.text + " " + str(self.literal))	



tokenList = []


def lex(script):
	global index
	tokenList.clear()
	index = 0
	line = 1
	hadError = False
	while index < len(script):
		#one character
		
		if script[index] == '(':
			tokenList.append(token("LEFT_PAREN", script[index], None, line))
			index += 1
		
		elif script[index] == ')':
			tokenList.append(token("RIGHT_PAREN", script[index], None, line))	
			index += 1
		
		elif script[index] == '{':
			tokenList.append(token("LEFT_BRACE", script[index], None, line))
			index += 1
		
		elif script[index] == '}':
			tokenList.append(token("RIGHT_BRACE", script[index], None, line))	
			index += 1	
		
		elif script[index] == ',':
			tokenList.append(token("COMMA", script[index], None, line))
			index += 1
		
		elif script[index] == '.':
			tokenList.append(token("DOT", script[index], None, line))	
			index += 1
		
		elif script[index] == '-':
			tokenList.append(token("MINUS", script[index], None, line))	
			index += 1	
		
		elif script[index] == '+':
			tokenList.append(token("PLUS", script[index], None, line))
			index += 1
		
		elif script[index] == ';':
			tokenList.append(token("SEMICOLON", script[index], None, line))	
			index += 1
		
		elif script[index] == '/':
			if lookahead(index, script) == '/':
				while lookahead(index, script) != '\n' and lookahead(index, script) != None:
					index += 1
				index += 1	
			elif lookahead(index, script) == '*':
				current = index + 1
				while True:
					if lookahead(current, script) == None:  #comment not enclosed error
						hadError = True
						index = current + 1
						print("comment not enclosed at " + str(line), file=sys.stderr)
						break
					elif lookahead(current, script) == '\n':
						line += 1
						current += 1
					elif lookahead(current, script) == '*' and lookahead(current+1, script) == '/': #closing
						index = current + 3
						break
					else:
						current += 1		
			else:
				tokenList.append(token("SLASH", script[index], None, line))
				index += 1
		
		elif script[index] == '*':
			tokenList.append(token("STAR", script[index], None, line))	
			index += 1
		
		# FILLERS		
		elif script[index] == ' ':
			index += 1
		
		elif script[index] == '\n':
			index += 1
			line += 1

		elif script[index] == '\t':
			index += 1
		elif script[index] == '\r':
			index += 1		
		# ONE LETTER OR TWO LETTER TOKENS

		elif script[index] == '!':
			if lookahead(index, script) == '=':
				tokenList.append(token("BANG_EQUAL", script[index:index+2], None, line))
				index += 2
			else:
				tokenList.append(token("BANG", script[index], None, line))
				index += 1

		elif script[index] == '=':
			if lookahead(index, script) == '=':
				tokenList.append(token("EQUAL_EQUAL", script[index:index+2], None, line))
				index += 2
			else:
				tokenList.append(token("EQUAL", script[index], None, line))
				index += 1

		elif script[index] == '>':
			if lookahead(index, script) == '=':
				tokenList.append(token("GREATER_EQUAL", script[index:index+2], None, line))
				index += 2
			else:
				tokenList.append(token("GREATER", script[index], None, line))
				index += 1

		elif script[index] == '<':
			if lookahead(index, script) == '=':
				tokenList.append(token("LESS_EQUAL", script[index:index+2], None, line))
				index += 2
			else:
				tokenList.append(token("LESS", script[index], None, line))
				index += 1

		#NUMBERS

		elif script[index] in numbers:
			lastInt = index
			while lookahead(lastInt, script)!=None and lookahead(lastInt, script) in numbers:
				lastInt += 1
			if lookahead(lastInt, script) == '.' and lookahead(lastInt+1, script) in numbers:
				lastInt += 2
				while lookahead(lastInt, script)!=None and lookahead(lastInt, script) in numbers:
					lastInt += 1
				tokenList.append(token("NUMBER", script[index:lastInt+1], float(script[index:lastInt+1]), line))	
			else:
				tokenList.append(token("NUMBER", script[index:lastInt+1], float(script[index:lastInt+1]), line))

			index = lastInt + 1

		#STRING
		
		elif script[index] == '"':
			literal = ""
			closing = index + 1
			while script[closing] !='"' and script[closing] != '\n' and closing<len(script):
				if script[closing] == '\\' and lookahead(closing, script) == 'n':
					literal += '\n'
					closing += 1
				else:
					literal += script[closing]	
				closing += 1
			if closing>=len(script):
				index = closing
				hadError = True
				print("invalid string token at line " + str(line) + " : not enclosed!", file = sys.stderr)	
			elif script[closing] == '"':
				tokenList.append(token("STRING", script[index:closing+1], literal, line))
				index = closing + 1

			else:	#error string not closed
				index = closing
				hadError = True
				print("invalid string token at line " + str(line) + " : not enclosed!", file = sys.stderr)

		#IDENTIFIER / KEYWORDS
		
		elif script[index] in firstLetters:
			last = index
			while lookahead(last, script) != None and lookahead(last, script) in otherLetters:
				last += 1
			key = script[index:last+1]
			if key in keywords:  #KEYWORD	
					if key == "true":
						tokenList.append(token("TRUE", script[index:last+1], True, line))

					elif key == "false":
						tokenList.append(token("FALSE", script[index:last+1], False, line))

					elif key == "nil":
						tokenList.append(token("NIL", script[index:last+1], None, line))

					else:	
						tokenList.append(token(key.upper(), script[index:last+1], None, line))
			
			else:	#IDENTIFIER
				tokenList.append(token("IDENTIFIER", script[index:last+1], None, line))
			index = last + 1	

		else:		#undefined token
			hadError = True
			print("unexpected character " + script[index] + " at " + str(line), file=sys.stderr)
			index += 1

	tokenList.append(token("EOF", "", "", line))
	return hadError


def lookahead(index, script):
	try:
		nextchar = script[index + 1]
		return nextchar
	except:
		return None



#Logging functions

def printTokenList():
	print("[", end='')
	for token in tokenList:
		print("'" + token.text + "'" + ", ", end='')
	print("]")
	for token in tokenList:
		token.printToken()



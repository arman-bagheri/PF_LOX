import scanner
import time
lexemes = ["and class else fun false true asdf23 fa__sa24 false false class"]

script = ""

for n in range(400):
	for x in lexemes:
		script += x
start_time = time.time_ns()
error = scanner.lex(script)
finish_time = time.time_ns()
print(error)
print("elapsed time is:    " + str(finish_time - start_time) + "ns")


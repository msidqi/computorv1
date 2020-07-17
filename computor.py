import re
import sys
import math

class Term:
	def __init__(self, degee, coefficient):
		self.deg = degree
		self.coef = coefficient

class Complex:
	def __init__(self, real, imaginary):
		self.r = real
		self.i = imaginary

def abs(n):
	if n < 0:
		return (-n)
	return n

def pow(a, exponent):
	if exponent == 0:
		return 1
	if exponent < 0:
		a = 1 / a
		exponent = -exponent
	while exponent > 1:
		a = a * a
		exponent -= 1
	return a

def solve_poly2(a, b, c):
	discr = b * b - 4 * a * c
	if discr == 0:
		return (-b / (2 * a))
	squareDisc = math.sqrt(abs(discr))
	if discr < 0:
		return [
			Complex(-b / (2 * a), squareDisc / (2 * a)),
			Complex(-b / (2 * a), -squareDisc / (2 * a))
		]
	return [
		(-b + squareDisc) / (2 * a),
		(-b - squareDisc) / (2 * a)
		]


def put_error(message):
	print(message, file = sys.stderr)

def check_equation_format(equation):
	len = len(equation)
	# if (len < 3 || )

error_usage = "Usage: computor.py [EQUATION STRING]"
error_format = "Error: Equation not well formated"

argc = len(sys.argv)
if argc < 2:
	put_error(error_usage)
	exit(0)
equation = sys.argv[1]
equation = equation.split('=')
if len(equation) != 2:
	put_error(error_format)
	exit(0)
leftside = equation[0]
rightside = equation[1]

# m = re.match('X\^[\d]', leftside)
leftside = leftside.replace(" ", "")
print(leftside)
# m = re.search("((?P<coef>[+-]?\d+\.?\d*)\*X\^(?P<deg>\d+))+", leftside)
m = re.search("((?P<coef>[+-]?\d+\.?\d*)\*[Xx](?P<deg>\^?\d+)*)", leftside)
# m = re.search("(\d+(\.\d+)?)", leftside)
if m:
	print(m.groups())
else:
	print("No match")
# print(leftside, '  ||||||  ', rightside)

# ret = solve_poly2(9, 2, 1)
# print(isinstance(ret[0], Complex))


# check_equation_format(equation)
# print("argv> ", equation, "\nargc> ", argc)

# txt = "The rain in Spain ai"
# x = re.search("ai", txt)
# print(x.string)

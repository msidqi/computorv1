import re
import sys
import math

class Term:
	def __init__(self, coefficient, degree):
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

def fill_terms(matches):
	terms = []
	for match in matches:
		if match[3] == '0':
			coef = 0
			deg = 1
		else:
			if match[1] == '' and match[2] != '':
				coef = 1
			else:
				coef = float(match[1])
			deg = float(match[2])
		t = Term(coef, deg)
		terms.append(t)
	return terms

def is_matches_valid_format(matches):
	for match in matches:
		if len(match) != 4:
			return False
		if match[1] == '' and match[2] == '' and match[3] != '0':
			return False
		# if match[1] == '' or match[2] == '' and match[3] != '0'
			# return False
	return True

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
leftside = equation[0].replace(" ", "")
rightside = equation[1].replace(" ", "")
# m = re.search("((?P<coef>[+-]?\d+\.?\d*)\*X\^(?P<deg>\d+))+", leftside)
regex = "((?P<coef>[+-]?\d+\.?\d*)?\*?[Xx]\^?(?P<deg>\d+)*)|(0)"
leftside = re.findall(regex, leftside)
rightside = re.findall(regex, rightside)

if leftside and rightside and is_matches_valid_format(leftside) and is_matches_valid_format(rightside):
	leftside = fill_terms(leftside)
	rightside = fill_terms(rightside)
else:
	put_error(error_format)
	exit(0)

print('leftside')
for term in leftside:
	print(term.coef, '^', term.deg)


print('rightside')
for term in rightside:
	print(term.coef, '^', term.deg)

# ret = solve_poly2(9, 2, 1)
# print(isinstance(ret[0], Complex))

# test 0 | test negative coef
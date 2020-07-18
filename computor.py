import re
import sys
import math

class Term:
	def __init__(self, coefficient, degree, hide_exponent = False):
		self.deg = degree
		self.coef = coefficient
		self.hide_exponent = hide_exponent

	def add(self, other_term):
		if self.deg != other_term.deg:
			raise Exception("Error::Term: Cannot add terms with different exponents")
		self.coef += other_term.coef

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
		return (
			Complex(-b / (2 * a), squareDisc / (2 * a)),
			Complex(-b / (2 * a), -squareDisc / (2 * a))
		)
	return (
		(-b + squareDisc) / (2 * a),
		(-b - squareDisc) / (2 * a)
	)

def put_error(message):
	print(message, file = sys.stderr)

def aton(a):
	num = float(a)
	num = int(num) if num.is_integer() else num
	return num

def fill_terms(matches):
	terms = []
	for match in matches:
		if match[3] != '': # case 2 => deg 0 => 2 * X^0
			coef = aton(match[3])
			deg = 0
		elif match[1] == '' and match[2] != '': # case X^3 => coef 1 => 1 * X^3
			coef = 1
			deg = aton(match[2])
		# elif match[1] != '' and match[2] == '':
		# 	coef = aton(match[1])
		# 	deg = 0
		elif match[1] != '' and match[2] == '': # case 6 * X => coef 6 deg 1 => 6 * X^1
			coef = aton(match[1])
			deg = 1
		else:
			coef = aton(match[1])
			deg = aton(match[2])
		t = Term(coef, deg)
		terms.append(t)
	return terms

def is_matches_valid_format(matches):
	for match in matches:
		if len(match) != 4:
			return False
		if match[1] == '' and match[2] == '' and match[3] == '':
			return False
	return True

def print_equation_side(equ):
	length = len(equ)
	for i in range(length):
		if equ[i].hide_exponent and i <= 2 and i >= 0 and length > 1:
			continue
		if i == 0:
			if equ[i].hide_exponent:
				print(equ[i].coef, end = " ")
			else:
				print("{} * X^{}".format(equ[i].coef, equ[i].deg), end = " ")
		else:
			if equ[i].hide_exponent:
				print("{} {}".format('-' if equ[i].coef < 0 else '+', abs(equ[i].coef)), end = " ")
			else:
				print("{} {} * X^{}".format('-' if equ[i].coef < 0 else '+', abs(equ[i].coef), equ[i].deg), end = " ")

def print_equation(leftside, rightside, prefix = ""):
	if prefix:
		print(prefix, end=" ")
	print_equation_side(leftside)
	print("=", end = " ")
	print_equation_side(rightside)
	print("")

def print_poly_degree(poly_degree):
	print('Polynomial degree: {}'.format(poly_degree))

def simplify_equation(leftside, rightside):
	# move rightside to left
	for term in rightside:
		term.coef *= -1
		leftside.append(term)
	# replace right with 0
	rightside = [Term(0, 0, True)]
	# simplify
	simplified = [ Term(0, 0, True), Term(0, 1, True), Term(0, 2, True) ]
	poly_degree = 0
	for term in leftside:
		# if term.coef == 0:
		# 	simplified[0].hide_exponent = False
		# 	simplified[1].hide_exponent = False
		# 	simplified[2].hide_exponent = False
		# 	continue
		# else:
		if term.deg == 0:
			simplified[0].add(term)
			simplified[0].hide_exponent = False
			poly_degree = max(term.deg, poly_degree)
		elif term.deg == 1:
			simplified[1].add(term)
			simplified[1].hide_exponent = False
			poly_degree = max(term.deg, poly_degree)
		elif term.deg == 2:
			simplified[2].add(term)
			simplified[2].hide_exponent = False
			print('passed----')
			poly_degree = max(term.deg, poly_degree)
		elif term.deg > 2: # degree cannot solve
			poly_degree = max(term.deg, poly_degree)
			for s in simplified:
				if s.deg == term.deg:
					s.add(term)
					s.hide_exponent = False
					break
			else:
				term.hide_exponent = False
				simplified.append(term)
	# filter coef == 0 from simplified
	return (simplified, rightside, poly_degree)

def solve_equation(leftside, rightside, poly_degree):
	no_solutions = 'There are no solutions !'
	all_real_numbers = 'The solution: all real numbers'
	if poly_degree > 2:
		print("The polynomial degree is stricly greater than 2, I can't solve.")
		return
	if poly_degree == 2:
		solution = solve_poly2(leftside[2].coef, leftside[1].coef, leftside[0].coef)
		if isinstance(solution, float) or isinstance(solution, int):
			print('Discriminant is strictly positive is null, the solution is:', solution)
		elif isinstance(solution[0], float) or isinstance(solution[0], int):
			print('Discriminant is strictly positive, the two solutions are:',
			solution[0],
			solution[1])
		elif isinstance(solution[0], Complex):
			print('Discriminant is strictly negative, the two solutions are:',
			"{} {} {} i".format(solution[0].r, '-' if solution[0].i < 0 else '+', abs(solution[0].i)),
			"{} {} {} i".format(solution[1].r, '-' if solution[1].i < 0 else '+', abs(solution[1].i)))
	if poly_degree == 1:
		zero_term = leftside[0]
		one_term = leftside[1]
		if one_term.coef == 0 and zero_term.coef != 0: # 1 == 0
			print(no_solutions)
		elif one_term.coef == 0 and zero_term.coef == 0: # 0 == 0
			print(all_real_numbers)
		elif one_term.coef != 0 and zero_term.coef == 0:
			solution = -1 * zero_term.coef / one_term.coef
			print('The solution is:', solution)	
	if poly_degree == 0:
		zero_term = leftside[0]
		if zero_term.coef != 0:
			print(no_solutions)
		else:
			print(all_real_numbers)
		# for term in leftside:
		# 	if term.coef != 0:
		# 		print(no_solutions)
		# 		break

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

regex = "((?P<coef>[+-]?\d+\.?\d*)?\*?[Xx]\^?(?P<deg>\d+)*)|([+-]?\d+\.?\d*)"
leftside = re.findall(regex, leftside)
rightside = re.findall(regex, rightside)

# print(leftside, rightside)
if leftside and rightside and is_matches_valid_format(leftside) and is_matches_valid_format(rightside):
	leftside = fill_terms(leftside)
	rightside = fill_terms(rightside)
else:
	put_error(error_format)
	exit(0)

# simplify
leftside, rightside, poly_degree = simplify_equation(leftside, rightside)

for simp in leftside:
	print(simp.coef, simp.deg)

print_equation(leftside, rightside, 'Reduced form:')
print_poly_degree(poly_degree)
solve_equation(leftside, rightside, poly_degree)

# ret = solve_poly2(9, 2, 1)
# print(isinstance(ret[0], Complex))

# test 0 | test negative coef
import re
import sys
import math

class Term:
	def __init__(self, coefficient, degree, hide_exponent = False, hide_term = False):
		self.deg = degree
		self.coef = coefficient
		self.hide_exponent = hide_exponent
		self.hide_term = hide_term

	def add(self, other_term):
		if self.deg != other_term.deg:
			raise Exception("Error::Term: Cannot add terms with different exponents")
		self.coef += other_term.coef
		self.update_hide_state()

	def update_hide_state(self):
		if self.coef == 0:
			self.hide_exponent = True
			self.hide_term = True
		else:
			if self.deg != 0:
				self.hide_exponent = False
			else:
				self.hide_exponent = True
			self.hide_term = False

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
			coef = float(match[3])
			deg = 0
		elif match[1] == '' and match[2] != '': # case X^3 => coef 1 => 1 * X^3
			coef = 1
			deg = float(match[2])
		# elif match[1] != '' and match[2] == '':
		# 	coef = aton(match[1])
		# 	deg = 0
		elif match[1] != '' and match[2] == '': # case 6 * X => coef 6 deg 1 => 6 * X^1
			coef = float(match[1])
			deg = 1
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
		if match[1] == '' and match[2] == '' and match[3] == '':
			return False
	return True

def print_equation_side(equ):
	length = len(equ)
	for i in range(length):
		# if equ[i].hide_exponent and i <= 2 and i >= 0 and length > 1 and equ[i].coef == 0: # hide defaults that are 0
		# 	continue
		# print('equ[i].hide_term', equ[i].hide_term)
		if equ[i].hide_term:
			continue
		if i == 0:
			if equ[i].hide_exponent:
				print(equ[i].coef, end = " ")
			else:
				print("{} * X^{:.0f}".format(equ[i].coef, equ[i].deg), end = " ")
		else:
			if equ[i].hide_exponent:
				print("{} {}".format('-' if equ[i].coef < 0 else '+', abs(equ[i].coef)), end = " ")
			else:
				print("{} {} * X^{:.0f}".format('-' if equ[i].coef < 0 else '+', abs(equ[i].coef), equ[i].deg), end = " ")

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
	rightside = [Term(0, 0, True, False)]
	# simplify
	simplified = [ Term(0, 0, True, True), Term(0, 1, True, True), Term(0, 2, True, True) ]
	for term in leftside:
		if term.coef == 0:
			continue
		if term.deg == 0:
			simplified[0].add(term)
		elif term.deg == 1:
			simplified[1].add(term)
		elif term.deg == 2:
			simplified[2].add(term)
		elif term.deg > 2: # degree cannot solve
			for simp in simplified:
				if simp.deg == term.deg:
					simp.add(term)
					break
			else:
				term.update_hide_state()
				simplified.append(term)
	poly_degree = 0
	for simp in simplified:
		if simp.coef != 0:
			poly_degree = max(simp.deg, poly_degree)
	return (simplified, rightside, poly_degree)

def pick_precision(num):
	return 0 if num.is_integer() else 4

def solve_equation(leftside, rightside, poly_degree):
	no_solutions = 'There are no solutions !'
	all_real_numbers = 'The solution: all real numbers'
	if poly_degree > 2:
		print("The polynomial degree is stricly greater than 2, I can't solve.")
	elif poly_degree == 2:# and leftside[2].coef != 0:
		solution = solve_poly2(leftside[2].coef, leftside[1].coef, leftside[0].coef)
		if isinstance(solution, float):# or isinstance(solution, int):
			print('Discriminant is strictly positive is null, the solution is:')
			print("{0:.{1}f}".format(solution, pick_precision(solution)))
		elif isinstance(solution[0], float):# or isinstance(solution[0], int):
			print('Discriminant is strictly positive, the two solutions are:')
			print("{0:.{1}f}".format(solution[0], pick_precision(solution[0])))
			print("{0:.{1}f}".format(solution[1], pick_precision(solution[1])))
		elif isinstance(solution[0], Complex):
			print('Discriminant is strictly negative, the two solutions are:\n'
			" {0:.{1}f} {2} {3:.{4}f}i\n".format(solution[0].r, pick_precision(solution[0].r),
			'-' if solution[0].i < 0 else '+', abs(solution[0].i), pick_precision(solution[0].i)),
			"{0:.{1}f} {2} {3:.{4}f}i".format(solution[1].r, pick_precision(solution[1].r),
			'-' if solution[1].i < 0 else '+', abs(solution[1].i), pick_precision(solution[1].i)))
	elif poly_degree == 1:
		zero_term = leftside[0]
		one_term = leftside[1]
		if one_term.coef == 0 and zero_term.coef != 0: # 1 == 0
			print(no_solutions)
		elif one_term.coef == 0 and zero_term.coef == 0: # 0 == 0
			print(all_real_numbers)
		elif one_term.coef != 0:# and zero_term.coef == 0:
			solution = -1 * zero_term.coef / one_term.coef
			print('The solution is:', solution)	
	elif poly_degree == 0:
		zero_term = leftside[0]
		if zero_term.coef != 0:
			print(no_solutions)
		else:
			print(all_real_numbers)
		# for term in leftside:
		# 	if term.coef != 0:
		# 		print(no_solutions)
		# 		break

def parse_equation(equation_string):
	error_format = "Error: Equation not well formated"
	equation = equation_string.split('=')
	if len(equation) != 2:
		raise Exception(error_format)
	leftside = equation[0].replace(" ", "")
	rightside = equation[1].replace(" ", "")

	regex = "((?P<coef>[+-]?\d+\.?\d*)?\*?[Xx]\^?(?P<deg>\d+)*)|([+-]?\d+\.?\d*)"
	leftside = re.findall(regex, leftside)
	rightside = re.findall(regex, rightside)
	if not is_matches_valid_format(leftside) or not is_matches_valid_format(rightside):
		raise Exception(error_format)
	return (leftside, rightside)


# intro
def main(argv):
	error_usage = "Usage: computor.py [EQUATION STRING]"
	argc = len(argv)
	if argc < 2:
		put_error(error_usage)
		exit(0)
	equation_string = argv[1]

	try:
		leftside, rightside = parse_equation(equation_string)
	except Exception as format_error:
		put_error(format_error)
		exit(0)

	# transform matches to lists of Term class 
	leftside = fill_terms(leftside)
	rightside = fill_terms(rightside)

	# simplify
	leftside, rightside, poly_degree = simplify_equation(leftside, rightside)

	# for simp in leftside:
	# 	print(simp.coef, simp.deg)

	print_equation(leftside, rightside, 'Reduced form:')
	print_poly_degree(poly_degree)
	solve_equation(leftside, rightside, poly_degree)

	# test 0 | test negative coef

if __name__ == "__main__":
	main(sys.argv)
import unittest
from computor import main, parse_equation, fill_terms, simplify_equation, solve_equation, Term, Complex

class TestEquationSolver(unittest.TestCase):
	def test_2nd_degree_positive_disc(self):
		leftside, rightside = parse_equation("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
		expect_leftside = [('5*X^0', '5', '0', ''), ('+4*X^1', '+4', '1', ''), ('-9.3*X^2', '-9.3', '2', '')]
		expect_rightside = [('1*X^0', '1', '0', '')]
		self.assertEqual(leftside, expect_leftside)
		self.assertEqual(rightside, expect_rightside)

		# make list of terms
		leftside = fill_terms(leftside)
		rightside = fill_terms(rightside)
		expect_leftside = [Term(5, 0), Term(4, 1), Term(-9.3, 2)]
		expect_rightside = [Term(1, 0)]
		self.assertEquationSideEquals(leftside, expect_leftside)
		self.assertEquationSideEquals(rightside, expect_rightside)

		#simplify equation
		leftside, rightside, poly_degree = simplify_equation(leftside, rightside)
		expect_poly_degree = 2
		expect_leftside = [Term(4, 0, True, False), Term(4, 1), Term(-9.3, 2)]
		expect_rightside = [Term(0, 0, True, False)]
		self.assertEqual(poly_degree, expect_poly_degree)
		self.assertEquationSideEquals(leftside, expect_leftside)
		self.assertEquationSideEquals(rightside, expect_rightside)


	def test_1st_degree_long_format(self):
		leftside, rightside = parse_equation("5 * X^0 + 4 * X^1 = 4 * X^0")
		expect_leftside = [('5*X^0', '5', '0', ''), ('+4*X^1', '+4', '1', '')]
		expect_rightside = [('4*X^0', '4', '0', '')]
		self.assertEqual(leftside, expect_leftside)
		self.assertEqual(rightside, expect_rightside)

		# make list of terms
		leftside = fill_terms(leftside)
		rightside = fill_terms(rightside)
		expect_leftside = [Term(5, 0), Term(4, 1)]
		expect_rightside = [Term(4, 0)]
		self.assertEquationSideEquals(leftside, expect_leftside)
		self.assertEquationSideEquals(rightside, expect_rightside)

		#simplify equation
		leftside, rightside, poly_degree = simplify_equation(leftside, rightside)
		expect_poly_degree = 1
		expect_leftside = [Term(1, 0, True, False), Term(4, 1), Term(0, 2, True, True)]
		expect_rightside = [Term(0, 0, True, False)]
		self.assertEqual(poly_degree, expect_poly_degree)
		self.assertEquationSideEquals(leftside, expect_leftside)
		self.assertEquationSideEquals(rightside, expect_rightside)


	def test_1st_degree_natural_format(self):
		leftside, rightside = parse_equation("5 + 4 * X + X^2 = X^2")
		expect_leftside = [('', '', '', '5'), ('+4*X', '+4', '', ''), ('X^2', '', '2', '')]
		expect_rightside = [('X^2', '', '2', '')]
		# same parsed values
		self.assertEqual(leftside, expect_leftside)
		self.assertEqual(rightside, expect_rightside)

		# make list of terms
		leftside = fill_terms(leftside)
		rightside = fill_terms(rightside)
		expect_leftside = [Term(5, 0), Term(4, 1), Term(1, 2)]
		expect_rightside = [Term(1, 2.0)]
		self.assertEquationSideEquals(leftside, expect_leftside)
		self.assertEquationSideEquals(rightside, expect_rightside)

		#simplify equation
		leftside, rightside, poly_degree = simplify_equation(leftside, rightside)
		expect_poly_degree = 1
		expect_leftside = [Term(5, 0, True, False), Term(4, 1), Term(0, 2, True, True)]
		expect_rightside = [Term(0, 0, True, False)]
		self.assertEqual(poly_degree, expect_poly_degree)
		self.assertEquationSideEquals(leftside, expect_leftside)
		self.assertEquationSideEquals(rightside, expect_rightside)

		# solve_equation(leftside, rightside, poly_degree)



	def assertTermsEqual(self, term, expect_term):
		self.assertEqual(term.deg, expect_term.deg)
		self.assertEqual(term.coef, expect_term.coef)
		self.assertEqual(term.hide_exponent, expect_term.hide_exponent)
		self.assertEqual(term.hide_term, expect_term.hide_term)
	
	def assertEquationSideEquals(self, side, expect_side):
		# same length
		self.assertEqual(len(side), len(expect_side))
		# same term values
		for i in range(len(side)):
			self.assertTermsEqual(side[i], expect_side[i])
			i += 1

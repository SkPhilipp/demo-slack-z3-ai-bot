from pyinvoker.usage import Usage
from z3 import z3


def math_z3_solve(expression: str):
    parsed = z3.parse_smt2_string(expression)
    solver = z3.Solver()
    solver.add(parsed)
    result = solver.check()
    if result == z3.sat:
        return f"The result is satisfiable. Model: {solver.model()}."
    elif result == z3.unsat:
        return f"The result is unsatisfiable."
    elif result == z3.unknown:
        return f"The result is unknown."
    else:
        raise ValueError(f"Unexpected result: {result}.")


math_z3_solve_usage = Usage(math_z3_solve)
math_z3_solve_usage.example(description="""
user: "Given a is less than 10 and f(a, true) is less than 100, what is a?"
""")(expression="""
(declare-const a Int)
(declare-fun f (Int Bool) Int)
(assert (< a 10))
(assert (< (f a true) 100))
""")
math_z3_solve_usage.example(description="""
user: "What is 1 + 1?"
""")(expression="""
(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(assert (= a 1))
(assert (= b 1))
(assert (= c (+ a b)))
""")

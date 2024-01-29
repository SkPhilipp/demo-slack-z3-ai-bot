from z3 import z3

from rebot.ai.functions import FunctionPackage

package_math = FunctionPackage(name="math")


@package_math.registered(
    name="math.z3solve",
    description="Solve mathematical expressions using Z3 in smt2 format",
    examples=[
        """
        user: Given a is less than 10 and f(a, true) is less than 100, what is a?
        assistant:
        (declare-const a Int)
        (declare-fun f (Int Bool) Int)
        (assert (< a 10))
        (assert (< (f a true) 100))
        """,
        """
        user: What is 1 + 1?
        assistant:
        (declare-const a Int)
        (declare-const b Int)
        (declare-const c Int)
        (assert (= a 1))
        (assert (= b 1))
        (assert (= c (+ a b)))
        """
    ],
    inputs="A multiline string expression in smt2 format"
)
def math__z3solve(expression: str):
    print(expression)
    parsed = z3.parse_smt2_string(expression)
    solver = z3.Solver()
    solver.add(parsed)
    result = solver.check()
    if result == z3.sat:
        return f"The result is {solver.model()}.\nExpression: ```\n{expression}\n```"
    elif result == z3.unsat:
        return f"The result is unsatisfiable.\nExpression: ```\n{expression}\n```"
    elif result == z3.unknown:
        return f"The result is unknown.\nExpression: ```\n{expression}\n```"
    else:
        return f"An unknown error occurred.\nExpression: ```\n{expression}\n```"

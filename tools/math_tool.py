from langchain_core.tools import tool
from sympy import sympify, solve, Symbol
from sympy.core.sympify import SympifyError

@tool
def math_tool(expression: str) -> str:
    """
    Safely evaluates or solves a mathematical expression.
    Examples:
    - '2 * (3 + 5)'
    - 'solve(3*x + 2 - 11)'
    """
    try:
        if "solve" in expression:
            x = Symbol('x')
            eq = expression.replace("solve(", "").rstrip(")")
            equation = sympify(eq)
            solutions = solve(equation, x)
            return f"Solutions: {solutions}"
        else:
            result = sympify(expression)
            return f"Result: {result}"
    except SympifyError as e:
        return f"Invalid math expression: {e}"
    except Exception as e:
        return f"Error solving expression: {e}"

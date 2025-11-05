import ast
import operator
import sys

# /d:/Tugas/LTIK/git/calculator.py

_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_unary_ops = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def safe_eval(expr: str):
    """
    Evaluates a numeric expression safely by allowing only numbers,
    binary ops (+ - * / % ** //) and unary +/-. Raises ValueError for invalid nodes.
    """
    node = ast.parse(expr, mode='eval')

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.Constant):  # Python 3.8+
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("Unsupported constant")
        if isinstance(n, ast.Num):  # older Python
            return n.n
        if isinstance(n, ast.BinOp):
            if type(n.op) in _ops:
                left = _eval(n.left)
                right = _eval(n.right)
                return _ops[type(n.op)](left, right)
            raise ValueError("Unsupported binary operator")
        if isinstance(n, ast.UnaryOp):
            if type(n.op) in _unary_ops:
                return _unary_ops[type(n.op)](_eval(n.operand))
            raise ValueError("Unsupported unary operator")
        raise ValueError(f"Unsupported expression: {type(n).__name__}")

    return _eval(node)

def main():
    print("Kalkulator interaktif. Ketik 'q' atau 'quit' untuk keluar.")
    while True:
        try:
            expr = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not expr:
            continue
        if expr.lower() in ("q", "quit", "exit"):
            break
        try:
            result = safe_eval(expr)
            print(result)
        except ZeroDivisionError:
            print("Error: pembagian dengan nol")
        except (SyntaxError, ValueError) as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
import re

def evaluate(expr: str, model: dict) -> bool:
    """
    Evaluate a propositional-logic formula under a given truth assignment.
    Supports: ~, &, ||, =>, <=>
    """
    # 1) Parenthesize all negations: "~X" → "(not X)"
    expr = re.sub(r'~\s*(\w+|\([^()]*\))', r'(not \1)', expr)

    # 2) Parenthesize and replace biconditional:
    #    A <=> B  →  (A) == (B)
    expr = re.sub(
        r'((?:\([^()]*\)|\b\w+\b)(?:\s*and\s*(?:\([^()]*\)|\b\w+\b))*)\s*<=>\s*(\([^()]*\)|\b\w+\b)',
        r'(\1) == (\2)',
        expr
    )

    # 3) Parenthesize and replace implication:
    #    A => B  →  (A) <= (B)
    expr = re.sub(
        r'((?:\([^()]*\)|\b\w+\b)(?:\s*and\s*(?:\([^()]*\)|\b\w+\b))*)\s*=>\s*(\([^()]*\)|\b\w+\b)',
        r'(\1) <= (\2)',
        expr
    )

    # 4) Replace disjunction and conjunction
    expr = expr.replace('||', ' or ')
    expr = expr.replace('&', ' and ')

    # 5) Substitute every propositional symbol with its model value (True/False)
    for sym in set(re.findall(r'\b[a-zA-Z_]\w*\b', expr)):
        if sym in model:
            expr = re.sub(rf'\b{sym}\b', str(model[sym]), expr)

    # 6) Safely evaluate the Python expression
    try:
        return eval(expr)
    except Exception:
        return False

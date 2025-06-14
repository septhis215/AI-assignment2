import re

def evaluate(expr: str, model: dict) -> bool:
    """
    Evaluate a logical expression (as a string) using Python's eval and a given truth assignment (model).
    Logical syntax: ~, &, ||, =>, <=>
    """
    # Convert logical syntax to Python syntax
    expr = expr.replace("<=>", "==")  # a <=> b → a == b
    expr = re.sub(r'(?<![a-zA-Z0-9_])=>', ' or not ', expr)  # a => b → not a or b
    expr = expr.replace("||", " or ")
    expr = expr.replace("&", " and ")
    expr = expr.replace("~", " not ")

    # Replace variables with model values
    for symbol in re.findall(r'\b[a-zA-Z_]\w*\b', expr):
        if symbol in model:
            expr = re.sub(rf'\b{symbol}\b', str(model[symbol]), expr)

    # Evaluate safely
    try:
        return eval(expr)
    except Exception:
        return False
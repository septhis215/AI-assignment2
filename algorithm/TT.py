from eval import evaluate
from typing import List, Tuple, Dict

def _eval_kb(clauses: List[str], facts: List[str], model: Dict[str, bool]) -> bool:
    full_kb = facts + clauses
    for expr in full_kb:
        if not evaluate(expr, model):
            return False
    return True

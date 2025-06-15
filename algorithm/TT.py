from eval import evaluate
from typing import List, Dict, Tuple
import re

def _eval_kb(clauses: List[str], facts: List[str], model: Dict[str, bool]) -> bool:
    full_kb = facts + clauses
    return all(evaluate(expr, model) for expr in full_kb)

def _extract_symbols(clauses: List[str], facts: List[str], query: str) -> List[str]:
    """Find all propositional symbols in the KB and query."""
    text = " ".join(clauses + facts + [query])
    # Match variables like a, p1, f_2, etc.
    symbols = set(re.findall(r'\b[a-zA-Z_]\w*\b', text))
    return sorted(symbols)

def tt(clauses: List[str], facts: List[str], query: str) -> Tuple[bool, int]:
    symbols = _extract_symbols(clauses, facts, query)
    n = len(symbols)
    count = 0

    # Iterate over all 2^n possible assignments
    for bits in range(1 << n):
        model = {}
        for i, sym in enumerate(symbols):
            # bit i of `bits` determines truth of symbols[i]
            model[sym] = bool((bits >> i) & 1)

        # If the KB is true under this model...
        if _eval_kb(clauses, facts, model):
            # ...and the query is also true, count it
            if evaluate(query, model):
                count += 1

    # entailed if at least one model of KB makes query true
    return (count > 0, count)

from typing import List, Tuple, Set
import re

# Splits a disjunction clause string into a set of literals
def parse_clause(clause: str) -> Set[str]:
    return set(part.strip() for part in clause.split("||"))

# Negates a literal: 'a' -> '~a', '~a' -> 'a'
def negate_literal(literal: str) -> str:
    return literal[1:] if literal.startswith('~') else f'~{literal}'

# Applies the resolution rule to two clauses and returns all possible resolvents
def resolve(ci: Set[str], cj: Set[str]) -> List[Set[str]]:
    resolvents = []
    for li in ci:
        if negate_literal(li) in cj:
            resolvent = (ci - {li}) | (cj - {negate_literal(li)})
            resolvents.append(resolvent)
    return resolvents

# Converts logic expressions with => and <=> into CNF-like disjunctions
def preprocess_logic(expr: str) -> List[str]:
    expr = expr.replace(" ", "")
    # Replace biconditional a<=>b with (a=>b)&(b=>a)
    expr = re.sub(r'(\w+)<=>\(([^()]+)\)', r'(\1=>(\2))&((\2)=>\1)', expr)
    expr = re.sub(r'\(([^()]+)\)<=>(\w+)', r'((\1)=>\2)&(\2=>(\1))', expr)
    expr = re.sub(r'(\w+)<=>(\w+)', r'(\1=>\2)&(\2=>\1)', expr)
    # Replace implication a=>b with ~a||b
    expr = re.sub(r'(\w+)=>(\w+)', r'~\1||\2', expr)
    expr = re.sub(r'(\w+)=>\(([^()]+)\)', r'~\1||(\2)', expr)
    expr = re.sub(r'\(([^()]+)\)=>(\w+)', r'~(\1)||\2', expr)
    # Split top-level conjunctions
    clauses = [cl.strip("()") for cl in expr.split("&")]
    return clauses

# Negates the query for resolution: 
# - conjunctions become a single clause with all negated literals (De Morgan)
# - disjunctions become multiple single-literal clauses
def negate_query(query: str) -> List[Set[str]]:
    query = query.replace(" ", "")
    if "&" in query:
        literals = [p.strip() for p in query.split("&")]
        return [set(negate_literal(lit) for lit in literals)]
    elif "||" in query:
        literals = [p.strip() for p in query.split("||")]
        return [{negate_literal(lit)} for lit in literals]
    else:
        return [{negate_literal(query)}]

# Main propositional logic resolution algorithm
def pl_resolution(clauses: List[str], facts: List[str], query: str) -> Tuple[bool, List[str]]:
    kb = []
    # Preprocess all clauses and facts into CNF-like disjunctions
    for cl in clauses + facts:
        for part in preprocess_logic(cl):
            kb.append(parse_clause(part))

    # Add the negated query to the KB
    for nq in negate_query(query):
        kb.append(nq)

    new = set()
    processed_pairs = set()

    # Main resolution loop
    while True:
        n = len(kb)
        for i in range(n):
            for j in range(i + 1, n):
                ci, cj = kb[i], kb[j]
                pair_key = frozenset((frozenset(ci), frozenset(cj)))
                if pair_key in processed_pairs:
                    continue
                processed_pairs.add(pair_key)

                resolvents = resolve(ci, cj)
                for res in resolvents:
                    print(f"Resolving: {ci} + {cj} => {res}")
                    if not res:
                        # Empty clause found: query is entailed
                        return True, ["{} (empty clause reached)"]
                    new.add(frozenset(res))

        # If no new clauses, query is not entailed
        if new.issubset(set(frozenset(c) for c in kb)):
            return False, []

        # Add new clauses to the KB
        for clause in new:
            if set(clause) not in kb:
                kb.append(set(clause))
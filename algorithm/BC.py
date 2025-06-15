from typing import List, Tuple, Dict, Set

def bc(clauses: List[str], facts: List[str], query: str) -> Tuple[bool, List[str]]:
    """
    Backward-Chaining over Horn clauses

    Args:
        clauses: List of strings. Each string is either
                - a fact (atomic symbol), e.g. "Rain"
                - a Horn clause of the form "A & B => C"
        facts:   List of known atomic symbols (initial facts), e.g. ["Rain", "Sprinkler"]
        query:   The symbol we want to test for entailment, e.g. "WetGrass"

    Returns:
        A tuple (entailed, inference_order):
            - entailed: True if `query` can be derived, False otherwise.
            - inference_order: The sequence in which symbols were attempted/inferred.
    """

    # Parse the Horn clauses into a mapping from conclusion to list of premise lists.
    # For example, for "a & b => c", rules["c"] = [["a", "b"]]
    rules: Dict[str, List[List[str]]] = {}
    for clause in clauses:
        if "=>" in clause:
            lhs, rhs = clause.split("=>")
            premises = [p.strip() for p in lhs.split("&")]
            conclusion = rhs.strip()
            # Add the premises list to the list of rules for this conclusion
            rules.setdefault(conclusion, []).append(premises)

    # Set of known facts (atomic symbols known to be true from the start)
    known_facts: Set[str] = set(facts)
    # List to record the order in which symbols are inferred or attempted
    inference_order: List[str] = []
    # Set to avoid revisiting the same symbol in the same proof chain (prevents infinite loops)
    visited: Set[str] = set()

    def prove(symbol: str) -> bool:
        """
        Recursively attempts to prove the given symbol.
        Returns True if the symbol can be inferred from facts and rules.
        """
        # If symbol is already a known fact, it's proven
        if symbol in known_facts:
            # Record the inference order if not already recorded
            if symbol not in inference_order:
                inference_order.append(symbol)
            return True
        # If we've already tried to prove this symbol in the current chain, avoid cycles
        if symbol in visited:
            return False
        # Mark this symbol as visited in the current proof chain
        visited.add(symbol)
        # Try to prove symbol using each rule that concludes it
        if symbol in rules:
            for premises in rules[symbol]:
                # Prove all premises for this rule
                if all(prove(p) for p in premises):
                    # If all premises are proven, this symbol is now a known fact
                    known_facts.add(symbol)
                    inference_order.append(symbol)
                    return True
        # If no rule can prove the symbol, return False
        return False

    # Start the backward chaining process for the query symbol
    entailed = prove(query)
    return entailed, inference_order
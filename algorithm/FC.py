from typing import List, Tuple, Dict
from collections import defaultdict, deque

def fc(clauses: List[str], facts: List[str], query: str) -> Tuple[bool, List[str]]:
    """
        Forward-Chaining over Horn clauses 
        
        Args:
        clauses: List of strings. Each string is either
                - a fact (atomic symbol), e.g. "Rain"
                - a Horn clause of the form "A & B => C"
        facts:   List of known atomic symbols (initial facts), e.g. ["Rain", "Sprinkler"]
        query:   The symbol we want to test for entailment, e.g. "WetGrass"
        
        Returns:
        A tuple (entailed, inference_order):
            - entailed: True if `query` can be derived, False otherwise.
            - inference_order: The sequence in which new symbols were inferred.
    """
    inferred = set() # tracks which symbols we've already processed
    agenda = deque(facts) # is a queue of symbols to explore; seeded with the initial facts
    inference_order = [] # records the exact order we derive new symbols
    
    count: Dict[str, int] = {} # tracks how many clauses each symbol appears in
    clause_map: Dict[str, List[Tuple[List[str], str]]] = defaultdict(list) # maps symbols to clauses that derive them

    # Initialize count and clause_map
    for clause in clauses:
        if "=>" in clause:
            lhs, rhs = clause.split("=>") # Split into left-hand side (premises) and right-hand side (conclusion)
            # A & B & ...  →  ["A", "B", ...]
            premises = [p.strip() for p in lhs.split("&")]
            conclusion = rhs.strip()
            key = f"{'&'.join(premises)} => {conclusion}"
            # initliaze how many premises are unmet
            count[key] = len(premises)
            # For each premise symbol, note that this clause is waiting on it
            for prem in premises:
                clause_map[prem].append((premises, conclusion))

    # Main Forward-chaining loop
    while agenda:
        symbol = agenda.popleft() # take next symbol to process
        # if this symbol already handled then skip
        if symbol in inferred:
            continue

        # mark it as inferred, and record in order list
        inferred.add(symbol)
        inference_order.append(symbol)

        # Fire any clause that mentions this symbol as a premise
        for premises, conclusion in clause_map.get(symbol, []):
            # Re-create the clause key to decrement its unmet-premise count
            key = f"{'&'.join(premises)} => {conclusion}"
            count[key] -= 1
            # If all premises of this clause are now satisfied, infer the conclusion
            if count[key] == 0 and conclusion not in inferred:
                # add the newly inferred symbol into the agenda
                agenda.append(conclusion)
    
    # entailed? = did we infer the query symbol?, inference_order = full derivation sequence
    return (query in inferred), inference_order 

    
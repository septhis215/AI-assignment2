import sys
from typing import List, Tuple

def parse_problem_file(filename: str) -> Tuple[List[str], List[str], str]:
    """
    Reads a file with TELL and ASK sections.
    Returns:
      - tell_clauses: list of raw clause strings
      - facts: list of atomic fact symbols
      - query: the ASK symbol
    """
    tell_clauses: List[str] = []
    facts: List[str] = []
    query: str = ""
    section = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            token = line.upper()
            if token == "TELL":
                section = "TELL"
                continue
            elif token == "ASK":
                section = "ASK"
                continue
            if section == "TELL":
                # Clauses or facts
                if "=>" in line or "&" in line:
                    tell_clauses.append(line)
                else:
                    facts.append(line)
            elif section == "ASK":
                query = line
    return tell_clauses, facts, query

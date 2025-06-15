import argparse
from parser import parse_problem_file
from algorithm import FC, BC, TT, RES  

def main():
    parser = argparse.ArgumentParser(
        description="Inference Engine: TT | FC | BC | RES"
    )
    parser.add_argument("filename", help="TELL/ASK input file")
    parser.add_argument(
        "method", help="TT, FC, BC, or RES (case-insensitive)"
    )
    args = parser.parse_args()
    method = args.method.upper()
    clauses, facts, query = parse_problem_file(args.filename)

    if method == "TT":
        entailed, count = TT.tt(clauses, facts, query)
        print(f"YES: {count}" if entailed else "NO")

    elif method == "FC":
        entailed, order = FC.fc(clauses, facts, query)
        print("YES: " + ", ".join(order) if entailed else "NO")

    elif method == "RES":
        entailed, proof = RES.pl_resolution(clauses, facts, query)
        print("YES: " + ", ".join(proof) if entailed else "NO")

    else:  # BC
        entailed, proof = BC.bc(clauses, facts, query)
        print("YES: " + ", ".join(proof) if entailed else "NO")

if __name__ == "__main__":
    main()
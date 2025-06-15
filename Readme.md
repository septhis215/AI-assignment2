# Inference Engine — Truth Table, Forward Chaining, Backward Chaining

This project implements a propositional logic inference engine in Python. It supports:

- **Truth Table Checking (TT)** — for general propositional logic
- **Forward Chaining (FC)** — for Horn clause knowledge bases
- **Backward Chaining (BC)** — for Horn clause queries

---

## Features

✅ Parses TELL/ASK statements from input text files  
✅ Supports propositional logic syntax:

- `~` for negation (¬)
- `&` for conjunction (∧)
- `||` for disjunction (∨)
- `=>` for implication (⇒)
- `<=>` for biconditional (⇔)

✅ Inference Methods:

- **TT**: General KB inference using model enumeration
- **FC**: Horn clause inference using agenda-based forward chaining
- **BC**: Horn clause inference using recursive backward chaining

---

RUN IN Command Prompt (CMD)
iengine <filename> <method>

Example:
iengine test\simple1.txt FC
iengine test\complex1.txt TT

RUN IN POWERSHELL
.\iengine <filename> <method>

Example:
.\iengine test\simple1.txt FC
.\iengine test\complex1.txt TT

📄 Test Files - yan yang
✅ 4 simple\*.txt — for FC and BC
These files use only Horn clauses (no negation, disjunction, or biconditional).
Use them to test Forward Chaining (FC) or Backward Chaining (BC) methods.

✅ complex\*.txt — for TT
These files use general propositional logic, including ~, ||, <=>.
Use them only for the Truth Table (TT) method.

© 2025 - Ng Yong Lin / 104842772 | Teh Yan Yang / 104809625

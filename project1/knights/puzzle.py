from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0 (A = Knave)
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(Not(And(AKnight, AKnave)), Not(AKnight))
)

# Puzzle 1 (A = Knave, B = Knight)
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Not(And(AKnave, BKnave)),
    Not(AKnight),
    Not(BKnave), 
    Implication(Not(AKnight), AKnave),
    Or(BKnight, BKnave)
)

# Puzzle 2 (A = Knave, B = Knight)
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Implication(Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))), BKnight),   #if different kinds = true, b not lying
    Implication(Or(And(AKnight, BKnight), And(AKnave, BKnave)), BKnave),         #if same kinds = true, b lying
    Implication(BKnave, AKnave),                                                 #if b is lying, a has to be lying
    Biconditional(BKnight, AKnave),                                              #only reasonable solution left lol
)

# Puzzle 3 (A = Knight, B = Knave, C = Knight)
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    Implication(BKnave, AKnight),           #if b is lying, a is not lying 
    Implication(BKnave, CKnight),           #if b is lying, c is not lying
    Implication(BKnight, CKnave),           #if b is not lying, c is lying
    Implication(BKnight, Not(AKnave)),      #if b is lying, a can NEITHER BE A KNIGHT NOR A KNAVE
    Implication(BKnight, Not(AKnight)),
    Implication(CKnave, AKnave)             #if c is lying, a is lying
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()



class Symbol:
    def __init__(self, name):
        self.name = name

    def content(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name

    def __len__(self):
        return 1

class Operators:
    def __init__(self):
        pass

    def content(self):
        return self.c

    def __repr__(self):
        return str(self)

    def set_content(self, c):
        self.content = c

    def nested(self):
        return self

    def distribute(self):
        return self

    def __len__(self):
        return len(self.content())

    def eliminate(self):
        return self

    def __iter__(self):
        c = self.content()
        if type(c) in [Symbol]:
            c = [c]
        return iter(c)

    def update_content(self, a):
        """
        Thing is, content is usually a list. However, NOT's the exception.
        """
        if type(self) is NOT:
            a = a[0]
        self.c = a
        self.inf_update()

    def inf_update(self):
        self.inf_avail = True


class NOT(Operators):
    def __init__(self, p):
        super().__init__()
        clause = False
        if type(p) is not Symbol:
            clause = True
        self.isclause = clause
        self.c = p
        self.inf_avail = type(self.c) in [NOT, AND, OR] if self.isclause else False

    def inf_update(self):
        self.inf_avail = type(self.c) in [NOT, AND, OR] if self.isclause else False

    def __str__(self):
        out = "¬"+str(self.content())
        if self.isclause:
            out = f"¬({self.content()})"
        return out

    def __len__(self):
        return 1

    def content(self):
        return self.c

    def double_negation(self):
        return self.content().content()

    def deMorgan(self):
        return OR(*[NOT(p) for p in self.content().content()])

    def reverseDeMorgan(self):
        return AND(*[NOT(p) for p in self.content().content()])

    def __iter__(self):
        return iter([self.content()])

    def infer(self):
        if not self.inf_avail:
            return self
        actions = {
            NOT: self.double_negation,
            AND: self.deMorgan,
            OR: self.reverseDeMorgan,
            Symbol: lambda : self
        }
        try:
            return actions[type(self.content())]()
        except KeyError:
            raise ValueError(f"Can't call inference on {type(self.content())} with inner content {self.content()}")


class AND(Operators):
    def __init__(self, *args):
        super().__init__()
        self.c = list(args)
        self.inf_avail = any([type(i) is AND for i in self.content()])

    def inf_update(self):
        self.inf_avail = any([type(i) is AND for i in self.content()])

    # Currently, I don't see how this type of inference leads to the
    # conjunctive normal form; it makes things a disjuction of conjuctions

    def nested(self):
        old = self.content()
        for i in range(len(old)):
            if type(old[i]) == AND:
                val = old[i].content()
                del old[i]
                old = [val[0]] + old + val[1:]
        return AND(*old)

    def __str__(self):
        out = ""
        c = self.content()
        for i in c:
            if type(i) not in [NOT, Symbol]:
                out += f"({str(i)}) ∧ "
            else:
                out += str(i) + " ∧ "
        return out[:-3]


class OR(Operators):
    def __init__(self, *args):
        super().__init__()
        self.c = list(args)
        self.inf_avail = any([type(i) in [AND, OR] for i in self.content()])

    def inf_update(self):
        self.inf_avail = any([type(i) in [AND, OR] for i in self.content()])

    def __str__(self):
        out = ""
        c = self.content()
        for i in c:
            if type(i) not in [NOT, Symbol]:
                out += f"({str(i)}) ∨ "
            else:
                out += str(i) + " ∨ "
        return out[:-3]

    def nested(self):
        old = self.content()
        for i in range(len(old)):
            if type(old[i]) == OR:
                val = old[i].content()
                del old[i]
                old = [val[0]] + old + val[1:]
        return OR(*old)

    def distribute(self):
        """
        Assumes there are no NOT operators
        Also Assumes there are no nested OR operators
        """
        if not any([type(i) is AND for i in self.content()]):
            return self
        def clause_distr(out, clause):
            content = [clause] if type(clause) in [Symbol, NOT] else clause.content()
            if not out:
                return content
            elif type(out) in [NOT, Symbol]:
                out = [out]
            new_out = []
            for i in content:
                new_out += [base+[i] if (type(base) not in [Symbol, NOT]) else [base]+[i] for base in out]
            return new_out
        out = []
        c = self.content()
        for i in c:
            out = clause_distr(out, i)
        for j in range(len(out)):
            out[j] = OR(*out[j])
        return AND(*out)


class Biconditional(Operators):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        self.inf_avail = True

    def content(self):
        return [self.a, self.b]

    def __len__(self):
        return 2

    def __str__(self):
        x = [f"({str(i)})" if type(i) is not Symbol else str(i) for i in [self.a, self.b]]
        return f"{x[0]} ↔ {x[1]}"

    def eliminate(self):
        return AND(Implication(self.a, self.b), Implication(self.b, self.a))


class Implication(Operators):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        self.inf_avail = True

    def content(self):
        return [self.a, self.b]

    def __len__(self):
        return 2

    def __str__(self):
        x = [f"({str(i)})" if (type(i) not in [Symbol, NOT]) else str(i) for i in [self.a, self.b]]
        return f"{x[0]} → {x[1]}"

    def eliminate(self):
        return OR(NOT(self.a), self.b)


# Function that converts statements into their conjuctive normal form
# The conjunctive normal form is a conjuction of disjuctions.
def CNF(statement):
    def scour(statement, cls, scouring_f):
        # print("scouring", statement, "type", type(statement).__name__, "required", cls.__name__)
        # if nothing to do, return as is
        if type(statement) is Symbol:
            # print("\tsymbol; returning")
            return statement
        elif type(statement) is cls:  # otherwise hit
            # print("found! before:", statement)
            statement = scouring_f(statement)
            # print("after", statement, "type after", type(statement).__name__)
            if type(statement) is Symbol:
                return statement
        # Go through each of the elements inside the class, looking for the target
        # print("\tbreakdown; looking at", [str(i) for i in statement], "inside type", type(statement).__name__)
        c = [scour(i, cls, scouring_f) for i in statement]
        # print("\t\tscour done, result", [str(i) for i in c])
        # Update contents
        statement.update_content(c)
        # print("\t\tupdated vals")

        # Remove nested items
        statement = statement.nested()

        # Remove double negation

        # print("\t\tcleaned nests")
        # print("\t\treturning")
        return statement

    #Related to Biconditionals and Implications
    level_1 = [Biconditional, Implication]
    # print("Attempting to convert the following to CNF", statement)
    for sub_level in level_1:
        # print("\tRemoving", sub_level.__name__, "...")
        statement = scour(statement, sub_level, sub_level.eliminate)
        # print("\tResult")
        # print(statement)

    # print("\tNow NOT")
    # Related to NOT
    statement = scour(statement, NOT, NOT.infer)
    # Finally apply the OR implications
    # print(statement, "before")
    statement = scour(statement, OR, OR.distribute)

    return statement



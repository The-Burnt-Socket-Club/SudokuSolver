

class Symbol:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class NOT:
    def __init__(self, p):
        clause = False
        if type(p) is not Symbol:
            clause = True
        self.isclause = clause
        self.p = p
        self.inf_avail = type(p) in [NOT, AND, OR] if self.isclause else False

    def __str__(self):
        out = "¬"+str(self.content())
        if self.isclause:
            out = f"¬({self.content()})"
        return out

    def content(self):
        return self.p

    def double_negation(self):
        return self.content().content()

    def deMorgan(self):
        return OR(*[NOT(p) for p in self.content().content()])

    def reverseDeMorgan(self):
        return AND(*[NOT(p) for p in self.content().content()])

    def infer(self):
        actions = {
            NOT: self.double_negation,
            AND: self.deMorgan,
            OR: self.reverseDeMorgan
        }
        try:
            return actions[type(self.content())]()
        except KeyError:
            raise ValueError(f"Can't call inference on {NOT} with inner content {self.content()}")


class AND:
    def __init__(self, *args):
        self.p = list(args)
        self.inf_avail = any([type(i) is AND for i in self.content()])

    def content(self):
        return self.p

    # Currently, I don't see how this type of inference leads to the
    # conjunctive normal form; it makes things a disjuction of conjuctions
    def distribute(self):
        pass

    def and_extraction(self):
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


class OR:
    def __init__(self, *args):
        self.p = list(args)
        self.inf_avail = any([type(i) in [AND, OR] for i in self.content()])

    def __str__(self):
        out = ""
        c = self.content()
        for i in c:
            if type(i) not in [NOT, Symbol]:
                out += f"({str(i)}) ∧ "
            else:
                out += str(i) + " ∨ "
        return out[:-3]

    def content(self):
        return self.p

    def nested_ors(self):
        old = self.content()
        for i in range(len(old)):
            if type(old[i]) == OR:
                val = old[i].content()
                del old[i]
                old = [val[0]] + old + val[1:]
        return OR(*old)

    def distribute_or(self):
        """
        Assumes there are no NOT operators
        Also Assumes there are no nested OR operators
        """
        def clause_distr(out, clause):
            content = [clause] if type(clause) is Symbol else clause.content()
            if not out:
                return content
            new_out = []
            for i in content:
                new_out += [base+[i] if type(base) is not Symbol else [base]+[i] for base in out]
            return new_out
        out = []
        c = self.content()
        for i in c:
            out = clause_distr(out, i)
        for j in range(len(out)):
            out[j] = OR(*out[j])
        return AND(*out)



x = [Symbol(i) for i in "abcdefgh"]
y = OR(AND(x[3], x[0]), AND(x[1], x[2]))
print(y)
print(y.distribute_or())



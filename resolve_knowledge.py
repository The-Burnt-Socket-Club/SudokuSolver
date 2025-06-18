
from operations import CNF, NOT, Symbol, OR


class Clause:
    def __init__(self, propositions: list):
        self.p = propositions

    def __len__(self):
        return len(self.p)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "OR("+", ".join([str(i) for i in self.sentence()])+")"

    def sentence(self):
        return self.p

    def isMatch(self, a, b):
        print("\tinside isMatch", type(a), type(b))
        print("\tvals:", a, b, "content", a.content(), b.content())
        if type(a) == type(b):
            return a.content() == b.content()

    def add(self, a):
        if not self.inside(a):
            self.p.append(a)

    def inside(self, a):
        """
        Checks if a is inside self
        Returns bool
        """
        print("\tGoing to see if", a, "is inside", self)
        for i in self.sentence():
            print("\telement in self", i, a)
            if self.isMatch(i, a):
                print("Match! return")
                return True
            print("\tno match\n")
        return False


    def merge(self, other):
        s, o = self.sentence(), other.sentence()
        print(s, o, "things to be merged")
        for i in s:
            print("considering", i)
            n = NOT(i).infer()
            print("not is", n)
            print("checking if", n, "is in", repr(o), n in o)
            if other.inside(n):
                print("\tit is")
                m = Clause([])
                unwanted = Clause([n, i])
                print("here's what's not wanted", unwanted)
                for j in o+s:
                    if not unwanted.inside(j):
                        m.add(j)
                return m
            print(False)
        return None

    def __iter__(self):
        return iter(self.sentence())


class KnowledgeBase:
    def __init__(self, *args, KB=None):
        """
        Idea that args is a series of parameters, each a list with
        a non-zero number of propositional symbols and operators
        """
        if KB is not None:
            self.knowledge = KB
        else:
            k = []
            for i in args:
                if len(i) == 1:
                    k.append(Clause([i]))
                elif len(i) > 1:
                    k.append(Clause(i.content()))
            self.knowledge = list(sorted(k, key=lambda x: len(x)))


    def add(self, sentence):
        sentence = CNF(sentence)
        if sentence not in self.KB():
            if len(sentence) == 1:
                self.knowledge.append(Clause([sentence]))
            elif len(sentence) > 1:
                self.knowledge.append(Clause(sentence.content()))
        self.knowledge = list(sorted(self.knowledge, key=lambda x: len(x)))

    def KB(self):
        return self.knowledge

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.KB())

    def __str__(self):
        return " ∧ ".join([str(i) for i in self.KB()])

    def pop(self):
        assert self.knowledge
        out = self.knowledge[0]
        del self.knowledge[0]
        return out

    def remove(self, index):
        del self.knowledge[index]



def resolve(kb: KnowledgeBase, p=None):
    """
    Assumes kb to be an instance of KnowledgeBase.
    """
    if p is not None:
        print("\tadding", p, "to k")
        print("before:", kb)
        kb.add(p)
        print("after:", kb)
    # get the smallest clause
    knowledge_base = kb.KB()
    if not knowledge_base:
        return None
    elif len(knowledge_base) == 1:
        return knowledge_base
    c = kb.pop()
    # check other clauses for a potential merger
    for other in range(len(knowledge_base)):
        m = c.merge(knowledge_base[other])
        print("\tvalue returned from merge", m)
        if m is not None:
            kb.remove(other)
            if len(m):
                if len(m) == 1:
                    kb.add(m.sentence()[0])
                else:
                    kb.add(OR(*m.sentence()))
                print("new kb after merge", kb)
            else:
                return None
            return resolve(kb, p=None)
        print("conjuctions with no similar elements - KB:", kb)
    base = resolve(kb).append(c)
    kb = KnowledgeBase(KB=base)
    return knowledge_base



# x = [Symbol(i) for i in "abcdefghi"]
# k = KnowledgeBase(
#         OR(x[0], x[1], x[2]),
#         NOT(x[0]),
#         NOT(x[4]),
#         NOT(x[7]),
#         OR(NOT(x[2]), NOT(x[5]), NOT(x[8]))
#     )
# for i in k.KB():
#     print(type(i.sentence()), "type clause")
# # blah = k.KB()
# print("here's the CNF form of the KB")
# print(k)

# print(resolve(k))

# c1 = k.KB()[0]
# c2 = k.KB()[1]
# for i in c1:
#     print("\tis", NOT(i), "inside", c2)
#     print(c2.inside(NOT(i)))

# print(c1.merge(c2))

# pos = []
# first_layer = resolve(k)
# fls = []
# if first_layer is not None:
#     elems = first_layer[0].sentence()
#     for sym in first_layer[0].sentence():
#         fls.append(first_layer)
#         pos.append((resolve(KnowledgeBase(KB=first_layer), p=NOT(sym)), sym))
# print([(True, value) if (value[0] is None) else ("Maybe", value) for value in pos])
# print(fls)
# pos = []
# for sym in x:
#     if resolve(k, NOT(sym)) is None:
#         pos.append(True)
#     else:
#         pos.append("Maybe")
# print(pos)






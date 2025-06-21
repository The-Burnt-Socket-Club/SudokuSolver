
from operations import CNF, NOT, Symbol, OR, Implication, AND


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
        # print("\tinside isMatch", type(a), type(b))
        # print("\tvals:", a, b, "content", a.content(), b.content())
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
        # print("\tGoing to see if", a, "is inside", self)
        for i in self.sentence():
            # print("\telement in self", i, a)
            if self.isMatch(i, a):
                # print("Match! return")
                return True
            # print("\tno match\n")
        return False


    def merge(self, other):
        s, o = self.sentence(), other.sentence()
        # print(s, o, "things to be merged")
        for i in s:
            # print("considering", i)
            n = NOT(i).infer()
            # print("not is", n)
            # print("checking if", n, "is in", repr(o), n in o)
            if other.inside(n):
                # print("\tit is")
                m = Clause([])
                unwanted = Clause([n, i])
                # print("here's what's not wanted", unwanted)
                for j in o+s:
                    if not unwanted.inside(j) and not m.inside(j):
                        m.add(j)
                return m
            # print(False)
        return None

    def __iter__(self):
        return iter(self.sentence())


class KnowledgeBase:
    def __init__(self, *args, KB=None):
        """
        Idea that args is a series of parameters, each a list with
        a non-zero number of propositional symbols and operators
        """
        args = list(args)
        if KB is not None:
            self.knowledge = KB
        else:
            k = []
            for i in args:
                i = CNF(i)
                if type(i) is AND:
                    i = i.content()
                    args.extend(i[1:])
                    i = i[0]
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

    def direct_add(self, sentence):
        self.knowledge.append(sentence)
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
        # print("\tadding", p, "to k")
        # print("before:", kb)
        kb.add(p)
        # print("after:", kb)
    # get the smallest clause
    knowledge_base = kb.KB()
    if not knowledge_base:
        return None
    elif len(knowledge_base) == 1:
        return kb
    # print("currently considering", kb)
    c = kb.pop()
    # check other clauses for a potential merger
    for other in range(len(knowledge_base)):
        m = c.merge(knowledge_base[other])
        # print("\tvalue returned from merge", m)
        if m is not None:
            kb.remove(other)
            if len(m):
                if len(m) == 1:
                    kb.add(m.sentence()[0])
                else:
                    kb.add(OR(*m.sentence()))
                # print("new kb after merge", kb)
            else:
                return None
            return resolve(kb)
        # print("conjuctions with no similar elements - KB:", kb)
    # print("element", c, "couldn't be merged with anything, running sub-process")
    kb = resolve(kb)
    kb.direct_add(c)
    # print("output from subprocess -", kb)
    return kb


# Here are the relevant symbols for this:
x = [Symbol(i) for i in "KC"]
# The following commented block is based on the following puzzle:
# An advertisement for a tennis magazine says, If I'm not playing tennis, I'm
#watching tennis. And if I'm not watching tennis, I'm reading about tennis.
#Assume that the speaker can only do one activity at once. What is the speaker
#doing?
# k = KnowledgeBase(
#         Implication(NOT(x[0]), x[1]),
#         Implication(NOT(x[1]), x[2]),
#         NOT(AND(x[0], x[1])),
#         NOT(AND(x[0], x[2])),
#         NOT(AND(x[1], x[2])),
#         OR(x[0], x[1], x[2])
# )

# And here is another riddle:
# There are two tribes of trolls, the Glums and the Plogs. Glums are all
# truthtellers and Plogs are all liars. You meet two trolls one day, Kim and
# Coin. Kim says "We are from different clans." Coin says "Kim is a liar."
# Which tribe is Kim from and which tribe is Coin from?

if __name__ == "__main__":
    x = [
        Implication(x[0], NOT(x[1])),
        Implication(x[1], NOT(x[0]))
    ]
    k = KnowledgeBase(*x)

    print([CNF(i) for i in x])
    print(k)
    print(resolve(k))


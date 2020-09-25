import xilema.types as xt
import random


class PersonGenerator:
    def __init__(self):
        self.names = {}
        self.surnames = []
        self.ages = []
        self.sexes = []

        self.wishes = []
        self.opportunities = []
        self.likes = []
        self.hates = []
        self.props_range = range(1, 1)
        return

    def setNames(self, sex: xt.Sex, names: list):
        self.names[sex] = names

    def setSurnames(self, surnames: list):
        self.surnames = surnames

    def setAges(self, ages: list):
        self.ages = ages

    def setSexes(self, sexes: list):
        self.sexes = sexes

    def setWishes(self, wishes: list):
        self.wishes = wishes

    def setOpportunities(self, opportunities: list):
        self.opportunities = opportunities

    def setLikes(self, likes: list):
        self.likes = likes

    def setHates(self, hates: list):
        self.hates = hates

    def setRangeOfProperties(self, props_range: range):
        self.props_range = props_range

    def generate(self, count: int):
        res = []

        for i in range(1, count):
            sex = random.choice(self.sexes)
            name = random.choice(self.names[sex])
            surname = random.choice(self.surnames)
            age = random.choice(self.ages)

            pers = xt.Character(name, surname, sex, age)

            for i in range(random.choice(self.props_range)):
                prop = xt.Property(random.choice(self.wishes),
                                   random.choice(range(1, 3)))
                pers.addWish(prop)

            for i in range(random.choice(self.props_range)):
                prop = xt.Property(random.choice(
                    self.opportunities), random.choice(range(1, 3)))
                pers.addOpportunity(prop)

            for i in range(random.choice(self.props_range)):
                prop = xt.Property(random.choice(self.likes),
                                   random.choice(range(1, 3)))
                pers.addLike(prop)

            for i in range(random.choice(self.props_range)):
                prop = xt.Property(random.choice(
                    self.hates), random.choice(range(1, 3)))
                pers.addHate(prop)

            res.append(pers)

        return res

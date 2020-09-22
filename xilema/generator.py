import xilema.types as xt
import random


class PersonGenerator:
    def __init__(self):
        self.names = {}
        self.surnames = []
        self.ages = []
        self.sexes = []
        return

    def setNames(self, sex: xt.Sex, names: list):
        self.names[sex] = names

    def setSurnames(self, surnames: list):
        self.surnames = surnames

    def setAges(self, ages: list):
        self.ages = ages

    def setSexes(self, sexes: list):
        self.sexes = sexes

    def generate(self, count: int):
        res = []

        for i in range(1, count):
            sex = random.choice(self.sexes)
            name = random.choice(self.names[sex])
            surname = random.choice(self.surnames)
            age = random.choice(self.ages)
            res.append(xt.Character(name, surname, sex, age))

        return res

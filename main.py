import xilema.types as xt
import xilema.cluster as xc
import xilema.generator as xg
import xilema.database as xd
import xilema.clope
import math
import random


def gen_transaction(elems: list, num: int):
    res = []
    for i in range(0, num):
        res.append(random.choice(elems))
    return res


if __name__ == "__main__":

    gen = xg.PersonGenerator()

    gen.setSexes([xt.Sex.Male, xt.Sex.Female])
    gen.setNames(xt.Sex.Male, xd.getMaleNames())
    gen.setNames(xt.Sex.Female, xd.getFemaleNames())
    gen.setSurnames(xd.getSurnames())
    gen.setAges(range(18, 65))

    gen.setWishes(xd.getWishlist())
    gen.setOpportunities(xd.getWishlist())
    gen.setLikes(xd.getLikelist())
    gen.setHates(xd.getLikelist())
    gen.setRangeOfProperties(range(3, 10))

    persons = gen.generate(100)

    # clope test
    clope = xilema.clope.CLOPE(2.5)

    for i in range(0, 1000):
        trans = gen_transaction(
            xd.getLikelist()[:20], random.choice(range(3, 10)))
        clope.addTransaction(trans)

    for i in range(0, 100):
        iter_res = clope.optimizeIteration(0)
        if not iter_res:
            break

    '''
    def search_filter(p1: xt.Character, p2: xt.Character):
        if abs(p1.age - p2.age) > 10:
            return False
        if p1.sex == p2.sex:
            return False
        return True

    best_duals = xc.findBestDuals(persons, search_filter)

    print(best_duals)
    '''

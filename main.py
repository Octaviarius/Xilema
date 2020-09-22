import xilema.types as xt
import xilema.cluster as xc
import xilema.generator as xg
import xilema.database as xd


if __name__ == "__main__":

    gen = xg.PersonGenerator()

    gen.setSexes([xt.Sex.Male, xt.Sex.Female])
    gen.setNames(xt.Sex.Male, xd.getMaleNames())
    gen.setNames(xt.Sex.Female, xd.getFemaleNames())
    gen.setSurnames(xd.getSurnames())
    gen.setAges(range(18, 65))

    persons = gen.generate(100)

    cluster = xc.Cluster()

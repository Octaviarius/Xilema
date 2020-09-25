import xilema.types as xt
import xilema.utils as xu


def calcCategoryMetric(dic1: dict, dic2: dict):
    all_elems = set(dic1.keys()) | set(dic2.keys())
    both_elems = set(dic1.keys()) & set(dic2.keys())

    all_value = 0.0
    both_value = 0.0

    # calc value for all elements
    all_value = all_elems.__len__()

    # calc value for both elements
    for e in both_elems:
        e1 = dic1[e]
        e2 = dic2[e]
        if e1.weight <= e2.weight:
            both_value = both_value + e1.weight / e2.weight
        else:
            both_value = both_value + e2.weight / e1.weight
    return both_value / all_value


def findBestDuals(persons: [xt.Character], filter=lambda p1, p2: True):
    p1_idx = 0

    p1_best = None
    p2_best = None
    metric_max = 0.0

    for p1 in persons:
        p1_idx = p1_idx + 1

        for p2 in persons[p1_idx:]:

            if not filter(p1, p2):
                continue

            like_vs_hate_metric1 = calcCategoryMetric(
                p1.like_dict, p2.hate_dict)
            like_vs_hate_metric2 = calcCategoryMetric(
                p2.like_dict, p1.hate_dict)

            like_vs_like_metric = calcCategoryMetric(
                p1.like_dict, p2.like_dict)
            hate_vs_hate_metric = calcCategoryMetric(
                p2.hate_dict, p1.hate_dict)

            metric = (like_vs_like_metric + hate_vs_hate_metric) - \
                (like_vs_hate_metric1 + like_vs_hate_metric2)

            if metric > metric_max:
                p1_best = p1
                p2_best = p2
                metric_max = metric

    return (p1_best, p2_best, metric_max)


class Cluster:
    def __init__(self):
        self.wish_dict = {}
        self.opportunity_dict = {}
        self.like_dict = {}
        self.hate_dict = {}
        self.character_list = []

    def integrateDict(dic_target, dic):
        for v in dic.values():
            elem = dic_target.get(v.name, xt.Property(v.name, 0.0))
            elem.weight = elem.weight + v.weight
            dic_target[v.name] = elem

    def excludeDict(dic_target: dict, dic: dict):
        for v in dic.values():
            elem = dic_target.get(v.name, None)
            if elem != None:
                elem.weight = elem.weight - v.weight
                if abs(elem.weight) < 0.0001:
                    del dic_target[v.name]

    def addCharacter(self, char: xt.Character):
        self.character_list.append(char)
        integrateDict(self.wish_dict, char.wish_dict)
        integrateDict(self.opportunity_dict, char.opportunity_dict)
        integrateDict(self.like_dict, char.like_dict)
        integrateDict(self.hate_dict, char.hate_dict)

    def getWishList(self):
        return self.wish_dict.values()

    def getOpportunityList(self):
        return self.opportunity_dict.values()

    def getLikeList(self):
        return self.like_dict.values()

    def getHateList(self):
        return self.hate_dict.values()

    def addWish(self, wish: xt.Property):
        for w in xu.listify(wish):
            self.wish_dict.update({w.name: w})

    def addOpportunity(self, opportunity: xt.Property):
        for o in xu.listify(opportunity):
            self.opportunity_dict.update({o.name: o})

    def addLike(self, like: xt.Property):
        for l in xu.listify(like):
            self.like_dict.update({l.name: l})

    def addHate(self, hate: xt.Property):
        for u in xu.listify(hate):
            self.hate_dict.update({u.name: u})

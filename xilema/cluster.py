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


def findBestDuals(persons: [xt.Character]):
    p1_idx = 0

    p1_best = None
    p2_best = None
    metric_max = 0.0

    for p1 in persons:
        p1_idx = p1_idx + 1

        for p2 in persons[p1_idx:]:

            if p1.sex == p2.sex:
                continue

            wish_vs_opport_metric1 = calcCategoryMetric(
                p1.wish_dict, p2.opportunity_dict)
            wish_vs_opport_metric2 = calcCategoryMetric(
                p2.wish_dict, p1.opportunity_dict)

            like_vs_unlike_metric1 = calcCategoryMetric(
                p1.like_dict, p2.unlike_dict)
            like_vs_unlike_metric2 = calcCategoryMetric(
                p2.like_dict, p1.unlike_dict)

            like_vs_like_metric = calcCategoryMetric(
                p1.like_dict, p2.like_dict)
            unlike_vs_unlike_metric = calcCategoryMetric(
                p2.unlike_dict, p1.unlike_dict)

            metric = (wish_vs_opport_metric1 + wish_vs_opport_metric2) - \
                (like_vs_unlike_metric1 + like_vs_unlike_metric2) + \
                (like_vs_like_metric + unlike_vs_unlike_metric)

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
        self.unlike_dict = {}
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
        integrateDict(self.unlike_dict, char.unlike_dict)

    def getWishList(self):
        return self.wish_dict.values()

    def getOpportunityList(self):
        return self.opportunity_dict.values()

    def getLikeList(self):
        return self.like_dict.values()

    def getUnlikeList(self):
        return self.unlike_dict.values()

    def addWish(self, wish: xt.Property):
        for w in xu.listify(wish):
            self.wish_dict.update({w.name: w})

    def addOpportunity(self, opportunity: xt.Property):
        for o in xu.listify(opportunity):
            self.opportunity_dict.update({o.name: o})

    def addLike(self, like: xt.Property):
        for l in xu.listify(like):
            self.like_dict.update({l.name: l})

    def addUnlike(self, unlike: xt.Property):
        for u in xu.listify(unlike):
            self.unlike_dict.update({u.name: u})

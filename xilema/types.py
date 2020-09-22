import enum
import xilema.utils as xu


class Sex(enum.IntEnum):
    Undef = 0
    Male = 1
    Female = 2


class PropList(enum.Enum):
    Wish = 0
    Opportunity = 1
    Like = 2
    Unlike = 3


class Property:
    def __init__(self, name='', weight: float = 1.0):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return '{name:%s, weight:%i}' % (self.name, self.weight)


class Character:
    def __init__(self, name='', surname='', sex: Sex = Sex.Undef, age: int = 0):
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex

        self.wish_dict = {}
        self.opportunity_dict = {}
        self.like_dict = {}
        self.unlike_dict = {}

    def __repr__(self):
        return '{name:%s, sur:%s, sex:%s, age:%i}' % (self.name, self.surname, self.sex, self.age)

    def rename(self, name, surname):
        self.name = name
        self.surname = surname

    def setAge(self, age):
        self.age = age

    def getWishList(self):
        return self.wish_dict.values()

    def getOpportunityList(self):
        return self.opportunity_dict.values()

    def getLikeList(self):
        return self.like_dict.values()

    def getUnlikeList(self):
        return self.unlike_dict.values()

    def addWish(self, wish: Property):
        for w in xu.listify(wish):
            self.wish_dict.update({w.name: w})

    def addOpportunity(self, opportunity: Property):
        for o in xu.listify(opportunity):
            self.opportunity_dict.update({o.name: o})

    def addLike(self, like: Property):
        for l in xu.listify(like):
            self.like_dict.update({l.name: l})

    def addUnlike(self, unlike: Property):
        for u in xu.listify(unlike):
            self.unlike_dict.update({u.name: u})

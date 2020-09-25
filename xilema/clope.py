import math


class Cluster:
    def __init__(self, repulsion=2.0):
        self.transactions = []
        self.square = int(0)
        self.width = int(0)
        self.height = 0.0
        self.repulsion = repulsion
        self.trans_count = int(0)
        self.records = {}

    def addTransaction(self, transaction: list):
        for t in transaction:
            if self.records.get(t, None) == None:
                self.width = self.width + 1
                self.records[t] = int(1)
            else:
                self.records[t] = self.records[t] + int(1)

        self.transactions.append(transaction)
        self.square = self.square + len(transaction)
        self.trans_count = self.trans_count + int(1)
        self.height = self.square / math.pow(self.width, self.repulsion)

    def removeTransaction(self, transaction: list):
        for t in transaction:
            v = int(self.records.get(t, 0))
            v = v - 1

            if int(v) <= 0:
                self.width = self.width - int(1)
                self.records.pop(t)
            else:
                self.records[t] = v

        self.square = self.square - len(transaction)
        self.transactions.remove(transaction)
        self.trans_count = self.trans_count - 1

        if self.width <= 0:
            self.height = 0.0
        else:
            self.height = self.square / math.pow(self.width, self.repulsion)

    def deltaAdd(self, transaction: list):
        new_width = self.width
        new_square = self.square + len(transaction)

        for t in transaction:
            if self.records.get(t, None) == None:
                new_width = new_width + 1
                continue

        new_cost = new_square * (self.trans_count + 1) / \
            math.pow(new_width, self.repulsion)
        old_cost = 0.0

        if int(self.width) >= 1:
            old_cost = self.square * self.trans_count / \
                math.pow(self.width, self.repulsion)

        return new_cost - old_cost

    def deltaRemove(self, transaction: list):
        new_width = self.width
        new_square = self.square - len(transaction)

        for t in transaction:
            if self.records.get(t, 0) == 1:
                new_width = new_width - 1

        new_cost = 0.0
        if new_width != 0:
            new_cost = new_square * (self.trans_count - 1) / \
                math.pow(new_width, self.repulsion)

        old_cost = 0.0
        if int(self.width) >= 1:
            old_cost = self.square * self.trans_count / \
                math.pow(self.width, self.repulsion)

        return new_cost - old_cost


class CLOPE:
    def __init__(self, repulsion=2.0):
        self.clusters = []
        self.repulsion = repulsion

    def addTransaction(self, transaction: list):
        opt_add = self.findOptimumAdd(transaction)
        target_cluster = opt_add[0]
        is_new = opt_add[1]

        target_cluster.addTransaction(transaction)

        if is_new:
            self.clusters.append(target_cluster)

        return target_cluster

    def findOptimumAdd(self, transaction: list):
        target_cluster = Cluster(self.repulsion)
        max_cost = target_cluster.deltaAdd(transaction)
        is_new = True

        for c in self.clusters:
            cost = c.deltaAdd(transaction)
            if cost > max_cost:
                is_new = False
                max_cost = cost
                target_cluster = c

        return (target_cluster, is_new)

    def optimizeIteration(self, cost_threshold: float = 0.0):
        is_moved = False

        for c_rem in self.clusters:
            for t in c_rem.transactions:
                cost_remove = c_rem.deltaRemove(t)

                cost_add = -100000000.0
                cluster_add = c_rem

                for c_add in self.clusters:
                    if c_rem == c_add:
                        cost = -cost_remove
                    else:
                        cost = c_add.deltaAdd(t)
                        if cost > cost_add:
                            cost_add = cost
                            cluster_add = c_add

                if cluster_add == c_rem:
                    continue
                elif cost_add + cost_remove > cost_threshold:
                    is_moved = True
                    c_rem.removeTransaction(t)

                    if c_rem.trans_count == 0:
                        self.clusters.remove(c_rem)

                    cluster_add.addTransaction(t)

        return is_moved

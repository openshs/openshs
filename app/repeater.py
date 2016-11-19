import csv
from random import randint
from math import floor, ceil
import sys


class Repeater():
    """
    Given a csv reader of the dataset, this class repeats the dataset and
    construct new random dataset
    """
    def __init__(self, dataset, alpha=0, hasheader=True):
        try:
            if alpha > 1.0 or alpha < 0:
                raise TypeError
            self.alpha = alpha
            self.dataset = dataset
            self.data = [l for l in self.dataset]
            if hasheader:
                self.keys = self.data[0]
                self.data = self.data[1:]
            self.pat_ts, self.pattern = self.extractPats()
            self.total_time = len(self.data)
            self.init_state = self.data[0]
            self.last_margin = 0
        except TypeError:
            print("Type Error: dataset must be iterable and alpha must be less than 1 and greater than 0.")
            sys.exit(-1)

    @staticmethod
    def diffLists(l1, l2):
        """returns a list of tuples of the index and the old and new values of
        the difference between the two lists"""
        if len(l1) != len(l2):
            raise ValueError("Lists are of different sizes")

        if (len(l1) == 0) or (len(l2) == 0):
            raise ValueError("Lists cannot be empty")

        if (not isinstance(l1, list)) or (not isinstance(l1, list)):
            raise TypeError("Expecting a list")

        return [(i, j, k) for i, (j, k) in enumerate(zip(l1, l2)) if j != k]

    def extractPats(self):
        """returns the pattern's timestamp AND a list of lists of tuples that
        represent the patterns in the data"""
        li = []
        ts = []
        temp = self.data[0]
        for i, row in enumerate(self.data):
            diffItem = self.diffLists(temp, row)
            if diffItem:
                li.append([x for x in diffItem])
                ts.append(i)
                temp = row
        return ts, li

    # @staticmethod
    def marginCalc(self, pat_idx, total_time, num_pats):
        try:
            bucket_size = total_time // num_pats
            sub_margin = bucket_size - floor(bucket_size * self.alpha)
            bucket_size -= sub_margin
            if self.last_margin == 0:
                if sub_margin == 0:
                    left_margin = self.last_margin
                elif bucket_size == 0:
                    left_margin = pat_idx
                else:
                    s = ceil(pat_idx / bucket_size)
                    left_margin = pat_idx - s
            else:
                left_margin = self.last_margin

            right_margin = left_margin + bucket_size
            right_margin -= 1

            return left_margin, right_margin
        except ZeroDivisionError:
            print("Error: Too many changes in the sensors and not enough data to generate new replications.")
            sys.exit(-1)

    def randomizePos(self):
        """returns a list of random positions for the patterns spanning the
        whole time"""
        num_pats = len(self.pattern)
        dist = []
        for pi in self.pat_ts:
            leftMargin, rightMargin = self.marginCalc(pi, self.total_time, num_pats)
            # print(str(pi) + " L=" + str(leftMargin) + " R=" + str(rightMargin))
            # leftMargin = floor(leftMargin * self.alpha)
            # rightMargin = floor(rightMargin * self.alpha)
            # dist.append(randint(pi - leftMargin, pi + rightMargin))
            if leftMargin >= rightMargin:
                dist.append(pi)
            else:
                dist.append(randint(leftMargin, rightMargin))
            self.last_margin = rightMargin + 1
        return dist

    def consData(self):
        "constructs a dataset given the inital states and the pattern"
        dataSet = []
        patSet = []

        temp = self.init_state[:]

        for p in self.pattern:
            for e in p:
                temp[e[0]] = e[2]
            patSet.append(list(temp))

        curRow = self.init_state[:]
        randPos = self.randomizePos()

        for i in range(self.total_time):
            if i in randPos:
                curRow = patSet.pop(0)
            dataSet.append(curRow)

        return dataSet


if __name__ == '__main__':

    f = open("temp/temp_dataset.csv", "r")
    r = csv.reader(f)
    obj = Repeater(r)
    obj.consData()
    f.close()

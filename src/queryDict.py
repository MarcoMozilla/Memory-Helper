
import random

class QueryDict(dict):

    def p(self):
        print(self)
        print(self.__dict__)

    def __init__(self, d):

        super().__init__(d)
        self.keys = set(self.keys())

        self.last = [None, None]
        if len(self) == 2:
            self.last = [None]
        elif len(self) == 1:
            self.last = []

    def randkey(self):
        #print(self.keys)
        value = random.sample(self.keys, 1)[0]
        if self.last != [] and value in self.last and len(self.keys) > 1:
            self.keys.remove(value)
            new_value = random.sample(self.keys, 1)[0]
            self.keys.add(value)
            value = new_value
        if self.last != []:
            self.last = [value] + self.last[:-1]
        return value

    def _tracksub(self):
        if len(self) <= 2:
            self.last = self.last[:-1]

    def _trackadd(self):
        if 2 <= len(self) <= 3:
            self.last += [None]

    def __setitem__(self, key, value):
        self.keys.add(key)
        c1 = len(self)
        super().__setitem__(key, value)
        c2 = len(self)
        if c2 > c1:
            self._trackadd()

    def __delitem__(self, key):
        self.keys.remove(key)
        super().__delitem__(key)
        self._tracksub()

    def pop(self, key):
        key = super().pop(key)
        self.keys.remove(key)
        self._tracksub()
        return key

    def popitem(self):
        key, item = super().popitem()
        self.keys.remove(key)
        self._tracksub()
        return key, item


if __name__ == '__main__':
    d = {1:2,2:3,3:4}
    a =QueryDict(d)
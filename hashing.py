from primality import next_prime
from avl import AVLTree


class BaseHash:
    def __init__(self, th, base_element):
        self.table = [base_element for i in range(th)]
        self.th = th

    def __str__(self):
        return str(self.table)

    def hash_function(self, x):
        return x % len(self.table)


class AVLOpenHash(BaseHash):
    def __init__(self, th):
        super().__init__(th, None)
        self.tree = AVLTree()

    def add(self, value):
        pos = self.hash_function(value)
        self.table[pos] = self.tree.add(value, self.table[pos])

    def search(self, value):
        pos = self.hash_function(value)
        return pos, self.tree.search(self.table[pos], value)

    def delete(self, value):
        pos, root = self.search(value)
        if(root is not None):
            self.table[pos].delete(self.table[pos], value)

    @property
    def load_factor(self):
        load = 0
        for root in self.table:
            if(self.tree.get_height(root) > load):
                load = self.tree.get_height(root)
        return load

    @property
    def balance_factor(self):
        soma = 0
        for root in self.table:
            soma += self.tree.get_height(root)

        return soma / (self.th * self.load_factor)


class ListOpenHash(BaseHash):
    def __init__(self, th):
        super().__init__(th, [])

    def add(self, value):
        pos = self.hash_function(value)
        self.table[pos].append(value)

    def search(self, value):
        pos = self.hash_function(value)
        try:
            return pos, self.table[pos].index(value)
        except ValueError:
            return -1

    def delete(self, value):
        pos = self.search(value)
        if(pos != -1):
            self.table[pos[0]].remove(value)

    @property
    def load_factor(self):
        load = 0
        for list_item in self.table:
            if(len(list_item) > load):
                load = len(list_item)
        return load

    @property
    def balance_factor(self):
        soma = 0
        for setlist in self.table:
            soma += (self.load_factor - len(setlist))

        return soma / (self.th * self.load_factor)


class LinearClosedHash(BaseHash):
    def __init__(self, th):
        super().__init__(th, None)

    def add(self, value):
        for i in range(self.th):
            pos = self.hash_function(value + i)
            if(self.table[pos] is None):
                self.table[pos] = value
                break

    def search(self, value):
        for i in range(self.th):
            pos = self.hash_function(value + i)
            if(self.table[pos] == value):
                return pos

        return -1

    def delete(self, value):
        pos = self.search(value)
        if(pos != -1):
            self.table[pos] = None


class SquareClosedHash(BaseHash):
    def __init__(self, th):
        super().__init__(th, None)

    @property
    def num_elements(self):
        num = 0
        for element in self.table:
            if(element is not None):
                num += 1

        return num

    @property
    def can_add(self):
        return self.num_elements < int(self.th / 2) + 1

    def add(self, value):
        if(self.can_add):
            for i in range(int(self.th / 2) + 1):
                pos = self.hash_function(value + i ** 2)
                if(self.table[pos] is None):
                    self.table[pos] = value
                    break

    def search(self, value):
        for i in range(int(self.th / 2) + 1):
            pos = self.hash_function(value + i ** 2)
            if(self.table[pos] == value):
                return pos

        return -1

    def delete(self, value):
        pos = self.search(value)
        if(pos != -1):
            self.table[pos] = None


class DoubleRClosedHash(BaseHash):
    def __init__(self, th):
        super().__init__(th, None)
        self.r = next_prime(self.th / 2)

    def hd(self, n):
        return self.r - (n % self.r)

    def add(self, value):
        for i in range(1, self.r + 1):
                pos = self.hash_function(i * self.hd(value))
                if(pos is None):
                    self.table[pos] = value
                    break


class HalfOpenHash(BaseHash):
    def __init__(self, th):
        super().__init__(th, None)

    def rehash(self):
        new_th = next_prime(self.th * 2)
        new_table = [None for i in range(new_th)]
        for item in self.table:
            if(item is not None):
                for i in range(int(new_th / 2) + 1):
                    pos = (item + i ** 2) % new_th
                    if(new_table[pos] is None):
                        new_table[pos] = item
                        break
        self.table = new_table
        self.th = new_th

    @property
    def num_elements(self):
        num = 0
        for element in self.table:
            if(element is not None):
                num += 1

        return num

    @property
    def can_add(self):
        return self.num_elements < int(self.th / 2) + 1

    def add(self, value):
        if(not self.can_add):
            self.rehash()

        for i in range(int(self.th / 2) + 1):
            pos = self.hash_function(value + i ** 2)
            if(self.table[pos] is None):
                self.table[pos] = value
                break

    def search(self, value):
        for i in range(int(self.th / 2) + 1):
            pos = self.hash_function(value + i ** 2)
            if(self.table[pos] == value):
                return pos

        return -1

    def delete(self, value):
        pos = self.search(value)
        if(pos != -1):
            self.table[pos] = None

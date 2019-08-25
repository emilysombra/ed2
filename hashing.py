from primality import next_prime


class BaseHash:
    def __init__(self, th, base_element):
        self.table = [base_element for i in range(th)]
        self.th = th

    def __str__(self):
        return str(self.table)

    def hash_function(self, x):
        return x % len(self.table)


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

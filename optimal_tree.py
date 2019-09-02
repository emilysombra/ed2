from tree import TreeNode


def generate_matrix(m, n):
    return [[None for x in range(n)] for y in range(m)]


class OptimalTree:
    def __init__(self, values, frequency_errors):
        n = len(values)
        self.n = n
        self.values = [None]
        self.f = [None]
        self.f_ = frequency_errors
        for value, frequency in values:
            self.values.append(value)
            self.f.append(frequency)
        self.c = generate_matrix(n + 1, n + 1)
        self.F = generate_matrix(n + 1, n + 1)
        self.k = generate_matrix(n + 1, n + 1)
        self.low_cost()
        self.root = self.generate_optimal(0, n)

    def low_cost(self):
        n = len(self.values)
        for j in range(n):
            self.c[j][j] = 0
            self.F[j][j] = self.f_[j]
        for d in range(1, n + 1):
            for i in range(n - d):
                j = i + d
                self.F[i][j] = self.F[i][j - 1] + self.f[j] + self.f_[j]
                cost = 9223372036854775808  # 2 ^ 63
                min_k = -1
                for k in range(i + 1, j + 1):
                    temp = self.c[i][k - 1] + self.c[k][j] + self.F[i][j]
                    if(temp < cost):
                        cost = temp
                        min_k = k
                self.c[i][j] = cost
                self.k[i][j] = min_k

    def generate_optimal(self, i, j):
        ind_k = self.k[i][j]
        if(ind_k is not None):
            root = TreeNode(self.values[self.k[i][j]])
            root.left = self.generate_optimal(i, ind_k - 1)
            root.right = self.generate_optimal(ind_k, j)
            return root
        else:
            return None

    def search(self, root, value):
        current = self.root
        while(current is not None):
            if(value == root.value):
                break
            elif(value < root.value):
                current = current.left
            else:
                current = current.right

        return current

    def preorder(self, root):
        if(root is None):
            return '--'
        temp = str(root.value) + ' '
        temp += self.preorder(root.left) + ' '
        temp += self.preorder(root.right)
        while('  ' in temp):
            temp.replace('  ', ' ')
        return temp

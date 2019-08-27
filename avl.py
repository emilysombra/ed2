class TreeNode:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None
        self.height = 1

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


class AVLTree:
    def add_list(self, values, root):
        for value in values:
            root = self.add(value, root)
        return root

    def add(self, value, root=None):
        # Adding element (regular BST insertion)
        if(root is None):
            return TreeNode(value)
        if(value == root.value):
            return root
        elif(value < root.value):
            root.left = self.add(value, root.left)
        else:
            root.right = self.add(value, root.right)

        # update height
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        balance = self.get_balance(root)
        # doing rotation
        if(balance > 1 and value < root.left.value):
            return self.rotate_right(root)
        elif(balance < -1 and value > root.right.value):
            return self.rotate_left(root)
        elif(balance > 1 and value > root.left.value):
            return self.asym_rotate_left(root)
        elif(balance < -1 and value < root.right.value):
            return self.asym_rotate_right(root)

        return root

    def get_height(self, root):
        if(root is None):
            return 0

        return root.height

    def get_balance(self, root):
        if(root is None):
            return 0

        return self.get_height(root.left) - self.get_height(root.right)

    def rotate_right(self, k2):
        k1 = k2.left
        b = k1.right

        k1.right = k2
        k2.left = b

        k2.height = 1 + max(self.get_height(k2.left),
                            self.get_height(k2.right))
        k1.height = 1 + max(self.get_height(k1.left),
                            self.get_height(k1.right))
        return k1

    def rotate_left(self, k1):
        k2 = k1.right
        b = k2.left

        k2.left = k1
        k1.right = b

        k1.height = 1 + max(self.get_height(k1.left),
                            self.get_height(k1.right))
        k2.height = 1 + max(self.get_height(k2.left),
                            self.get_height(k2.right))
        return k2

    def asym_rotate_left(self, k3):
        k1 = k3.left
        k2 = k1.right
        b = k2.left
        c = k2.right

        k2.left = k1
        k1.right = b
        k2.right = k3
        k3.left = c

        k1.height = 1 + max(self.get_height(k1.left),
                            self.get_height(k1.right))
        k2.height = 1 + max(self.get_height(k2.left),
                            self.get_height(k2.right))
        k3.height = 1 + max(self.get_height(k3.left),
                            self.get_height(k3.right))

        return k2

    def asym_rotate_right(self, k1):
        k3 = k1.right
        k2 = k3.left
        b = k2.left
        c = k2.right

        k2.left = k1
        k1.right = b
        k2.right = k3
        k3.left = c

        k1.height = 1 + max(self.get_height(k1.left),
                            self.get_height(k1.right))
        k2.height = 1 + max(self.get_height(k2.left),
                            self.get_height(k2.right))
        k3.height = 1 + max(self.get_height(k3.left),
                            self.get_height(k3.right))

        return k2

    def preorder(self, root):
        if(root is None):
            return '--'
        temp = str(root.value) + ' '
        temp += self.preorder(root.left) + ' '
        temp += self.preorder(root.right)
        while('  ' in temp):
            temp.replace('  ', ' ')
        return temp

    def to_list(self, root):
        if(root is None):
            return list(set())
        base = {root.value}
        base.update(self.to_list(root.left))
        base.update(self.to_list(root.right))
        return list(base)

    def search(self, root, value):
        if(root is None):
            return None
        if(value == root.value):
            return root
        elif(value < root.value):
            return self.search(root.left, value)
        else:
            return self.search(root.right, value)

    def delete(self, root, value):
        if(root is None):
            return root

        if(value == root.value):
            lista = self.to_list(root.right)
            return self.add_list(lista, root.left)
        elif(value < root.value):
            root.left = self.delete(root.left, value)
        else:
            root.right = self.delete(root.right, value)
        # update height
        try:
            left_height = self.get_height(root.left)
        except AttributeError:
            left_height = 0
        try:
            right_height = self.get_height(root.right)
        except AttributeError:
            right_height = 0
        root.height = 1 + max(left_height, right_height)
        # check the balance
        balance = self.get_balance(root)
        # doing rotation
        if(balance > 1):
            root = self.rotate_right(root)
            new_balance = self.get_balance(root)
            if(new_balance < -1):
                root = self.asym_rotate_right(root)
        elif(balance < -1):
            root = self.rotate_left(root)
            new_balance = self.get_balance(root)
            if(new_balance > 1):
                root = self.asym_rotate_left(root)

        return root


if __name__ == '__main__':
    tree = AVLTree()
    root = tree.add_list([10, 5, 15, 7, 3], None)
    print(tree.preorder(root))
    root = tree.delete(root, 5)
    print(tree.preorder(root))
    print(tree.get_height(root))

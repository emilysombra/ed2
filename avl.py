class TreeNode:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def add(self, root, value):
        # Adding element (regular BST insertion)
        if(root is None):
            return TreeNode(value)
        elif(value == root.value):
            return root
        elif(value < root.value):
            root.left = self.add(root.left, value)
        else:
            root.right = self.add(root.right, value)

        # update height
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        balance = self.get_balance(root)
        # doing rotation
        if(balance > 1 and value < root.value):
            return self.rotate_right(root)
        elif(balance < -1 and value > root.value):
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
        return temp


if __name__ == '__main__':
    tree = AVLTree()
    root = None
    root = tree.add(root, 3)
    print(tree.preorder(root))
    root = tree.add(root, 8)
    print(tree.preorder(root))
    root = tree.add(root, 9)
    print(tree.preorder(root))
    root = tree.add(root, 4)
    print(tree.preorder(root))
    root = tree.add(root, 16)
    print(tree.preorder(root))
    root = tree.add(root, 17)
    print(tree.preorder(root))
    root = tree.add(root, 13)
    print(tree.preorder(root))
    root = tree.add(root, 7)
    print(tree.preorder(root))
    root = tree.add(root, 12)
    print(tree.preorder(root))

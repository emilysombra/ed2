from tree import TreeNode


class SplayTree:
    def add_list(self, values, root):
        for value in values:
            root = self.add(value, root)
        return root

    def add(self, value, root):
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

    def get_height(self, root):
        if(root is None):
            return 0

        return root.height

    def preorder(self, root):
        if(root is None):
            return '--'
        temp = str(root.value) + ' '
        temp += self.preorder(root.left) + ' '
        temp += self.preorder(root.right)
        while('  ' in temp):
            temp.replace('  ', ' ')
        return temp

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

    def search(self, root, value):
        pass

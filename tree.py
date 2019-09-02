class TreeNode:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None
        self.height = 1

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

class FibonacciHeap:

    class Node:
        def __init__(self, key):
            self.key = key
            self.parent = self.child = self.prev = self.next = None
            self.degree = 0
            self.mark = False
        
        def __str__(self):
            return f"({self.key})"

    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    def is_empty(self):
        return self.root_list == None

    root_list, min_node = None, None

    total_nodes = 0

    def find_min(self):
        return self.min_node

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                for x in self.iterate(z.child):
                    self.merge_with_root_list(x)
                    x.parent = None
            self.remove_from_root_list(z)
            if z == z.right:
                self.min_node = self.root_list = None
            else:
                self.min_node = z.right
                self.consolidate()
            self.total_nodes -= 1
        return z.key

    def insert(self, key):
        n = self.Node(key)
        n.left = n.right = n
        self.merge_with_root_list(n)
        if self.min_node is None or n.key < self.min_node.key:
            self.min_node = n
        self.total_nodes += 1
        return n

    def decrease_key(self, x, k):
        if k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    def merge(self, h2):
        H = FibonacciHeap()
        H.root_list, H.min_node = self.root_list, self.min_node

        last = h2.root_list.left
        h2.root_list.left = H.root_list.left
        H.root_list.left.right = h2.root_list
        H.root_list.left = last
        H.root_list.left.right = H.root_list

        if h2.min_node.key < H.min_node.key:
            H.min_node = h2.min_node
        
        H.total_nodes = self.total_nodes + h2.total_nodes
        return H

    def cut(self, x, y):
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_root_list(x)
        x.parent = None
        x.mark = False

    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def consolidate(self):
        A = [None] * self.total_nodes
        for x in self.iterate(self.root_list):
            d = x.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        for a in A:
            if a is not None:
                if a.key < self.min_node.key:
                    self.min_node =a

    def heap_link(self, y, x):
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    def merge_with_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def remove_from_root_list(self, node):
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left

    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left

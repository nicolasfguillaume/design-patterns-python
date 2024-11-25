class Node:
  def __init__(self, value, left=None, right=None):
    self.right = right
    self.left = left
    self.value = value

    self.parent = None

    if left:
      self.left.parent = self
    if right:
      self.right.parent = self

  def __iter__(self):
    return InOrderIterator(self)


class InOrderIterator:
  def __init__(self, root):
    self.root = self.current = root
    self.yielded_start = False
    while self.current.left:
      self.current = self.current.left

  def __next__(self):
    if not self.yielded_start:
      self.yielded_start = True
      return self.current

    if self.current.right:
      self.current = self.current.right
      while self.current.left:
        self.current = self.current.left
      return self.current
    else:
      p = self.current.parent
      while p and self.current == p.right:
        self.current = p
        p = p.parent
      self.current = p
      if self.current:
        return self.current
      else:
        raise StopIteration

def traverse_in_order(root):
  # Inner function to recursively traverse the tree in order
  def traverse(current):
    """Recursive generator function that performs an in-order traversal of the binary tree.
       In-order traversal visits nodes in the following order: left subtree, current node, right subtree.
       This ensures that nodes are visited in ascending order for binary search trees."""
    # If the current node has a left child, it recursively traverses the left subtree first.
    if current.left:
      for left in traverse(current.left):
        yield left
    # After traversing the left subtree, it yields the current node.
    yield current
    # If the current node has a right child, it recursively traverses the right subtree next.
    if current.right:
      for right in traverse(current.right):
        yield right
  
  # Start the traversal from the root and yield each node in in-order sequence.
  for node in traverse(root):
    yield node



if __name__ == '__main__':
  #   1
  #  / \
  # 2   3

  # in-order: 213
  # preorder: 123
  # postorder: 231

  root = Node(1,
              Node(2),
              Node(3))

  it = iter(root)

  print([next(it).value for x in range(3)])

  for x in root:
    print(x.value)

  for y in traverse_in_order(root):
    print(y.value)
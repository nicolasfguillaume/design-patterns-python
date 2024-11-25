# Iterator Coding Exercise

# Given the following definition of a Node , please implement preorder traversal right inside Node. 
# The sequence returned should be the sequence of values, not their containing nodes.

  #   1
  #  / \
  # 2   3

  # in-order: 213
  # preorder: 123
  # postorder: 231

import unittest


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

#   def traverse_preorder(self):
#     # This function performs a preorder traversal of a binary tree.
#     # Preorder traversal visits nodes in the following order: root, left subtree, right subtree.
#     #   1
#     #  / \
#     # 2   3
#     # preorder: 123

#     def traverse(current):
#       yield current
#       if current.left:
#         for left in traverse(current.left):
#             yield left
#       if current.right:
#         for right in traverse(current.right):
#           yield right

#     for node in traverse(self):
#       yield node.value

  # equivalent solution, using yield from
  def traverse_preorder(self):
    # This function performs a preorder traversal of a binary tree.
    # Preorder traversal visits nodes in the following order: root, left subtree, right subtree.

    # Yield the value of the current node (root).
    yield self.value
    # If the current node has a left child, recursively traverse the left subtree.
    if self.left:
        yield from self.left.traverse_preorder()
    # If the current node has a right child, recursively traverse the right subtree.
    if self.right:
        yield from self.right.traverse_preorder()


class TestSuite(unittest.TestCase):
  def test_exercise_1(self):
    #   1
    #  / \
    # 2   3
    # preorder: 123
    root = Node(1, 
                Node(2), 
                Node(3))
    self.assertEqual([1, 2, 3], [x for x in root.traverse_preorder()])

  def test_exercise_2(self):
    #   1
    #  / \
    # 2   3
    #    / \
    #   4   5
    # preorder: 12345
    child = Node(3, 
                 Node(4), 
                 Node(5))
    root = Node(1, 
                Node(2), 
                child)
    self.assertEqual([1, 2, 3, 4, 5], [x for x in root.traverse_preorder()])

  def test_exercise_3(self):
    #     1
    #    / \
    #   2   3
    #  / \
    # 4   5
    # preorder: 12453
    child = Node(2, 
                 Node(4), 
                 Node(5))
    root = Node(1,
                child,
                Node(3))
    self.assertEqual([1, 2, 4, 5, 3], [x for x in root.traverse_preorder()])

if __name__ == "__main__":
  unittest.main(exit=False)

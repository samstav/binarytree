"""Binary trees please."""

from __future__ import print_function

import itertools
import json
import random


def randint(begin=1, end=100):
    """Return a random int in the begin/end range."""
    return random.randrange(begin, end)


def gen_tree(depth=3, iterable=None):

    """Generate binary tree of specified depth.

    If 'iterable' is supplied, the values of the
    nodes will be sourced from the iterable. Otherwise,
    random integers are used for node values

    The Tree is built beginning at the leaf nodes,
    working its way to the root of the tree.

    Items from 'iterable' are placed in this order:

           6
         4   5
        0 1 2 3

    Example:

        gen_tree(depth=4, iterable=[a, b, c, d, e, f, g, h])

                   g
               e       f
             a   b   c   d
            a b c d e f g h


    """
    if not iterable:
        iterable = (f() for f in itertools.repeat(randint))
    iterable = itertools.cycle(iter(iterable))

    count = sum(2**x for x in xrange(depth))
    if count < 1:
        return
    row = [BinaryTree(next(iterable)) for _ in xrange(2**(depth-1))]
    while len(row) != 1:
        row = [BinaryTree(next(iterable), left=left, right=right) for
               left, right in itertools.izip(row[::2], row[1::2])]
    return row[0]


class Null(Exception):

    """Tree branch points to nothing."""


class BinaryTree(object):

    """Binary Tree implementation."""

    def __init__(self, value, left=None, right=None):
        """Initialize the tree, a value is required."""
        self.value = value
        self._left = left
        self._right = right

    def __eq__(self, other):
        """Determine if the 'other' tree is equivalent to self."""
        if self is other:
            return True

        if not isinstance(other, BinaryTree):
            return False

        if self.value != other.value:
            return False

        if self.is_leaf != other.is_leaf:
            return False

        return self._left == other._left and self._right == other._right

    def __contains__(self, other):
        """Return True if 'other' is a subtree of self."""
        if other == self:
            return True
        try:
            isin = other in self.left
        except Null:
            isin = False
        if not isin:
            try:
                isin = other in self.right
            except Null:
                isin = False
        return isin

    def __iter__(self):
        """Yield key-value pairs for dict()."""
        yield 'value', self.value
        if self._left is not None:
            yield 'left', dict(self.left)
        if self._right is not None:
            yield 'right', dict(self.right)
        raise StopIteration()

    @property
    def is_leaf(self):
        """Return True if this is a leaf node, False otherwise."""
        return not self._left and not self._right

    @property
    def left(self):
        """The left child tree of this node."""
        if self._left is None:
            raise Null("Left child of %s is null." % self._inst)
        return self._left

    @property
    def right(self):
        """The right child tree of this node."""
        if self._right is None:
            raise Null("Right child of %s is null." % self._inst)
        return self._right

    @property
    def _inst(self):
        """Return the object-type-at-memory-location string."""
        return '<%r at %s>' % (self, hex(id(self)))

    @property
    def pretty(self):
        """Create a somewhat 'pretty' representation of the tree."""
        return json.dumps(dict(self), sort_keys=True,
                          indent=6, separators=(',', ' --> '))

    def __repr__(self):
        """Return the object repr, excluding left/right if they are null."""
        inst = '%s(%s' % (self.__class__.__name__, self.value)
        if self._left is not None:
            inst += ', left=%s' % self.left
        if self._right is not None:
            inst += ', right=%s' % self.right
        inst += ')'
        return inst


class AutoBinaryTree(BinaryTree):

    """Binary tree that lazily grows on the fly.

    Instantiation requires a seed value.
    """

    @property
    def left(self):
        """Auto-populate the 'left' attribute if it doesn't exist."""
        if not self._left:
            self._left = self.__class__(randint())
        return self._left

    @property
    def right(self):
        """Auto-populate the 'right' attribute if it doesn't exist."""
        if not self._right:
            self._right = self.__class__(randint())
        return self._right


if __name__ == '__main__':

    print(gen_tree(depth=randint(3, 7)).pretty)

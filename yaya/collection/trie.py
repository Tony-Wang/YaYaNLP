__author__ = 'tony'
__all__ = ['Trie', 'StringTrie', 'SortedTrie', 'SortedStringTrie', 'Node']

import sys
from copy import copy
from operator import itemgetter
from collections import MutableMapping

# Python 3 interoperability
PY3 = sys.version_info[0] == 3
if PY3:
    def itervalues(d):
        return d.values()


    def iteritems(d):
        return d.items()
else:
    def itervalues(d):
        return d.itervalues()


    def iteritems(d):
        return d.iteritems()


# Singleton sentinel - works with pickling
class NULL(object):
    pass


class Node(object):
    '''Trie node class.

    Subclasses may extend it to replace :attr:`ChildrenFactory` with a different
    mapping class (e.g. `sorteddict <http://pypi.python.org/pypi/sorteddict/>`_).

    :ivar value: The value of the key corresponding to this node or :const:`NULL`
        if there is no such key.
    :ivar children: A ``{key-part : child-node}`` mapping.
    '''
    __slots__ = ('value', 'children')

    #: A callable for creating a new :attr:`children` mapping.
    ChildrenFactory = dict

    def __init__(self, value=NULL):
        self.value = value
        self.children = self.ChildrenFactory()

    def numkeys(self):
        '''Return the number of keys in the subtree rooted at this node.'''
        return (int(self.value is not NULL) +
                sum(child.numkeys() for child in itervalues(self.children)))

    def __repr__(self):
        return '(%s, {%s})' % (
            self.value is NULL and 'NULL' or repr(self.value),
            ', '.join('%r: %r' % t for t in iteritems(self.children)))

    def __copy__(self):
        clone = self.__class__(self.value)
        clone_children = clone.children
        for key, child in iteritems(self.children):
            clone_children[key] = child.__copy__()
        return clone

    def __getstate__(self):
        return (self.value, self.children)

    def __setstate__(self, state):
        self.value, self.children = state


class Trie(MutableMapping):
    '''Base trie class.

    As with regular dicts, keys are not necessarily returned sorted. Use
    :class:`SortedTrie` if sorting is required.
    '''

    #: Callable for forming a key from its parts.
    KeyFactory = tuple

    #: Callable for creating new trie nodes.
    NodeFactory = Node

    def __init__(self, *args, **kwargs):
        '''Create a new trie.

        Parameters are the same with ``dict()``.
        '''
        self._root = self.NodeFactory()

        self.update(*args, **kwargs)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        '''Create a new trie with keys from ``iterable`` and values set to ``value``.

        Parameters are the same with ``dict.fromkeys()``.
        '''
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    # ----- trie-specific methods -----------------------------------------------

    def longest_prefix(self, key, default=NULL):
        '''Return the longest key in this trie that is a prefix of ``key``.

        If the trie doesn't contain any prefix of ``key``:
          - if ``default`` is given, return it
          - otherwise raise ``KeyError``
        '''
        try:
            return self.longest_prefix_item(key)[0]
        except KeyError:
            if default is not NULL:
                return default
            raise

    def longest_prefix_value(self, key, default=NULL):
        '''Return the value associated with the longest key in this trie that is
        a prefix of ``key``.

        If the trie doesn't contain any prefix of ``key``:
          - if ``default`` is given, return it
          - otherwise raise ``KeyError``
        '''
        current = self._root
        longest_prefix_value = NULL
        for part in key:
            current = current.children.get(part)
            if current is None:
                break
            value = current.value
            if value is not NULL:
                longest_prefix_value = value
        if longest_prefix_value is not NULL:
            return longest_prefix_value
        elif default is not NULL:
            return default
        else:
            raise KeyError

    def longest_prefix_item(self, key, default=NULL):
        '''Return the item (``(key,value)`` tuple) associated with the longest
        key in this trie that is a prefix of ``key``.

        If the trie doesn't contain any prefix of ``key``:
          - if ``default`` is given, return it
          - otherwise raise ``KeyError``
        '''
        prefix = []
        append = prefix.append
        current = self._root
        longest_prefix_value = NULL
        max_non_null_index = -1
        for i, part in enumerate(key):
            current = current.children.get(part)
            if current is None:
                break
            append(part)
            value = current.value
            if value is not NULL:
                longest_prefix_value = value
                max_non_null_index = i
        if longest_prefix_value is not NULL:
            del prefix[max_non_null_index + 1:]
            return (self.KeyFactory(prefix), longest_prefix_value)
        elif default is not NULL:
            return default
        else:
            raise KeyError

    def iter_prefixes(self, key):
        'Return an iterator over the keys of this trie that are prefixes of ``key``.'
        key_factory = self.KeyFactory
        prefix = []
        append = prefix.append
        node = self._root
        for part in key:
            node = node.children.get(part)
            if node is None:
                break
            append(part)
            if node.value is not NULL:
                yield key_factory(prefix)

    def iter_prefix_values(self, key):
        '''Return an iterator over the values of this trie that are associated
        with keys that are prefixes of ``key``.
        '''
        node = self._root
        for part in key:
            node = node.children.get(part)
            if node is None:
                break
            if node.value is not NULL:
                yield node.value

    def iter_prefix_items(self, key):
        '''Return an iterator over the items (``(key,value)`` tuples) of this
        trie that are associated with keys that are prefixes of ``key``.
        '''
        key_factory = self.KeyFactory
        prefix = []
        append = prefix.append
        node = self._root
        for part in key:
            node = node.children.get(part)
            if node is None:
                break
            append(part)
            if node.value is not NULL:
                yield (key_factory(prefix), node.value)

    # ----- extended mapping API methods ----------------------------------------

    def keys(self, prefix=None):
        '''Return a list of this trie's keys.

        :param prefix: If not None, return only the keys prefixed by ``prefix``.
        '''
        return list(self.iterkeys(prefix))

    def values(self, prefix=None):
        '''Return a list of this trie's values.

        :param prefix: If not None, return only the values associated with keys
            prefixed by ``prefix``.
        '''
        return list(self.itervalues(prefix))

    def items(self, prefix=None):
        '''Return a list of this trie's items (``(key,value)`` tuples).

        :param prefix: If not None, return only the items associated with keys
            prefixed by ``prefix``.
        '''
        return list(self.iteritems(prefix))

    def iterkeys(self, prefix=None):
        '''Return an iterator over this trie's keys.

        :param prefix: If not None, yield only the keys prefixed by ``prefix``.
        '''
        return (key for key, value in self.iteritems(prefix))

    def itervalues(self, prefix=None):
        '''Return an iterator over this trie's values.

        :param prefix: If not None, yield only the values associated with keys
            prefixed by ``prefix``.
        '''

        def generator(node, NULL=NULL):
            if node.value is not NULL:
                yield node.value
            for part, child in iteritems(node.children):
                for subresult in generator(child):
                    yield subresult

        if prefix is None:
            node = self._root
        else:
            node = self._find(prefix)
            if node is None:
                node = self.NodeFactory()
        return generator(node)

    def iteritems(self, prefix=None):
        '''Return an iterator over this trie's items (``(key,value)`` tuples).

        :param prefix: If not None, yield only the items associated with keys
            prefixed by ``prefix``.
        '''
        parts = []
        append = parts.append

        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, NULL=NULL):
            if node.value is not NULL:
                yield (key_factory(parts), node.value)
            for part, child in iteritems(node.children):
                append(part)
                for subresult in generator(child):
                    yield subresult
                del parts[-1]

        node = self._root
        if prefix is not None:
            for part in prefix:
                append(part)
                node = node.children.get(part)
                if node is None:
                    node = self.NodeFactory()
                    break
        return generator(node)

    # ----- original mapping API methods ----------------------------------------

    def __len__(self):
        return self._root.numkeys()

    def __iter__(self):
        return self.iterkeys()

    def __contains__(self, key):
        node = self._find(key)
        return node is not None and node.value is not NULL

    def has_key(self, key):
        return key in self

    def __getitem__(self, key):
        node = self._find(key)
        if node is None or node.value is NULL:
            raise KeyError
        return node.value

    def __setitem__(self, key, value):
        node = self._root
        Node = self.NodeFactory
        for part in key:
            next = node.children.get(part)
            if next is None:
                node = node.children.setdefault(part, Node())
            else:
                node = next
        node.value = value

    def __delitem__(self, key):
        nodes_parts = []
        append = nodes_parts.append
        node = self._root
        for part in key:
            append((node, part))
            node = node.children.get(part)
            if node is None:
                break
        if node is None or node.value is NULL:
            raise KeyError
        node.value = NULL
        pop = nodes_parts.pop
        while node.value is NULL and not node.children and nodes_parts:
            node, part = pop()
            del node.children[part]

    def clear(self):
        self._root.children.clear()

    def copy(self):
        clone = copy(super(Trie, self))
        clone._root = copy(self._root)
        return clone

    def __repr__(self):
        return '%s({%s})' % (
            self.__class__.__name__,
            ', '.join('%r: %r' % t for t in self.iteritems()))

    def _find(self, key):
        node = self._root
        for part in key:
            node = node.children.get(part)
            if node is None:
                break
        return node


class StringTrie(Trie):
    '''A more appropriate for string keys :class:`Trie`.'''
    KeyFactory = ''.join


# XXX: quick & dirty sorted dict
# currently only iteritems() (for Python 2) or items() (for Python 3) has to be
# overriden. However this is implementation detail that may change in the future
class _SortedDict(dict):
    if PY3:
        def items(self):
            return iter(sorted(dict.items(self), key=itemgetter(0)))
    else:
        def iteritems(self):
            return iter(sorted(dict.iteritems(self), key=itemgetter(0)))


class _SortedNode(Node):
    ChildrenFactory = _SortedDict


class SortedTrie(Trie):
    '''A :class:`Trie` that returns its keys (and associated values/items) sorted.

    .. note::
        This implementation does not keep the keys sorted internally; instead it
        sorts them every time a method returning a list or iterator (e.g.
        :meth:`keys`) is called. In cases where a trie is relatively stable
        (few inserts/deletes) and is iterated often, it is probably more efficient
        to use a :attr:`NodeFactory` based on a sorted dict such as
        `sorteddict <http://pypi.python.org/pypi/sorteddict/>`_.
    '''
    NodeFactory = _SortedNode


class SortedStringTrie(SortedTrie, StringTrie):
    'A :class:`Trie` that is both a :class:`StringTrie` and a :class:`SortedTrie`.'


if __name__ == '__main__':
    import doctest

    doctest.testmod()

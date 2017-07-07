# -*- coding: utf-8 -*-
import abjad
import collections
import copy


class Tree(abjad.abctools.AbjadObject):
    r'''Tree.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Here's a tree:

        ::

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

        ::

            >>> graph(tree) # doctest: +SKIP

        ::

            >>> tree.get_payload(nested=True)
            [[[0, 1], [2, 3]], [4, 5]]

        ::

            >>> tree.get_payload()
            [0, 1, 2, 3, 4, 5]

    ..  container:: example

        Here's an internal node:

        ::

            >>> tree[1]
            Tree(items=[Tree(items=4), Tree(items=5)])

        ::

            >>> f(tree[1])
            baca.tools.Tree(
                items=[
                    baca.tools.Tree(
                        items=4,
                        ),
                    baca.tools.Tree(
                        items=5,
                        ),
                    ],
                )

        ::

            >>> tree[1].get_payload(nested=True)
            [4, 5]

        ::

            >>> tree[1].get_payload()
            [4, 5]

    ..  container:: example

        Here's a leaf:

        ::

            >>> tree[1][0]
            Tree(items=4)

        ::

            >>> f(tree[1][0])
            baca.tools.Tree(
                items=4,
                )

        ::
        
            >>> tree[1][0].get_payload(nested=True)
            4

        ::

            >>> tree[1][0].get_payload()
            [4]

    ..  container:: example

        Initializes from other trees:

        ::

            >>> tree_1 = baca.Tree(items=[0, 1])
            >>> tree_2 = baca.Tree(items=[2, 3])
            >>> tree_3 = baca.Tree(items=[4, 5])
            >>> tree = baca.Tree(items=[[tree_1, tree_2], tree_3])

        ::

            >>> graph(tree) # doctest: +SKIP

        ..  docs::

            >>> graph_ = tree.__graph__()
            >>> f(graph_)
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="",
                    shape=circle];
                node_1 [label="",
                    shape=circle];
                node_2 [label="",
                    shape=circle];
                node_3 [label="0",
                    shape=box];
                node_4 [label="1",
                    shape=box];
                node_5 [label="",
                    shape=circle];
                node_6 [label="2",
                    shape=box];
                node_7 [label="3",
                    shape=box];
                node_8 [label="",
                    shape=circle];
                node_9 [label="4",
                    shape=box];
                node_10 [label="5",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_8;
                node_1 -> node_2;
                node_1 -> node_5;
                node_2 -> node_3;
                node_2 -> node_4;
                node_5 -> node_6;
                node_5 -> node_7;
                node_8 -> node_9;
                node_8 -> node_10;
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_children',
        '_item_class',
        '_items',
        '_equivalence_markup',
        '_expression',
        '_parent',
        '_payload',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        self._children = []
        self._expression = None
        self._item_class = item_class
        self._parent = None
        self._payload = None
        if self._are_internal_nodes(items):
            items = self._initialize_internal_nodes(items)
        else:
            items = self._initialize_payload(items)
        self._items = items

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when tree contains `argument`.

        ..  container:: example

            Tree contains node:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> for node in tree:
                ...     node
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
                Tree(items=[Tree(items=4), Tree(items=5)])

            ::

                >>> tree[-1] in tree
                True

        ..  container:: example

            Tree does not contain node:

            ::

                >>> tree[-1][-1] in tree
                False

        Returns true or false.
        '''
        return argument in self._children

    def __eq__(self, argument):
        r'''Is true when `argument` is the same type as tree and when the payload
        of all subtrees are equal.

        ..  container:: example

            Is true when subtrees are equal:

            ::

                >>> sequence_1 = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree_1 = baca.Tree(sequence_1)
                >>> sequence_2 = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree_2 = baca.Tree(sequence_2)
                >>> sequence_3 = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree_3 = baca.Tree(sequence_3)

            ::

                >>> tree_1 == tree_1
                True
                >>> tree_1 == tree_2
                True
                >>> tree_1 == tree_3
                False
                >>> tree_2 == tree_1
                True
                >>> tree_2 == tree_2
                True
                >>> tree_2 == tree_3
                False
                >>> tree_3 == tree_1
                False
                >>> tree_3 == tree_2
                False
                >>> tree_3 == tree_3
                True

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            if self._payload is not None or argument._payload is not None:
                return self._payload == argument._payload
            if len(self) == len(argument):
                for x, y in zip(
                    self._noncyclic_children, argument._noncyclic_children):
                    if not x == y:
                        return False
                else:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats tree.

        ..  container:: example

            Formats tree:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> f(tree)
                baca.tools.Tree(
                    items=[
                        baca.tools.Tree(
                            items=[
                                baca.tools.Tree(
                                    items=[
                                        baca.tools.Tree(
                                            items=0,
                                            ),
                                        baca.tools.Tree(
                                            items=1,
                                            ),
                                        ],
                                    ),
                                baca.tools.Tree(
                                    items=[
                                        baca.tools.Tree(
                                            items=2,
                                            ),
                                        baca.tools.Tree(
                                            items=3,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        baca.tools.Tree(
                            items=[
                                baca.tools.Tree(
                                    items=4,
                                    ),
                                baca.tools.Tree(
                                    items=5,
                                    ),
                                ],
                            ),
                        ],
                    )

        Returns string.
        '''
        superclass = super(Tree, self)
        return superclass.__format__(format_specification=format_specification)

    def __getitem__(self, argument):
        r'''Gets node or node slice identified by `argument`.

        ..  container:: example

            Gets node:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> tree[-1]
                Tree(items=[Tree(items=4), Tree(items=5)])

        ..  container:: example

            Gets slice:

            ::

                >>> tree[-1:]
                [Tree(items=[Tree(items=4), Tree(items=5)])]

        Returns node or slice of nodes.
        '''
        return self._children.__getitem__(argument)

    def __graph__(self, **keywords):
        r'''Graphs tree.

        ..  container:: example

            Graphs tree:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> graph(tree) # doctest: +SKIP

            ::

                >>> tree_graph = tree.__graph__()
                >>> f(tree_graph)
                digraph G {
                    graph [bgcolor=transparent,
                        truecolor=true];
                    node_0 [label="",
                        shape=circle];
                    node_1 [label="",
                        shape=circle];
                    node_2 [label="",
                        shape=circle];
                    node_3 [label="0",
                        shape=box];
                    node_4 [label="1",
                        shape=box];
                    node_5 [label="",
                        shape=circle];
                    node_6 [label="2",
                        shape=box];
                    node_7 [label="3",
                        shape=box];
                    node_8 [label="",
                        shape=circle];
                    node_9 [label="4",
                        shape=box];
                    node_10 [label="5",
                        shape=box];
                    node_0 -> node_1;
                    node_0 -> node_8;
                    node_1 -> node_2;
                    node_1 -> node_5;
                    node_2 -> node_3;
                    node_2 -> node_4;
                    node_5 -> node_6;
                    node_5 -> node_7;
                    node_8 -> node_9;
                    node_8 -> node_10;
                }

        Returns Graphviz graph.
        '''
        graph = abjad.graphtools.GraphvizGraph(
            attributes={
                'bgcolor': 'transparent',
                'truecolor': True,
                },
            name='G',
            )
        node_mapping = {}
        for node in self._iterate_depth_first():
            graphviz_node = abjad.graphtools.GraphvizNode()
            if list(node):
                graphviz_node.attributes['shape'] = 'circle'
                graphviz_node.attributes['label'] = ''
            else:
                graphviz_node.attributes['shape'] = 'box'
                graphviz_node.attributes['label'] = str(node._payload)
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node._parent is not None:
                abjad.graphtools.GraphvizEdge().attach(
                    node_mapping[node._parent],
                    node_mapping[node],
                    )
        return graph

    def __hash__(self):
        r'''Hashes tree.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Tree, self).__hash__()

# TODO: make this work without recursion error
#    def __iter__(self):
#        r'''Iterates tree at level -1.
#
#        ..  container:: example
#
#            Gets node:
#
#            ::
#
#                >>> items = [[[0, 1], [2, 3]], [4, 5]]
#                >>> tree = baca.Tree(items=items)
#
#            ::
#
#                >>> tree.__iter__()
#
#        '''
#        return self.iterate(level=-1)

    def __len__(self):
        r'''Gets length of tree.

        ..  container:: example

            Gets length of tree:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> len(tree)
                2

        Defined equal to number of nodes in tree at level 1.

        Returns nonnegative integer.
        '''
        return len(self._children)

    def __repr__(self):
        r'''Gets interpreter representation of tree.

        ..  container:: example

            Gets interpreter representation of tree:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> baca.Tree(items=items)
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

        ..  container:: example

            Gets interpreter representation of leaf:

            ::

                >>> baca.Tree(0)
                Tree(items=0)

        ..  container:: example

            Gets interpreter representation of empty tree:

            ::

                >>> baca.Tree()
                Tree()

        Returns string.
        '''
        superclass = super(Tree, self)
        return superclass.__repr__()

    ### PRIVATE PROPERTIES ###

    @property
    def _noncyclic_children(self):
        return list(self._children)

    @property
    def _root(self):
        return self._get_parentage()[-1]

    ### PRIVATE METHODS ###

    def _apply_to_leaves_and_emit_new_tree(self, operator):
        result = abjad.new(self)
        for leaf in result.iterate(level=-1):
            assert not len(leaf), repr(leaf)
            pitch = leaf._items
            pitch = operator(pitch) 
            leaf._set_leaf_item(pitch)
        return result

    def _are_internal_nodes(self, argument):
        if (isinstance(argument, collections.Iterable) and
            not isinstance(argument, str)):
            return True
        if isinstance(argument, type(self)) and len(argument):
            return True
        return False

    def _get_depth(self):
        r'''Gets depth.

        ..  container:: example

            Gets depth:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> tree[1]._get_depth()
                2

        Returns nonnegative integer.
        '''
        levels = set([])
        for node in self._iterate_depth_first():
            levels.add(node._get_level())
        return max(levels) - self._get_level() + 1

    def _get_index_in_parent(self):
        if self._parent is not None:
            return self._parent._index(self)
        else:
            return None

    def _get_level(self, negative=False):
        r'''Gets level.

        ..  container:: example

            Gets level:

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> tree._get_level()
                0

            ::

                >>> tree[1]._get_level()
                1

            ::

                >>> tree[1][1]._get_level()
                2

        ..  container:: example

            Gets negative level:

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> tree._get_level(negative=True)
                -4

            ::

                >>> tree[1]._get_level(negative=True)
                -2

            ::

                >>> tree[1][1]._get_level(negative=True)
                -1

            ::

                >>> tree[-1][-1]._get_level(negative=True)
                -1

            ::

                >>> tree[-1]._get_level(negative=True)
                -2

        Returns nonnegative integer when `negative` is false.

        Returns negative integer when `negative` is true.
        '''
        if negative:
            return -self._get_depth()
        return len(self._get_parentage(include_self=False))

    def _get_next_n_nodes_at_level(
        self,
        n,
        level,
        nodes_must_be_complete=False,
        ):
        r'''Gets next `n` nodes `level`.

        ..  container:: example

            Nodes don't need to be complete:

            ::

                >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = baca.Tree(items=items)

            Gets all nodes at level 2:

            ::

                >>> tree[0][0]._get_next_n_nodes_at_level(None, 2)
                [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4), Tree(items=5), Tree(items=6), Tree(items=7)]

            Gets all nodes at level -1:

            ::
            
                >>> tree[0][0]._get_next_n_nodes_at_level(None, -1)
                [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4), Tree(items=5), Tree(items=6), Tree(items=7)]

            Gets next 4 nodes at level 2:

            ::

                >>> tree[0][0]._get_next_n_nodes_at_level(4, 2)
                [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4)]

            Gets next 3 nodes at level 1:

            ::

                >>> tree[0][0]._get_next_n_nodes_at_level(3, 1)
                [Tree(items=[Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)])]

            Gets next node at level 0:

            ::

                >>> tree[0][0]._get_next_n_nodes_at_level(1, 0)
                [Tree(items=[Tree(items=[Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6), Tree(items=7)])])]

            Gets next 4 nodes at level -1:

            ::

                >>> tree[0][0]._get_next_n_nodes_at_level(4, -1)
                [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4)]

            Gets next 3 nodes at level -2:

            ::

                >>> tree[0][0]._get_next_n_nodes_at_level(3, -2)
                [Tree(items=[Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)])]

            Gets previous 4 nodes at level 2:

            ::

                >>> tree[-1][-1]._get_next_n_nodes_at_level(-4, 2)
                [Tree(items=6), Tree(items=5), Tree(items=4), Tree(items=3)]

            Gets previous 3 nodes at level 1:

            ::

                >>> tree[-1][-1]._get_next_n_nodes_at_level(-3, 1)
                [Tree(items=[Tree(items=6)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=2), Tree(items=3)])]

            Gets previous node at level 0:

            ::

                >>> tree[-1][-1]._get_next_n_nodes_at_level(-1, 0)
                [Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6)])])]

            Gets previous 4 nodes at level -1:

            ::

                >>> tree[-1][-1]._get_next_n_nodes_at_level(-4, -1)
                [Tree(items=6), Tree(items=5), Tree(items=4), Tree(items=3)]

            Gets previous 3 nodes at level -2:

            ::

                >>> tree[-1][-1]._get_next_n_nodes_at_level(-3, -2)
                [Tree(items=[Tree(items=6)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=2), Tree(items=3)])]

        ..  container:: example

            Tree of length greater than ``1`` for examples with positive `n`:

            ::

                >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = baca.Tree(items=items)

            Gets next 4 nodes at level 2:

            ::

                >>> for node in tree[0][0]._get_next_n_nodes_at_level(
                ...     4, 2,
                ...     nodes_must_be_complete=True,
                ...     ):
                ...     node 
                Tree(items=1)
                Tree(items=2)
                Tree(items=3)
                Tree(items=4)

            Gets next 3 nodes at level 1:

            ::

                >>> for node in tree[0][0]._get_next_n_nodes_at_level(
                ...     3, 1,
                ...     nodes_must_be_complete=True,
                ...     ):
                ...     node
                Tree(items=[Tree(items=1)])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=[Tree(items=6), Tree(items=7)])

            Gets next 4 nodes at level -1:

            ::

                >>> for node in tree[0][0]._get_next_n_nodes_at_level(4, -1):
                ...     node
                Tree(items=1)
                Tree(items=2)
                Tree(items=3)
                Tree(items=4)

            Gets next 3 nodes at level -2:

            ::

                >>> for node in tree[0][0]._get_next_n_nodes_at_level(
                ...     3, -2,
                ...     nodes_must_be_complete=True,
                ...     ):
                ...     node
                Tree(items=[Tree(items=1)])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=[Tree(items=6), Tree(items=7)])

        ..  container:: example

            Tree of length greater than ``1`` for examples with negative `n`:

            ::

                >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = baca.Tree(items=items)

            Gets previous 4 nodes at level 2:

            ::

                >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
                ...     -4, 2,
                ...     nodes_must_be_complete=True,
                ...     ):
                ...     node
                Tree(items=6)
                Tree(items=5)
                Tree(items=4)
                Tree(items=3)

            Gets previous 3 nodes at level 1:

            ::

                >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
                ...     -3, 1,
                ...     nodes_must_be_complete=True,
                ...     ):
                ...     node
                Tree(items=[Tree(items=6)])
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=[Tree(items=0), Tree(items=1)])

            Gets previous 4 nodes at level -1:

            ::

                >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
                ...     -4, -1,
                ...     nodes_must_be_complete=True,
                ...     ):
                ...     node
                Tree(items=6)
                Tree(items=5)
                Tree(items=4)
                Tree(items=3)

            Gets previous 3 nodes at level -2:

            ::

                >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
                ...     -3, -2,
                ...     nodes_must_be_complete=True,
                ...     ):
                ...     node
                Tree(items=[Tree(items=6)])
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=[Tree(items=0), Tree(items=1)])

        '''
        if not self._is_valid_level(level):
            message = 'invalid level: {!r}.'.format(level)
            raise Exception(message)
        result = []
        self_is_found = False
        first_node_returned_is_trimmed = False
        all_nodes_at_level = False
        reverse = False
        if n is None:
            all_nodes_at_level = True
        elif n < 0:
            reverse = True
            n = abs(n)
        generator = self._root._iterate_depth_first(reverse=reverse)
        previous_node = None
        for node in generator:
            if not all_nodes_at_level and len(result) == n:
                if (not first_node_returned_is_trimmed or
                    not nodes_must_be_complete):
                    return result
            if not all_nodes_at_level and len(result) == n + 1:
                return result
            if node is self:
                self_is_found = True
                # test whether node to return is higher in tree than self;
                # or-clause allows for test of either nonnegative
                # or negative level
                if (((0 <= level) and level < self._get_level()) or
                    ((level < 0) and level < self._get_level(negative=True))):
                    first_node_returned_is_trimmed = True
                    subtree_to_trim = node._parent
                    # find subtree to trim where level is nonnegative
                    if 0 <= level:
                        while level < subtree_to_trim._get_level():
                            subtree_to_trim = subtree_to_trim._parent
                    # find subtree to trim where level is negative
                    else:
                        while subtree_to_trim._get_level(negative=True) < level:
                            subtree_to_trim = subtree_to_trim._parent
                    position_of_descendant = \
                        subtree_to_trim._get_position_of_descendant(node)
                    first_subtree = copy.deepcopy(subtree_to_trim)
                    reference_node = \
                        first_subtree._get_node_at_position(
                            position_of_descendant)
                    reference_node._remove_to_root(reverse=reverse)
                    result.append(first_subtree)
            if self_is_found:
                if node is not self:
                    if node._is_at_level(level):
                        result.append(node)
                    # special case to handle a cyclic tree of length 1
                    elif node._is_at_level(0) and len(node) == 1:
                        if previous_node._is_at_level(level):
                            result.append(node)
            previous_node = node
        else:
            if all_nodes_at_level:
                return result
            else:
                message = 'not enough nodes at level {}.'
                message = message.format(level)
                raise ValueError(message)

    def _get_node_at_position(self, position):
        result = self
        for index in position:
            result = result[index]
        return result

    def _get_parentage(self, include_self=True):
        '''Gets parentage.

        ..  container:: example

            Gets parentage with self:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)
                >>> parentage = tree[1]._get_parentage()
                >>> for tree in parentage:
                ...     tree
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            Gets parentage without self:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)
                >>> parentage = tree[1]._get_parentage(include_self=False)
                >>> for tree in parentage:
                ...     tree
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

        Returns tuple.
        '''
        result = []
        if include_self:
            result.append(self)
        current = self._parent
        while current is not None:
            result.append(current)
            current = current._parent
        return tuple(result)

    def _get_position(self):
        r'''Gets position.

        ..  container:: example

            Gets position:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> tree[1]._get_position()
                (1,)

        Position of node defined relative to root.

        Returns tuple of zero or more nonnegative integers.
        '''
        result = []
        for node in self._get_parentage():
            if node._parent is not None:
                result.append(node._get_index_in_parent())
        result.reverse()
        return tuple(result)

    def _get_position_of_descendant(self, descendant):
        r'''Gets position of `descendent` relative to node
        rather than relative to root.

        ..  container:: example

            Gets position of descendant:

            ::

                >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> tree[3]._get_position_of_descendant(tree[3][0])
                (0,)

        Returns tuple of zero or more nonnegative integers.
        '''
        if descendant is self:
            return ()
        else:
            return descendant._get_position()[len(self._get_position()):]

    def _index(self, node):
        for i, current_node in enumerate(self):
            if current_node is node:
                return i
        message = 'not in tree: {!r}.'
        message = message.format(node)
        raise ValueError(message)

    def _initialize_internal_nodes(self, items):
        children = []
        for item in items:
            expression = getattr(item, '_expression', None)
            equivalence_markup = getattr(item, '_equivalence_markup', None)
            child = type(self)(items=item, item_class=self.item_class)
            child._expression = expression
            child._equivalence_markup = equivalence_markup
            child._parent = self
            children.append(child)
        self._children = children
        return children

    def _initialize_payload(self, payload):
        if isinstance(payload, type(self)):
            assert not len(payload)
            payload = payload._payload
        if self.item_class is not None:
            payload = self.item_class(payload)
        self._payload = payload
        return payload

    def _is_at_level(self, level):
        if ((0 <= level and self._get_level() == level) or
            self._get_level(negative=True) == level):
            return True
        else:
            return False

    def _is_leaf(self):
        return self._get_level(negative=True) == -1

    def _is_leftmost_leaf(self):
        if not self._is_leaf():
            return False
        return self._get_index_in_parent() == 0

    def _is_rightmost_leaf(self):
        if not self._is_leaf():
            return False
        index_in_parent = self._get_index_in_parent()
        parentage = self._get_parentage()
        parent = parentage[1]
        return index_in_parent == len(parent) - 1

    def _is_valid_level(self, level):
        maximum_absolute_level = self._get_depth() + 1
        if maximum_absolute_level < abs(level):
            return False
        return True

    def _iterate_depth_first(self, reverse=False):
        r'''Iterates depth-first.

        ..  container:: example

            Iterates tree depth-first from left to right:

            ::

                >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> for node in tree._iterate_depth_first(): node
                ...
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6), Tree(items=7)])])
                Tree(items=[Tree(items=0), Tree(items=1)])
                Tree(items=0)
                Tree(items=1)
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=2)
                Tree(items=3)
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=4)
                Tree(items=5)
                Tree(items=[Tree(items=6), Tree(items=7)])
                Tree(items=6)
                Tree(items=7)

        ..  container::

            Iterates tree depth-first from right to left:

            ::

                >>> for node in tree._iterate_depth_first(reverse=True): node
                ...
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6), Tree(items=7)])])
                Tree(items=[Tree(items=6), Tree(items=7)])
                Tree(items=7)
                Tree(items=6)
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=5)
                Tree(items=4)
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=3)
                Tree(items=2)
                Tree(items=[Tree(items=0), Tree(items=1)])
                Tree(items=1)
                Tree(items=0)

        Returns generator.
        '''
        yield self
        iterable_self = self
        if reverse:
            iterable_self = reversed(self)
        for x in iterable_self:
            for y in x._iterate_depth_first(reverse=reverse):
                yield y

    def _remove_node(self, node):
        node._parent._children.remove(node)
        node._parent = None

    def _remove_to_root(self, reverse=False):
        r'''Removes node and all nodes left of node to root.

        ..container:: example

            Removes node and all nodes left of node to root:

            ::

                >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]

            ::

                >>> tree = baca.Tree(items=items)
                >>> tree[0][0]._remove_to_root()
                >>> tree.get_payload(nested=True)
                [[1], [2, 3], [4, 5], [6, 7]]

            ::

                >>> tree = baca.Tree(items=items)
                >>> tree[0][1]._remove_to_root()
                >>> tree.get_payload(nested=True)
                [[2, 3], [4, 5], [6, 7]]

            ::

                >>> tree = baca.Tree(items=items)
                >>> tree[1]._remove_to_root()
                >>> tree.get_payload(nested=True)
                [[4, 5], [6, 7]]

        Modifies in-place to root.

        Returns none.
        '''
        # trim left-siblings of self and self
        parent = self._parent
        if reverse:
            iterable_parent = reversed(parent)
        else:
            iterable_parent = parent[:]
        for sibling in iterable_parent:
            sibling._parent._remove_node(sibling)
            # break and do not remove siblings to right of self
            if sibling is self:
                break
        # trim parentage
        for node in parent._get_parentage():
            if node._parent is not None:
                iterable_parent = node._parent[:]
                if reverse:
                    iterable_parent = reversed(node._parent)
                else:
                    iterable_parent = node._parent[:]
                for sibling in iterable_parent:
                    if sibling is node:
                        # remove node now if it was emptied earlier
                        if not len(sibling):
                            sibling._parent._remove_node(sibling)
                        break
                    else:
                        sibling._parent._remove_node(sibling)

    def _set_leaf_item(self, item):
        assert self._is_leaf(), repr(self)
        self._items = item
        self._payload = item

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Gets item class.

        ..  container:: example

            Coerces input:

            ::

                >>> items = [[1.1, 2.2], [8.8, 9.9]]
                >>> tree = baca.Tree(items=items, item_class=int)

            ::

                >>> for node in tree.iterate(level=-1):
                ...     node
                Tree(items=1, item_class=int)
                Tree(items=2, item_class=int)
                Tree(items=8, item_class=int)
                Tree(items=9, item_class=int)

            ::

                >>> tree.get_payload(nested=True)
                [[1, 2], [8, 9]]

        Defaults to none.

        Set to class or none.

        Returns class or none.
        '''
        return self._item_class

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            Gets items:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> for item in tree.items:
                ...     item
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
                Tree(items=[Tree(items=4), Tree(items=5)])

        ..  container:: example

            Returns list:

            ::

                >>> isinstance(tree.items, list)
                True

        '''
        return self._items

    ### PUBLIC METHODS ###

    def get_payload(self, nested=False, reverse=False):
        r'''Gets payload.

        ..  container:: example

            Gets payload:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            ::

                >>> tree.get_payload()
                [0, 1, 2, 3, 4, 5]

        ..  container:: example

            Gets nested payload:

            ::

                >>> tree.get_payload(nested=True)
                [[[0, 1], [2, 3]], [4, 5]]

        ..  container:: example

            Gets payload in reverse:

            ::

                >>> tree.get_payload(reverse=True)
                [5, 4, 3, 2, 1, 0]

        Nested payload in reverse is not yet implemented.

        Returns list.
        '''
        result = []
        if nested:
            if reverse:
                raise NotImplementedError
            if self._payload is not None:
                return self._payload
            else:
                for child in self._noncyclic_children:
                    if child._payload is not None:
                        result.append(child._payload)
                    else:
                        result.append(child.get_payload(nested=True))
        else:
            for leaf_node in self.iterate(-1, reverse=reverse):
                result.append(leaf_node._payload)
        return result

    def iterate(self, level=None, reverse=False):
        r'''Iterates tree at optional `level`.

        ..  container:: example

            Example tree:

            ::

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)
                >>> graph(tree) # doctest: +SKIP

            Iterates all levels:

            ::

                >>> for node in tree.iterate():
                ...     node
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
                Tree(items=[Tree(items=0), Tree(items=1)])
                Tree(items=0)
                Tree(items=1)
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=2)
                Tree(items=3)
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=4)
                Tree(items=5)

            Iterates all levels in reverse:

            ::

                >>> for node in tree.iterate(reverse=True):
                ...     node
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=5)
                Tree(items=4)
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=3)
                Tree(items=2)
                Tree(items=[Tree(items=0), Tree(items=1)])
                Tree(items=1)
                Tree(items=0)

            Iterates select levels:

            ::

                >>> for node in tree.iterate(level=0):
                ...     node
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            ::

                >>> for node in tree.iterate(level=1):
                ...     node
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
                Tree(items=[Tree(items=4), Tree(items=5)])

            ::

                >>> for node in tree.iterate(level=2):
                ...     node
                Tree(items=[Tree(items=0), Tree(items=1)])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=4)
                Tree(items=5)

            ::

                >>> for node in tree.iterate(level=3):
                ...     node
                Tree(items=0)
                Tree(items=1)
                Tree(items=2)
                Tree(items=3)

            ::

                >>> for node in tree.iterate(level=-4):
                ...     node
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            ::

                >>> for node in tree.iterate(level=-3):
                ...     node
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])

            ::

                >>> for node in tree.iterate(level=-2):
                ...     node
                Tree(items=[Tree(items=0), Tree(items=1)])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=[Tree(items=4), Tree(items=5)])

            ::

                >>> for node in tree.iterate(level=-1):
                ...     node
                Tree(items=0)
                Tree(items=1)
                Tree(items=2)
                Tree(items=3)
                Tree(items=4)
                Tree(items=5)

            Iterates select levels in reverse:

            ::

                >>> for node in tree.iterate(level=0, reverse=True):
                ...     node
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            ::

                >>> for node in tree.iterate(level=1, reverse=True):
                ...     node
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])

            ::

                >>> for node in tree.iterate(level=2, reverse=True):
                ...     node
                Tree(items=5)
                Tree(items=4)
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=[Tree(items=0), Tree(items=1)])

            ::

                >>> for node in tree.iterate(level=3, reverse=True):
                ...     node
                Tree(items=3)
                Tree(items=2)
                Tree(items=1)
                Tree(items=0)

            ::

                >>> for node in tree.iterate(level=-4, reverse=True):
                ...     node
                Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            ::

                >>> for node in tree.iterate(level=-3, reverse=True):
                ...     node
                Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])

            ::

                >>> for node in tree.iterate(level=-2, reverse=True):
                ...     node
                Tree(items=[Tree(items=4), Tree(items=5)])
                Tree(items=[Tree(items=2), Tree(items=3)])
                Tree(items=[Tree(items=0), Tree(items=1)])

            ::

                >>> for node in tree.iterate(level=-1, reverse=True):
                ...     node
                Tree(items=5)
                Tree(items=4)
                Tree(items=3)
                Tree(items=2)
                Tree(items=1)
                Tree(items=0)

        Returns generator.
        '''
        for node in self._iterate_depth_first(reverse=reverse):
            if level is None:
                yield node
            elif 0 <= level:
                if node._get_level() == level:
                    yield node
            else:
                if node._get_level(negative=True) == level:
                    yield node

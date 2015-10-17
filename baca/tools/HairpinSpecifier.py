# -*- coding: utf-8 -*-
from abjad import *


class HairpinSpecifier(abctools.AbjadObject):
    r'''Hairpin specifier.

    ..  container:: example

        **Example 1.** Hairpin specifier:

        ::

            >>> import baca
            >>> specifier = baca.tools.HairpinSpecifier(
            ...     descriptor='p > niente',
            ...     include_following_rest=True,
            ...     start=-1,
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.tools.HairpinSpecifier(
                descriptor='p > niente',
                include_following_rest=True,
                start=-1,
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_descriptor',
        '_include_following_rest',
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        descriptor=None,
        include_following_rest=None,
        start=None,
        stop=None,
        ):
        if descriptor is not None:
            assert isinstance(descriptor, str), repr(descriptor)
        self._descriptor = descriptor
        if include_following_rest is not None:
            include_following_rest = bool(include_following_rest)
        self._include_following_rest = include_following_rest
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls hairpin specifier on `logical_ties`.

        Returns none.
        '''
        leaves = list(iterate(logical_ties).by_leaf())
        leaf_slice = leaves[self.start:self.stop]
        if leaf_slice[-1] is leaves[-1]:
            if self.include_following_rest:
                following_leaf = inspect_(leaf_slice[-1]).get_leaf(1)
                prototype = (scoretools.Rest, scoretools.MultimeasureRest)
                if isinstance(following_leaf, prototype):
                    leaf_slice.append(following_leaf)
        hairpin = spannertools.Hairpin(
            descriptor=self.descriptor,
            include_rests=self.include_following_rest,
            )
        attach(hairpin, leaf_slice)

    ### PUBLIC PROPERTIES ###

    @property
    def descriptor(self):
        r'''Gets descriptor.

        Set to string or none.

        Defaults to none.

        Returns string or none.
        '''
        return self._descriptor

    @property
    def include_following_rest(self):
        r'''Is true when hairpin should include following rest.
        Otherwise false.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._include_following_rest

    @property
    def start(self):
        r'''Gets start.

        Set to integer or none.

        Defaults to none.

        Returns integer or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets stop.

        Set to integer or none.

        Defaults to none.

        Returns integer or none.
        '''
        return self._stop
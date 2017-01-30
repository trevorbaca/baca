# -*- coding: utf-8 -*-
import abjad


class ChordalSpacingSpecifier(abjad.abctools.AbjadValueObject):
    r'''Chordal spacing specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.ChordalSpacingSpecifier()
            ChordalSpacingSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_remove_duplicates',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        remove_duplicates=None,
        ):
        if remove_duplicates is not None:
            remove_duplicates = bool(remove_duplicates)
        self._remove_duplicates = remove_duplicates

    ### SPECIAL METHODS ###

    def __call__(self, segment=None):
        r'''Calls specifier on `segment`.

        Returns pitch set.
        '''
        raise NotImplementedError
    
    ### PUBLIC PROPERTIES ###

    @property
    def remove_duplicates(self):
        r'''Is true when specifier removes pitch-class duplicates.

        Returns true, false or none.
        '''
        return self._remove_duplicates

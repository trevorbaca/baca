# -*- coding: utf-8 -*-
import abc
import abjad


class Handler(abjad.abctools.AbjadValueObject):
    r'''Handler.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Handlers'

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a handler with the same type and
        initializer parameter values as this one.

        Returns true or false.
        '''
        return abjad.systemtools.StorageFormatManager.compare(self, expr)

    def __format__(self, format_specification=''):
        r'''Formats handler.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return abjad.systemtools.StorageFormatManager.get_storage_format(
                self)
        return str(self)

    def __hash__(self):
        r'''Hashes handler.

        Returns integer.
        '''
        hash_values = abjad.systemtools.StorageFormatManager.get_hash_values(
            self)
        return hash(hash_values)

    ### PRIVATE METHODS ###

    @staticmethod
    def _remove_outer_rests_from_sequence(sequence):
        first_keep_index = None
        for i, element in enumerate(sequence):
            if not isinstance(element, abjad.scoretools.Rest):
                first_keep_index = i
                break
        last_keep_index = None
        for i, element in enumerate(reversed(sequence)):
            if not isinstance(element, abjad.scoretools.Rest):
                last_keep_index = len(sequence) - i
                break
        return sequence[first_keep_index:last_keep_index]
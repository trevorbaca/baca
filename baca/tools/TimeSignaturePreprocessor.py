# -*- coding: utf-8 -*-
from abjad import *


class TimeSignaturePreprocessor(abctools.AbjadObject):
    r'''Time signature preprocessor.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Initializes with stage specifier and time signatures:

        ::

            >>> stage_specifier = [
            ...     1, TimeSignature((2, 3)),
            ...     1, TimeSignature((2, 3)),
            ...     2, TimeSignature((1, 6)),
            ...     ]
            >>> time_signatures = [(3, 8), (3, 8), (4, 8), (4, 8)]
            >>> preprocessor = baca.tools.TimeSignaturePreprocessor(
            ...     stage_specifier=stage_specifier,
            ...     time_signatures=time_signatures,
            ...     )

        ::
            
            >>> print(format(preprocessor))
            baca.tools.TimeSignaturePreprocessor(
                stage_specifier=[
                    1,
                    indicatortools.TimeSignature((2, 3)),
                    1,
                    indicatortools.TimeSignature((2, 3)),
                    2,
                    indicatortools.TimeSignature((1, 6)),
                    ],
                time_signatures=datastructuretools.CyclicTuple(
                    [
                        (3, 8),
                        (3, 8),
                        (4, 8),
                        (4, 8),
                        ]
                    ),
                )

    ..  container:: example

        **Example 2.** Initializes with stage specifier and time signatures:

        ::

            >>> stage_specifier = [
            ...     1, [TimeSignature((2, 3)), TimeSignature((2, 3))],
            ...     1,
            ...     2,
            ...     ]
            >>> time_signatures = [(3, 8), (3, 8), (4, 8), (4, 8)]
            >>> preprocessor = baca.tools.TimeSignaturePreprocessor(
            ...     stage_specifier=stage_specifier,
            ...     time_signatures=time_signatures,
            ...     )

        ::
            
            >>> print(format(preprocessor))
            baca.tools.TimeSignaturePreprocessor(
                stage_specifier=[
                    1,
                    [
                        indicatortools.TimeSignature((2, 3)),
                        indicatortools.TimeSignature((2, 3)),
                        ],
                    1,
                    2,
                    ],
                time_signatures=datastructuretools.CyclicTuple(
                    [
                        (3, 8),
                        (3, 8),
                        (4, 8),
                        (4, 8),
                        ]
                    ),
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_repeat_count',
        '_stage_specifier',
        '_time_signatures',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        repeat_count=None,
        stage_specifier=None,
        time_signatures=None,
        ):
        self._repeat_count = repeat_count
        self._stage_specifier = stage_specifier
        time_signatures = datastructuretools.CyclicTuple(time_signatures)
        self._time_signatures = time_signatures

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls time signature preprocessor.

        ..  container:: example

            **Example 1.** With single explicit time signatures:

            ::

                >>> stage_specifier = [
                ...     1, TimeSignature((2, 3)),
                ...     1, TimeSignature((2, 3)),
                ...     2, TimeSignature((1, 6)),
                ...     ]
                >>> time_signatures = [(3, 8), (3, 8), (4, 8), (4, 8)]
                >>> preprocessor = baca.tools.TimeSignaturePreprocessor(
                ...     stage_specifier=stage_specifier,
                ...     time_signatures=time_signatures,
                ...     )

            ::

                >>> lists = preprocessor()
                >>> for list_ in lists: list_
                [(3, 8)]
                [TimeSignature((2, 3))]
                [(3, 8)]
                [TimeSignature((2, 3))]
                [(4, 8), (4, 8)]
                [TimeSignature((1, 6))]

        ..  container:: example

            **Example 2.** With runs of explicit time signatures:

            ::

                >>> stage_specifier = [
                ...     1, [TimeSignature((2, 3)), TimeSignature((2, 3))],
                ...     1,
                ...     2,
                ...     ]
                >>> time_signatures = [(3, 8), (3, 8), (4, 8), (4, 8)]
                >>> preprocessor = baca.tools.TimeSignaturePreprocessor(
                ...     stage_specifier=stage_specifier,
                ...     time_signatures=time_signatures,
                ...     )

            ::

                >>> lists = preprocessor()
                >>> for list_ in lists: list_
                [(3, 8)]
                [TimeSignature((2, 3)), TimeSignature((2, 3))]
                [(3, 8)]
                [(4, 8), (4, 8)]

        Returns list of time signature lists.
        '''
        time_signature_lists = []
        index = 0
        for x in self.stage_specifier:
            if isinstance(x, TimeSignature):
                time_signature_list = [x]
            elif isinstance(x, (tuple, list)):
                time_signature_list = list(x)
            else:
                time_signature_list = self.time_signatures[index:index+x]
                time_signature_list = list(time_signature_list)
                index += x
            time_signature_lists.append(time_signature_list)
        repeat_count = self.repeat_count or 1
        time_signature_lists *= repeat_count
        return time_signature_lists

    ### PUBLIC PROPERTIES ###

    @property
    def repeat_count(self):
        r'''Gets repeat count of time signature preprocessor.

        Set to positive integer or none.

        Defaults to none.

        Returns positive integer or none.
        '''
        return self._repeat_count

    @property
    def stage_specifier(self):
        r'''Gets stage specifier of time signature preprocessor.

        ..  container:: example

            ::
        
                >>> stage_specifier = [
                ...     1, TimeSignature((2, 3)),
                ...     1, TimeSignature((2, 3)),
                ...     2, TimeSignature((1, 6)),
                ...     ]
                >>> time_signatures = [(3, 8), (3, 8), (4, 8), (4, 8)]
                >>> preprocessor = baca.tools.TimeSignaturePreprocessor(
                ...     stage_specifier=stage_specifier,
                ...     time_signatures=time_signatures,
                ...     )

            ::

                >>> preprocessor.stage_specifier
                [1, TimeSignature((2, 3)), 1, TimeSignature((2, 3)), 2, TimeSignature((1, 6))]

        Set to stage specifier.

        Returns stage specifier.
        '''
        return self._stage_specifier

    @property
    def time_signatures(self):
        r'''Gets time signatures of time signature preprocessor.

        ..  container:: example

            ::

                >>> stage_specifier = [
                ...     1, TimeSignature((2, 3)),
                ...     1, TimeSignature((2, 3)),
                ...     2, TimeSignature((1, 6)),
                ...     ]
                >>> time_signatures = [(3, 8), (3, 8), (4, 8), (4, 8)]
                >>> preprocessor = baca.tools.TimeSignaturePreprocessor(
                ...     stage_specifier=stage_specifier,
                ...     time_signatures=time_signatures,
                ...     )

            ::

                >>> preprocessor.time_signatures
                CyclicTuple([(3, 8), (3, 8), (4, 8), (4, 8)])

        Set to iterable.

        Returns cyclic tuple.
        '''
        return self._time_signatures
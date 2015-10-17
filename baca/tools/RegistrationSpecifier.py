# -*- coding: utf-8 -*-
from abjad import *


class RegistrationSpecifier(abctools.AbjadObject):
    r'''Registration specifier.

    ..  container:: example

        ::

            >>> import baca
            >>> specifier = baca.tools.RegistrationSpecifier(
            ...     registration=pitchtools.Registration(
            ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
            ...         ),
            ...     )

        ::
            
            >>> print(format(specifier, 'storage'))
            baca.tools.RegistrationSpecifier(
                registration=pitchtools.Registration(
                    [
                        pitchtools.RegistrationComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[A0, C4)',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(15),
                            ),
                        pitchtools.RegistrationComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[C4, C8)',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(27),
                            ),
                        ]
                    ),
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_registration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        registration=None,
        ):
        from abjad.tools import pitchtools
        prototype = (type(None), pitchtools.Registration)
        assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        for logical_tie in logical_ties:
            for note in logical_tie:
                written_pitch = self.registration([note.written_pitch])
                note.written_pitch = written_pitch

    ### PUBLIC PROPERTIES ###

    @property
    def registration(self):
        r'''Gets registration of registration specifier.

        ..  container:: example

            ::

                >>> specifier.registration
                Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])

        Set to octave transposition mapping or none.
        '''
        return self._registration
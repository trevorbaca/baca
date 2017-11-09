import abjad


class RegistrationDictionary(abjad.TypedOrderedDict):
    '''Registration dictionary.

    ..  container:: example

        Two registrations:

        >>> registration_1 = baca.Registration(
        ...     [('[A0, C4)', 15), ('[C4, C8)', 27)]
        ...     )
        >>> registration_2 = baca.Registration(
        ...     [('[A0, C8]', -18)]
        ...     )
        >>> registrations = baca.RegistrationDictionary([
        ...     ('low', registration_1),
        ...     ('high', registration_2),
        ...     ])

        >>> abjad.f(registrations)
        baca.RegistrationDictionary(
            [
                (
                    'low',
                    baca.Registration(
                        components=[
                            baca.RegistrationComponent(
                                source_pitch_range=abjad.PitchRange('[A0, C4)'),
                                target_octave_start_pitch=abjad.NumberedPitch(15),
                                ),
                            baca.RegistrationComponent(
                                source_pitch_range=abjad.PitchRange('[C4, C8)'),
                                target_octave_start_pitch=abjad.NumberedPitch(27),
                                ),
                            ],
                        ),
                    ),
                (
                    'high',
                    baca.Registration(
                        components=[
                            baca.RegistrationComponent(
                                source_pitch_range=abjad.PitchRange('[A0, C8]'),
                                target_octave_start_pitch=abjad.NumberedPitch(-18),
                                ),
                            ],
                        ),
                    ),
                ]
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    __documentation_section__ = '(6) Utilities'

    ### PRIVATE METHODS ###

    @staticmethod
    def _item_coercer(argument):
        import baca
        if isinstance(argument, baca.Registration):
            return argument
        return baca.Registration(argument)

import abjad
import copy


class Registration(abjad.AbjadValueObject):
    '''Registration.

    ..  container:: example

        Registration in two parts:

        >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
        >>> registration = baca.Registration(components)

        >>> abjad.f(registration)
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
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_components',
        )

    __documentation_section__ = '(6) Utilities'

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, components=None):
        import baca
        components_ = []
        for component in components or []:
            if isinstance(component, baca.RegistrationComponent):
                components_.append(component)
            else:
                component_ = baca.RegistrationComponent(*component)
                components_.append(component_)
        self._components = components_ or None

    ### SPECIAL METHODS ###

    def __call__(self, pitches):
        r"""Calls registration on `pitches`.

        ..  container:: example

            Transposes four pitches:

            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([-24, -22, -23, -21])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("c'''")
            NamedPitch("d'''")
            NamedPitch("cs'''")
            NamedPitch("ef''")

        ..  container:: example

            Transposes four other pitches:

            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([0, 2, 1, 3])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("c''''")
            NamedPitch("d''''")
            NamedPitch("cs''''")
            NamedPitch("ef'''")

        ..  container:: example

            Transposes four quartertones:

            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([0.5, 2.5, 1.5, 3.5])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("cqs''''")
            NamedPitch("dqs''''")
            NamedPitch("dqf''''")
            NamedPitch("eqf'''")

        Returns list of new pitches.
        """
        return [self._transpose_pitch(_) for _ in pitches]

    ### PRIVATE METHODS ###

    def _transpose_pitch(self, pitch):
        pitch = abjad.NamedPitch(pitch)
        for component in self.components:
            if pitch in component.source_pitch_range:
                start_pitch = component.target_octave_start_pitch
                stop_pitch = start_pitch + 12
                if start_pitch <= pitch < stop_pitch:
                    return pitch
                elif pitch < start_pitch:
                    while pitch < start_pitch:
                        pitch += 12
                    return pitch
                elif stop_pitch <= pitch:
                    while stop_pitch <= pitch:
                        pitch -= 12
                    return pitch
                else:
                    raise ValueError(pitch, self)
        else:
            raise ValueError(f'{pitch!r} not in {self!r}.')

    ### PUBLIC PROPERTIES ###

    @property
    def components(self):
        r'''Gets components.

        Returns list or none.
        '''
        return self._components

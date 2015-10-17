# -*- coding: utf-8 -*-
from abjad import *


class RegistrationTransitionSpecifier(abctools.AbjadObject):
    r'''Registration transition specifier.

    ..  container:: example

        Starts at the octave of C4 and then transitions to the octave of C5:

        ::

            >>> import baca
            >>> specifier = baca.tools.RegistrationTransitionSpecifier(
            ...     start_registration=pitchtools.Registration(
            ...         [('[A0, C8]', 0)],
            ...          ),
            ...     stop_registration=pitchtools.Registration(
            ...         [('[A0, C8]', 12)],
            ...         ),
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.tools.RegistrationTransitionSpecifier(
                start_registration=pitchtools.Registration(
                    [
                        pitchtools.RegistrationComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[A0, C8]',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(0),
                            ),
                        ]
                    ),
                stop_registration=pitchtools.Registration(
                    [
                        pitchtools.RegistrationComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[A0, C8]',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(12),
                            ),
                        ]
                    ),
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_start_registration',
        '_stop_registration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_registration=None,
        stop_registration=None,
        ):
        assert isinstance(start_registration, pitchtools.Registration)
        assert isinstance(stop_registration, pitchtools.Registration)
        assert len(start_registration) == len(stop_registration)
        self._start_registration = start_registration
        self._stop_registration = stop_registration

    ### SPECIAL METHODS ###

    # TODO: extend SegmentMaker to pass timespan in here
    def __call__(self, logical_ties, timespan):
        for logical_tie in logical_ties:
            offset = logical_tie.get_timespan().start_offset
            registration = self._make_interpolated_registration(
                offset, 
                timespan,
                )
            for note in logical_tie:
                written_pitch = registration([note.written_pitch])
                note.written_pitch = written_pitch

    ### PRIVATE METHODS ###

    def _make_interpolated_registration(self, offset, timespan):
        assert timespantools.offset_happens_during_timespan(
            timespan=timespan,
            offset=offset,
            ), repr((timespan, offset))
        fraction = (offset - timespan.start_offset) / timespan.duration
        assert len(self.start_registration) == len(self.stop_registration)
        components = []
        start_components = self.start_registration.items
        stop_components = self.stop_registration.items
        pairs = zip(start_components, stop_components)
        for start_component, stop_component in pairs:
            start_pitch = start_component.source_pitch_range.start_pitch
            start_pitch = pitchtools.NumberedPitch(start_pitch)
            stop_pitch = stop_component.source_pitch_range.start_pitch
            lower_range_pitch = start_pitch.interpolate(stop_pitch, fraction)
            start_pitch = start_component.source_pitch_range.stop_pitch
            start_pitch = pitchtools.NumberedPitch(start_pitch)
            stop_pitch = stop_component.source_pitch_range.stop_pitch
            upper_range_pitch = start_pitch.interpolate(stop_pitch, fraction)
            range_string = '[{}, {})'
            range_string = range_string.format(
                lower_range_pitch.pitch_class_octave_label,
                upper_range_pitch.pitch_class_octave_label,
                )
            start_pitch = start_component.target_octave_start_pitch
            start_pitch = pitchtools.NumberedPitch(start_pitch)
            stop_pitch = stop_component.target_octave_start_pitch
            target_octave_start_pitch = start_pitch.interpolate(
                stop_pitch,
                fraction,
                )
            component = pitchtools.RegistrationComponent(
                source_pitch_range=range_string,
                target_octave_start_pitch=target_octave_start_pitch,
                )
            components.append(component)
        registration = pitchtools.Registration(components)
        return registration
    
    ### PUBLIC PROPERTIES ###

    @property
    def start_registration(self):
        r'''Gets start registration of registration transition specifier.

        Set to registration.
        '''
        return self._start_registration

    @property
    def stop_registration(self):
        r'''Gets stop registration of registration transition specifier.

        Set to registration.
        '''
        return self._stop_registration
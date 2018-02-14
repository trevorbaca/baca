import abjad
import baca
from .Command import Command
from .PitchCommand import PitchCommand
from .Typing import Number
from .Typing import Optional
from .Typing import Selector
from .Typing import Union


class StaffPositionInterpolationCommand(Command):
    r"""Staff position interpolation command.

    :param selector: command selector.

    :param start_pitch: interpolation start pitch.

    :param stop_pitch: interpolation stop pitch.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.clef('treble'),
        ...     baca.interpolate_staff_positions('Eb4', 'F#5'),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \clef "treble"                                                           %! IC
                            ef'16
                            [
                            e'16
                            f'16
                            f'16
                            f'16
                            g'16
                            g'16
                            g'16
                            a'16
                            a'16
                            a'16
                            b'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            b'16
                            [
                            c''16
                            c''16
                            c''16
                            d''16
                            d''16
                            d''16
                            e''16
                            e''16
                            e''16
                            f''16
                            fs''16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        >>> music_maker = baca.MusicMaker()

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.clef('treble'),
        ...     baca.interpolate_staff_positions('Eb4', 'F#5'),
        ...     baca.glissando(allow_repeats=True, stems=True), 
        ...     baca.glissando_thickness(3),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \override Glissando.thickness = #'3                                      %! OC1
                            \clef "treble"                                                           %! IC
                            ef'16
                            \glissando                                                               %! SC
                            [
                            \hide NoteHead                                                           %! SC
                            \override NoteColumn.glissando-skip = ##t                                %! SC
                            \override NoteHead.no-ledgers = ##t                                      %! SC
                            e'16
                            \glissando                                                               %! SC
                            f'16
                            \glissando                                                               %! SC
                            f'16
                            \glissando                                                               %! SC
                            f'16
                            \glissando                                                               %! SC
                            g'16
                            \glissando                                                               %! SC
                            g'16
                            \glissando                                                               %! SC
                            g'16
                            \glissando                                                               %! SC
                            a'16
                            \glissando                                                               %! SC
                            a'16
                            \glissando                                                               %! SC
                            a'16
                            \glissando                                                               %! SC
                            b'16
                            ]
                            \glissando                                                               %! SC
                        }
                        \scaleDurations #'(1 . 1) {
                            b'16
                            \glissando                                                               %! SC
                            [
                            c''16
                            \glissando                                                               %! SC
                            c''16
                            \glissando                                                               %! SC
                            c''16
                            \glissando                                                               %! SC
                            d''16
                            \glissando                                                               %! SC
                            d''16
                            \glissando                                                               %! SC
                            d''16
                            \glissando                                                               %! SC
                            e''16
                            \glissando                                                               %! SC
                            e''16
                            \glissando                                                               %! SC
                            e''16
                            \glissando                                                               %! SC
                            f''16
                            \glissando                                                               %! SC
                            \revert NoteColumn.glissando-skip                                        %! SC
                            \revert NoteHead.no-ledgers                                              %! SC
                            \undo \hide NoteHead                                                     %! SC
                            fs''16
                            ]
                            \revert Glissando.thickness                                              %! OC2
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_pitch',
        '_stop_pitch',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        selector: Selector = 'baca.plts()',
        start_pitch: Union[str, abjad.NamedPitch] = 'C4',
        stop_pitch: Union[str, abjad.NamedPitch] = 'C4',
        ) -> None:
        Command.__init__(self, selector=selector)
        start_pitch = abjad.NamedPitch(start_pitch)
        self._start_pitch: abjad.NamedPitch = start_pitch
        stop_pitch = abjad.NamedPitch(stop_pitch)
        self._stop_pitch: abjad.NamedPitch = stop_pitch

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        r'''Calls command on `argument`.
        '''
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = baca.select(argument).plts()
        if not plts:
            return
        count = len(plts)
        start_pl = plts[0].head
        clef = abjad.inspect(start_pl).get_effective(abjad.Clef)
        start_staff_position = self.start_pitch.to_staff_position(clef=clef)
        stop_pl = plts[-1].head
        clef = abjad.inspect(stop_pl).get_effective(
            abjad.Clef,
            default=abjad.Clef('treble'),
            )
        stop_staff_position = self.stop_pitch.to_staff_position(clef=clef)
        unit_distance = abjad.Fraction(
            stop_staff_position.number - start_staff_position.number,
            count - 1,
            )
        for i, plt in enumerate(plts):
            staff_position = unit_distance * i + start_staff_position.number
            staff_position = round(staff_position)
            staff_position = abjad.StaffPosition(staff_position)
            clef = abjad.inspect(plt.head).get_effective(
                abjad.Clef,
                default=abjad.Clef('treble'),
                )
            pitch = staff_position.to_pitch(clef=clef)
            PitchCommand._set_lt_pitch(plt, pitch)
            for leaf in plt:
                abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, leaf)
        PitchCommand._set_lt_pitch(plts[0], self.start_pitch)
        PitchCommand._set_lt_pitch(plts[-1], self.stop_pitch)

    ### PUBLIC PROPERTIES ###

    @property
    def start_pitch(self) -> abjad.NamedPitch:
        r'''Gets start pitch.
        '''
        return self._start_pitch

    @property
    def stop_pitch(self) -> abjad.NamedPitch:
        r'''Gets stop pitch.
        '''
        return self._stop_pitch

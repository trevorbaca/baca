import abjad
import typing
from .Partial import Partial


class HarmonicSeries(abjad.AbjadObject):
    r"""
    Harmonic series.

    ..  container:: example

        >>> harmonic_series = baca.HarmonicSeries('C2')
        >>> abjad.show(harmonic_series) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = harmonic_series.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff
            \with
            {
                \override BarLine.stencil = ##f
                \override Stem.transparent = ##t
                \override TextScript.font-size = #-1
                \override TextScript.staff-padding = #6
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                c,4 _ \markup { 1 }
                c4 _ \markup { 2 }
                g4
                    ^ \markup { +2 }
                    _ \markup { 3 }
                \clef "treble"
                c'4 _ \markup { 4 }
                e'4
                    ^ \markup { -14 }
                    _ \markup { 5 }
                g'4
                    ^ \markup { +2 }
                    _ \markup { 6 }
                bf'4
                    ^ \markup { -31 }
                    _ \markup { 7 }
                c''4 _ \markup { 8 }
                d''4
                    ^ \markup { +4 }
                    _ \markup { 9 }
                e''4
                    ^ \markup { -14 }
                    _ \markup { 10 }
                fqs''4
                    ^ \markup { +1 }
                    _ \markup { 11 }
                g''4
                    ^ \markup { +2 }
                    _ \markup { 12 }
                aqf''4
                    ^ \markup { -9 }
                    _ \markup { 13 }
                bf''4
                    ^ \markup { -31 }
                    _ \markup { 14 }
                b''4
                    ^ \markup { -12 }
                    _ \markup { 15 }
                c'''4 _ \markup { 16 }
                cs'''4
                    ^ \markup { +5 }
                    _ \markup { 17 }
                d'''4
                    ^ \markup { +4 }
                    _ \markup { 18 }
                ef'''4
                    ^ \markup { -2 }
                    _ \markup { 19 }
                e'''4
                    ^ \markup { -14 }
                    _ \markup { 20 }
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_fundamental',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fundamental: typing.Union[str, abjad.NamedPitch] = 'C1',
        ) -> None:
        fundamental = abjad.NamedPitch(fundamental)
        self._fundamental = fundamental

    ### SPECIAL METHODS ###

    def __illustrate__(self) -> abjad.LilyPondFile:
        r"""
        Illustrates harmonic series.

        ..  container:: example

            >>> harmonic_series = baca.HarmonicSeries('A1')
            >>> abjad.show(harmonic_series) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = harmonic_series.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff
                \with
                {
                    \override BarLine.stencil = ##f
                    \override Stem.transparent = ##t
                    \override TextScript.font-size = #-1
                    \override TextScript.staff-padding = #6
                    \override TimeSignature.stencil = ##f
                }
                {
                    \clef "bass"
                    a,,4 _ \markup { 1 }
                    a,4 _ \markup { 2 }
                    e4
                        ^ \markup { +2 }
                        _ \markup { 3 }
                    a4 _ \markup { 4 }
                    \clef "treble"
                    cs'4
                        ^ \markup { -14 }
                        _ \markup { 5 }
                    e'4
                        ^ \markup { +2 }
                        _ \markup { 6 }
                    g'4
                        ^ \markup { -31 }
                        _ \markup { 7 }
                    a'4 _ \markup { 8 }
                    b'4
                        ^ \markup { +4 }
                        _ \markup { 9 }
                    cs''4
                        ^ \markup { -14 }
                        _ \markup { 10 }
                    dqs''4
                        ^ \markup { +1 }
                        _ \markup { 11 }
                    e''4
                        ^ \markup { +2 }
                        _ \markup { 12 }
                    fqs''4
                        ^ \markup { -9 }
                        _ \markup { 13 }
                    g''4
                        ^ \markup { -31 }
                        _ \markup { 14 }
                    af''4
                        ^ \markup { -12 }
                        _ \markup { 15 }
                    a''4 _ \markup { 16 }
                    bf''4
                        ^ \markup { +5 }
                        _ \markup { 17 }
                    b''4
                        ^ \markup { +4 }
                        _ \markup { 18 }
                    c'''4
                        ^ \markup { -2 }
                        _ \markup { 19 }
                    cs'''4
                        ^ \markup { -14 }
                        _ \markup { 20 }
                }

        """
        staff = abjad.Staff()
        for n in range(1, 20 + 1):
            partial = self.partial(n)
            pitch = partial.approximation
            note = abjad.Note.from_pitch_and_duration(pitch, (1, 4))
            staff.append(note)
            deviation = partial.deviation
            if 0 < deviation:
                markup = abjad.Markup(f'+{deviation}', direction=abjad.Up)
                abjad.attach(markup, note)
            elif deviation < 0:
                markup = abjad.Markup(deviation, direction=abjad.Up)
                abjad.attach(markup, note)
            markup = abjad.Markup(n, direction=abjad.Down)
            abjad.attach(markup, note)
        notes = abjad.select(staff).notes()
        if notes[0].written_pitch < abjad.NamedPitch('C4'):
            abjad.attach(abjad.Clef('bass'), staff[0])
            for note in notes[1:]:
                if abjad.NamedPitch('C4') <= note.written_pitch:
                    abjad.attach(abjad.Clef('treble'), note)
                    break
        abjad.override(staff).bar_line.stencil = False
        abjad.override(staff).stem.transparent = True
        abjad.override(staff).text_script.font_size = -1
        abjad.override(staff).text_script.staff_padding = 6
        abjad.override(staff).time_signature.stencil = False
        score = abjad.Score([staff])
        moment = abjad.SchemeMoment((1, 8))
        abjad.setting(score).proportional_notation_duration = moment
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def fundamental(self) -> abjad.NamedPitch:
        """
        Gets fundamental.

        ..  container:: example

            >>> baca.HarmonicSeries('C2').fundamental
            NamedPitch('c,')

        """
        return self._fundamental

    ### PUBLIC METHODS ###

    def partial(self, n: int) -> Partial:
        """
        Gets partial ``n``.

        ..  container:: example

            >>> baca.HarmonicSeries('C2').partial(7)
            Partial(fundamental=NamedPitch('c,'), number=7)

        """
        return Partial(
            fundamental=self.fundamental,
            number=n,
            )

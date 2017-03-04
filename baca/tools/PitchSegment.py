# -*- coding: utf-8 -*-
import abjad
import baca
import inspect


class PitchSegment(abjad.PitchSegment):
    r'''Pitch segment.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes segment:

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = baca.pitch_segment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>


    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### PRIVATE METHODS ###

    def _to_selection(self):
        return abjad.scoretools.make_notes(self, [(1, 4)])

    ### PUBLIC METHODS ###

    def bass_to_octave(self, n=4):
        r'''Octave-transposes segment to bass in octave `n`.

        ..  container:: example

            ::

                >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

            ::

                >>> segment.bass_to_octave(n=4)
                PitchSegment([10, 10.5, 18, 19, 10.5, 19])

            ::

                >>> segment = segment.bass_to_octave(n=4)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            bf'1 * 1/8
                            bqf'1 * 1/8
                            fs''1 * 1/8
                            g''1 * 1/8
                            bqf'1 * 1/8
                            g''1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        Returns new segment.
        '''
        specifier = baca.tools.RegisterToOctaveSpecifier(
            anchor=Bottom,
            octave_number=n,
            )
        selection = self._to_selection()
        specifier([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)
        
    def chord(self):
        r'''Changes segment to set.

        ..  container:: example

            ::

                >>> segment = baca.pitch_segment([-2, -1.5, 6, 7])

            ::

                >>> segment.chord()
                PitchSet([-2, -1.5, 6, 7])

            ::

                >>> show(segment.chord()) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.chord().__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new PianoStaff <<
                        \new Staff {
                            \new Voice {
                                <fs' g'>1
                            }
                        }
                        \new Staff {
                            \new Voice {
                                <bf bqf>1
                            }
                        }
                    >>
                >>

        Returns pitch set.
        '''
        return baca.PitchSet(
            items=self,
            item_class=self.item_class,
            )

    def soprano_to_octave(self, n=4):
        r'''Octave-transposes segment to soprano in octave `n`.

        ..  container:: example

            ::

                >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

            ::

                >>> segment.soprano_to_octave(n=3)
                PitchSegment([-14, -13.5, -6, -5, -13.5, -5])

            ::

                >>> segment = segment.soprano_to_octave(n=3)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            bf,1 * 1/8
                            bqf,1 * 1/8
                            fs1 * 1/8
                            g1 * 1/8
                            bqf,1 * 1/8
                            g1 * 1/8
                        }
                    >>
                >>

        Returns new segment.
        '''
        specifier = baca.tools.RegisterToOctaveSpecifier(
            anchor=Top,
            octave_number=n,
            )
        selection = self._to_selection()
        specifier([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)

    def split(self, pitch=0):
        r'''Splits segment at `pitch`.

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = baca.pitch_segment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            fs'1 * 1/8
                            g'1 * 1/8
                            r1 * 1/8
                            g'1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            bqf1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

            ::

                >>> upper, lower = segment.split(pitch=0)

            ::

                >>> upper
                PitchSegment([6, 7, 7])

            ::

                >>> show(upper) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = upper.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            fs'1 * 1/8
                            g'1 * 1/8
                            g'1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

            ::

                >>> lower
                PitchSegment([-2, -1.5, -1.5])

            ::

                >>> show(lower) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = lower.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            bf1 * 1/8
                            bqf1 * 1/8
                            bqf1 * 1/8
                        }
                    >>
                >>

        Returns upper, lower segments.
        '''
        upper, lower = [], []
        for pitch_ in self:
            if pitch_ < pitch:
                lower.append(pitch_)
            else:
                upper.append(pitch_)
        upper = abjad.new(self, items=upper)
        lower = abjad.new(self, items=lower)
        return upper, lower


def _pitch_segment(items=None, **keywords):
    if items:
        return PitchSegment(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = baca.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchSegment,
        markup_expression=abjad.Expression().markup(),
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchSegment)

import abjad
import baca


class PitchSegment(abjad.PitchSegment):
    r"""
    Pitch segment.

    ..  container:: example

        Initializes segment:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### PRIVATE METHODS ###

    def _to_selection(self):
        maker = abjad.NoteMaker()
        return maker(self, [(1, 4)])

    ### PUBLIC METHODS ###

    def bass_to_octave(self, n=4):
        r"""
        Octave-transposes segment to bass in octave ``n``.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.bass_to_octave(n=4)
            PitchSegment([10, 10.5, 18, 19, 10.5, 19])

            >>> segment = segment.bass_to_octave(n=4)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs''1 * 1/8
                        g''1 * 1/8
                        bqf'1 * 1/8
                        g''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new segment.
        """
        command = baca.RegisterToOctaveCommand(
            anchor=abjad.Down,
            octave_number=n,
            )
        selection = self._to_selection()
        command([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)

    def center_to_octave(self, n=4):
        r"""
        Octave-transposes segment to center in octave ``n``.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.center_to_octave(n=3)
            PitchSegment([-14, -13.5, -6, -5, -13.5, -5])

            >>> segment = segment.center_to_octave(n=3)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                >>

        Returns new segment.
        """
        command = baca.RegisterToOctaveCommand(
            anchor=abjad.Center,
            octave_number=n,
            )
        selection = self._to_selection()
        command([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)

    def chord(self):
        r"""
        Changes segment to set.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7])

            >>> segment.chord()
            PitchSet([-2, -1.5, 6, 7])

            >>> abjad.show(segment.chord(), strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.chord().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <fs' g'>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            <bf bqf>1
                        }
                    }
                >>

        Returns pitch set.
        """
        return baca.PitchSet(
            items=self,
            item_class=self.item_class,
            )

    def soprano_to_octave(self, n=4):
        r"""
        Octave-transposes segment to soprano in octave ``n``.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.soprano_to_octave(n=3)
            PitchSegment([-14, -13.5, -6, -5, -13.5, -5])

            >>> segment = segment.soprano_to_octave(n=3)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                >>

        Returns new segment.
        """
        command = baca.RegisterToOctaveCommand(
            anchor=abjad.Up,
            octave_number=n,
            )
        selection = self._to_selection()
        command([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)

    def space_down(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r"""
        Spaces pitch segment down.

        ..  container:: example

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_down(bass=0)
            PitchSegment([14, 10, 9, 0])

            >>> segment = segment.space_down(bass=0)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        d''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        c'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_down(bass=2)
            PitchSegment([12, 10, 9, 2])

            >>> segment = segment.space_down(bass=2)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        d'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        specifier = baca.ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Down,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, baca.CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def space_up(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r"""
        Spaces pitch segment up.

        ..  container:: example

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_up(bass=0)
            PitchSegment([0, 2, 9, 10])

            >>> segment = segment.space_up(bass=0)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_up(bass=2)
            PitchSegment([2, 9, 10, 12])

            >>> segment = segment.space_up(bass=2)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                        c''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        specifier = baca.ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, baca.CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def split(self, pitch=0):
        r"""
        Splits segment at ``pitch``.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> upper, lower = segment.split(pitch=0)

            >>> upper
            PitchSegment([6, 7, 7])

            >>> abjad.show(upper, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = upper.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        fs'1 * 1/8
                        g'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> lower
            PitchSegment([-2, -1.5, -1.5])

            >>> abjad.show(lower, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = lower.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        bqf1 * 1/8
                    }
                >>

        Returns upper, lower segments.
        """
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
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchSegment)

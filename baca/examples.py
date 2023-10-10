r"""
Examples.

Colors octaves:

..  container:: example

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1, 1, no_skips=True)
    ...     score["StaffGroup"].lilypond_type = "PianoStaff"
    ...     score["StaffGroup"].name = "PianoStaff"
    ...     score["Music.1"].extend("d'4 e' f' g' a' b'")
    ...     score["Music.2"].extend("a4 g f e d c")
    ...     abjad.attach(abjad.TimeSignature((6, 4)), score["Music.1"][0])
    ...     baca.clef(score["Music.2"][0], "bass")
    ...     baca.section.color_octaves(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context PianoStaff = "PianoStaff"
            <<
                \context Staff = "Staff.1"
                {
                    \context Voice = "Music.1"
                    {
                        \time 6/4
                        d'4
                        e'4
                        \baca-octave-coloring
                        f'4
                        - \tweak color #red
                        ^ \markup OCTAVE
                        g'4
                        a'4
                        b'4
                    }
                }
                \context Staff = "Staff.2"
                {
                    \context Voice = "Music.2"
                    {
                        \clef "bass"
                        a4
                        g4
                        \baca-octave-coloring
                        f4
                        - \tweak color #red
                        ^ \markup OCTAVE
                        e4
                        d4
                        c4
                    }
                }
            >>
        }

..  container:: example

    Colors out-of-range pitches:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1, no_skips=True)
    ...     score["Music"].extend("c4 d' e' f'")
    ...     violin = abjad.Violin()
    ...     abjad.attach(violin, score["Music"][0])
    ...     baca.section.color_out_of_range_pitches(score)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Music"
                {
                    \baca-out-of-range-coloring
                    c4
                    d'4
                    e'4
                    f'4
                }
            }
        }

..  container:: example

    Colors repeat pitch-classes.

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1, no_skips=True)
    ...     voice = score["Music"]
    ...     voice.extend("c'4 d' d' e' f' f'' g'2")
    ...     baca.section.color_repeat_pitch_classes(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Music"
                {
                    c'4
                    \baca-repeat-pitch-class-coloring
                    d'4
                    \baca-repeat-pitch-class-coloring
                    d'4
                    e'4
                    \baca-repeat-pitch-class-coloring
                    f'4
                    \baca-repeat-pitch-class-coloring
                    f''4
                    g'2
                }
            }
        }

..  container:: example

    Transposes score:

    >>> def make_lilypond_file():
    ...     clarinet = abjad.ClarinetInBFlat()
    ...     score = baca.docs.make_empty_score(1, no_skips=True)
    ...     voice = score["Music"]
    ...     voice.extend("c'4 d' e' f'")
    ...     abjad.attach(clarinet, voice[0])
    ...     baca.section.transpose_score(score)
    ...     lilypond_file = baca.lilypond.file(score)
    ...     lilypond_file.items.insert(0, r'\language "english"')
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Music"
                {
                    d'4
                    e'4
                    fs'4
                    g'4
                }
            }
        }

"""


def dummy():
    """
    Read module-level examples.
    """

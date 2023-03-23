r"""
Examples.

..  container:: example

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.time_signatures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> abjad.label.with_indices(voice)
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    c'8
                    ^ \markup 0
                    [
                    c'8
                    ^ \markup 1
                    c'8
                    ^ \markup 2
                    c'8
                    ^ \markup 3
                    ]
                    c'8
                    ^ \markup 4
                    [
                    c'8
                    ^ \markup 5
                    c'8
                    ^ \markup 6
                    ]
                    c'8
                    ^ \markup 7
                    [
                    c'8
                    ^ \markup 8
                    c'8
                    ^ \markup 9
                    c'8
                    ^ \markup 10
                    ]
                    c'8
                    ^ \markup 11
                    [
                    c'8
                    ^ \markup 12
                    c'8
                    ^ \markup 13
                    ]
                }
            >>
        }

..  container:: example

    Colors octaves:

    >>> score = baca.docs.make_empty_score(1, 1)
    >>> time_signatures = baca.section.time_signatures([(6, 4)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = abjad.Container("d'4 e' f' g' a' b'")[:]
    >>> score["Music.1"].extend(music)
    >>> music = abjad.Container("a4 g f e d c")[:]
    >>> score["Music.2"].extend(music)
    >>> _ = baca.clef(score["Music.2"][0], "bass")
    >>> baca.section.color_octaves(score)
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context StaffGroup = "StaffGroup"
            <<
                \context Staff = "Staff.1"
                <<
                    \context Voice = "Skips"
                    {
                        \time 6/4
                        s1 * 6/4
                    }
                    \context Voice = "Music.1"
                    {
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
                >>
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

    Transposes score:

    >>> instruments = {}
    >>> instruments["clarinet"] = abjad.ClarinetInBFlat()
    >>> manifests = {"abjad.Instrument": instruments}
    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.time_signatures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.instrument(voice[0], "clarinet", manifests)
    >>> _ = baca.pitches(voice, "E4 F4")
    >>> baca.section.transpose_score(score)
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    fs'8
                    [
                    g'8
                    fs'8
                    g'8
                    ]
                    fs'8
                    [
                    g'8
                    fs'8
                    ]
                    g'8
                    [
                    fs'8
                    g'8
                    fs'8
                    ]
                    g'8
                    [
                    fs'8
                    g'8
                    ]
                }
            >>
        }

..  container:: example

    Does not transpose score:

    >>> instruments = {}
    >>> instruments["clarinet"] = abjad.ClarinetInBFlat()
    >>> manifests = {"abjad.Instrument": instruments}
    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.time_signatures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.instrument(voice[0], "clarinet", manifests)
    >>> _ = baca.pitches(voice, "E4 F4")
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    e'8
                    [
                    f'8
                    e'8
                    f'8
                    ]
                    e'8
                    [
                    f'8
                    e'8
                    ]
                    f'8
                    [
                    e'8
                    f'8
                    e'8
                    ]
                    f'8
                    [
                    e'8
                    f'8
                    ]
                }
            >>
        }

..  container:: example

    Colors out-of-range pitches.

    >>> collections = [
    ...     [4],
    ...     [-12, 2, 3, 5, 8, 9, 0],
    ...     [11],
    ...     [10, 7, 9, 10, 0, 5],
    ... ]
    >>> figures, time_signatures = [], []
    >>> for i, collection in enumerate(collections):
    ...     container = baca.from_collection(collection, [1], 16)
    ...     figures.append([container])
    ...     time_signature = abjad.get.duration(container)
    ...     time_signatures.append(time_signature)
    ...
    >>> figures_ = []
    >>> for figure in figures:
    ...     figures_.extend(figure)
    ...
    >>> figures = list(figures_)
    >>> instruments = {}
    >>> instruments["Violin"] = abjad.Violin()
    >>> manifests = {"abjad.Instrument": instruments}
    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.time_signatures(time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> score["Music"].extend(figures_)
    >>> voice = score["Music"]
    >>> _ = baca.instrument(voice[0], "Violin", manifests)
    >>> baca.section.color_out_of_range_pitches(score)
    >>> abjad.setting(score).autoBeaming = False
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            autoBeaming = ##f
        }
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 1/16
                    s1 * 1/16
                    \time 7/16
                    s1 * 7/16
                    \time 1/16
                    s1 * 1/16
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {
                        e'16
                    }
                    {
                        \baca-out-of-range-coloring
                        c16
                        d'16
                        ef'16
                        f'16
                        af'16
                        a'16
                        c'16
                    }
                    {
                        b'16
                    }
                    {
                        bf'16
                        g'16
                        a'16
                        bf'16
                        c'16
                        f'16
                    }
                }
            >>
        }

..  container:: example

    Colors repeat pitch-classes.

    >>> collections = [
    ...     [4],
    ...     [6, 2, 3, 5, 9, 9, 0],
    ...     [11],
    ...     [10, 7, 9, 12, 0, 5],
    ... ]
    >>> figures, time_signatures = [], []
    >>> for i, collection in enumerate(collections):
    ...     container = baca.from_collection(collection, [1], 16)
    ...     figures.append([container])
    ...     time_signature = abjad.get.duration(container)
    ...     time_signatures.append(time_signature)
    ...
    >>> figures_ = []
    >>> for figure in figures:
    ...     figures_.extend(figure)
    ...
    >>> figures = list(figures_)
    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.time_signatures(time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> score["Music"].extend(figures_)
    >>> baca.section.color_repeat_pitch_classes(score)
    >>> abjad.setting(score).autoBeaming = False
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            autoBeaming = ##f
        }
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 1/16
                    s1 * 1/16
                    \time 7/16
                    s1 * 7/16
                    \time 1/16
                    s1 * 1/16
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {
                        e'16
                    }
                    {
                        fs'16
                        d'16
                        ef'16
                        f'16
                        \baca-repeat-pitch-class-coloring
                        a'16
                        \baca-repeat-pitch-class-coloring
                        a'16
                        c'16
                    }
                    {
                        b'16
                    }
                    {
                        bf'16
                        g'16
                        a'16
                        \baca-repeat-pitch-class-coloring
                        c''16
                        \baca-repeat-pitch-class-coloring
                        c'16
                        f'16
                    }
                }
            >>
        }

"""


def dummy():
    """
    Read module-level examples.
    """

r"""
Segment-commands scope examples.

Wraps each command in ``commands`` with each scope in ``scopes``.

..  container:: example

    >>> score = baca.docs.make_empty_score(1)
    >>> commands = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )

    >>> commands(
    ...     "MusicVoice",
    ...     baca.make_even_divisions(),
    ...     baca.label(lambda _: abjad.label.with_indices(_)),
    ... )

    >>> _, _ = baca.interpreter(
    ...     score,
    ...     commands.commands,
    ...     commands.time_signatures,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.make_lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Music_Staff"
            <<
                \context Voice = "GlobalSkips"
                {
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "MusicVoice"
                {
                    b'8
                    ^ \markup 0
                    [
                    b'8
                    ^ \markup 1
                    b'8
                    ^ \markup 2
                    b'8
                    ^ \markup 3
                    ]
                    b'8
                    ^ \markup 4
                    [
                    b'8
                    ^ \markup 5
                    b'8
                    ^ \markup 6
                    ]
                    b'8
                    ^ \markup 7
                    [
                    b'8
                    ^ \markup 8
                    b'8
                    ^ \markup 9
                    b'8
                    ^ \markup 10
                    ]
                    b'8
                    ^ \markup 11
                    [
                    b'8
                    ^ \markup 12
                    b'8
                    ^ \markup 13
                    ]
                }
            >>
        }

..  container:: example

    Commands may be grouped into lists:

    >>> score = baca.docs.make_empty_score(1)
    >>> voice_names = baca.accumulator.get_voice_names(score)
    >>> commands = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ...     voice_names=voice_names,
    ... )

    >>> list_ = []
    >>> list_.append(baca.make_even_divisions())
    >>> list_.append(baca.label(lambda _: abjad.label.with_indices(_)))

    >>> commands(
    ...     "MusicVoice",
    ...     list_,
    ... )

    >>> _, _ = baca.interpreter(
    ...     score,
    ...     commands.commands,
    ...     commands.time_signatures,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.make_lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Music_Staff"
            <<
                \context Voice = "GlobalSkips"
                {
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "MusicVoice"
                {
                    b'8
                    ^ \markup 0
                    [
                    b'8
                    ^ \markup 1
                    b'8
                    ^ \markup 2
                    b'8
                    ^ \markup 3
                    ]
                    b'8
                    ^ \markup 4
                    [
                    b'8
                    ^ \markup 5
                    b'8
                    ^ \markup 6
                    ]
                    b'8
                    ^ \markup 7
                    [
                    b'8
                    ^ \markup 8
                    b'8
                    ^ \markup 9
                    b'8
                    ^ \markup 10
                    ]
                    b'8
                    ^ \markup 11
                    [
                    b'8
                    ^ \markup 12
                    b'8
                    ^ \markup 13
                    ]
                }
            >>
        }

..  container:: example exception

    Raises exception on noncommand input:

    >>> commands(
    ...     "MusicVoice",
    ...     "text",
    ... )
    Traceback (most recent call last):
        ...
    Exception:
    Must be command:
    'text'

..  container:: example exception

    Raises exception on unknown voice name:

    >>> commands(
    ...     "Percussion_Voice",
    ...     baca.make_repeated_duration_notes([(1, 4)]),
    ... )
    Traceback (most recent call last):
        ...
    Exception: unknown voice name 'Percussion_Voice'.

..  container:: example

    Colors octaves:

    >>> score = baca.docs.make_empty_score(1, 1)
    >>> commands = baca.CommandAccumulator(
    ...     time_signatures=[(6, 4)],
    ... )

    >>> commands(
    ...     ("Music_Voice_1", 1),
    ...     baca.make_music(abjad.Container("d'4 e' f' g' a' b'")[:]),
    ... )

    >>> commands(
    ...     ("Music_Voice_2", 1),
    ...     baca.make_music(abjad.Container("a4 g f e d c")[:]),
    ...     baca.clef("bass"),
    ... )

    >>> _, _ = baca.interpreter(
    ...     score,
    ...     commands.commands,
    ...     commands.time_signatures,
    ...     color_octaves=True,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.make_lilypond_file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context StaffGroup = "Music_Staff_Group"
            <<
                \context Staff = "Music_Staff_1"
                <<
                    \context Voice = "GlobalSkips"
                    {
                        \time 6/4
                        s1 * 3/2
                    }
                    \context Voice = "Music_Voice_1"
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
                \context Staff = "Music_Staff_2"
                {
                    \context Voice = "Music_Voice_2"
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
    >>> score = baca.docs.make_empty_score(1)
    >>> commands = baca.CommandAccumulator(
    ...     instruments=instruments,
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )

    >>> commands(
    ...     "MusicVoice",
    ...     baca.make_even_divisions(),
    ...     baca.instrument(instruments["clarinet"]),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> _, _ = baca.interpreter(
    ...     score,
    ...     commands.commands,
    ...     commands.time_signatures,
    ...     instruments=commands.instruments,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ...     transpose_score=True,
    ... )
    >>> lilypond_file = baca.make_lilypond_file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Music_Staff"
            <<
                \context Voice = "GlobalSkips"
                {
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "MusicVoice"
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
    >>> score = baca.docs.make_empty_score(1)
    >>> commands = baca.CommandAccumulator(
    ...     instruments=instruments,
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )

    >>> commands(
    ...     "MusicVoice",
    ...     baca.make_even_divisions(),
    ...     baca.instrument(instruments["clarinet"]),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> _, _ = baca.interpreter(
    ...     score,
    ...     commands.commands,
    ...     commands.time_signatures,
    ...     instruments=commands.instruments,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ...     transpose_score=False,
    ... )
    >>> lilypond_file = baca.make_lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Music_Staff"
            <<
                \context Voice = "GlobalSkips"
                {
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "MusicVoice"
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

    >>> figure = baca.figure([1], 16)
    >>> collection_lists = [
    ...     [[4]],
    ...     [[-12, 2, 3, 5, 8, 9, 0]],
    ...     [[11]],
    ...     [[10, 7, 9, 10, 0, 5]],
    ... ]
    >>> figures, time_signatures = [], []
    >>> for i, collections in enumerate(collection_lists):
    ...     selection = figure(collections)
    ...     figures.append(selection)
    ...     time_signature = abjad.get.duration(selection)
    ...     time_signatures.append(time_signature)
    ...
    >>> figures_ = []
    >>> for figure in figures:
    ...     figures_.extend(figure)
    ...
    >>> figures = list(figures_)

    >>> instruments = {}
    >>> instruments["Violin"] = abjad.Violin()

    >>> score = baca.docs.make_empty_score(1)
    >>> commands = baca.CommandAccumulator(
    ...     instruments=instruments,
    ...     time_signatures=time_signatures,
    ... )
    >>> commands(
    ...     ("MusicVoice", 1),
    ...     baca.make_music(figures_, do_not_check_total_duration=True),
    ...     baca.instrument(abjad.Violin()),
    ... )

    >>> _, _ = baca.interpreter(
    ...     score,
    ...     commands.commands,
    ...     commands.time_signatures,
    ...     instruments=instruments,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> abjad.setting(score).autoBeaming = False
    >>> lilypond_file = baca.make_lilypond_file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
            \context Staff = "Music_Staff"
            <<
                \context Voice = "GlobalSkips"
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
                \context Voice = "MusicVoice"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        e'16
                    }
                    \scaleDurations #'(1 . 1)
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
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                    }
                    \scaleDurations #'(1 . 1)
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

    >>> figure = baca.figure([1], 16)
    >>> collection_lists = [
    ...     [[4]],
    ...     [[6, 2, 3, 5, 9, 9, 0]],
    ...     [[11]],
    ...     [[10, 7, 9, 12, 0, 5]],
    ... ]
    >>> figures, time_signatures = [], []
    >>> for i, collections in enumerate(collection_lists):
    ...     selection = figure(collections)
    ...     figures.append(selection)
    ...     time_signature = abjad.get.duration(selection)
    ...     time_signatures.append(time_signature)
    ...
    >>> figures_ = []
    >>> for figure in figures:
    ...     figures_.extend(figure)
    ...
    >>> figures = list(figures_)

    >>> score = baca.docs.make_empty_score(1)
    >>> commands = baca.CommandAccumulator(
    ...     time_signatures=time_signatures,
    ... )
    >>> commands(
    ...     ("MusicVoice", 1),
    ...     baca.make_music(figures, do_not_check_total_duration=True),
    ... )

    >>> _, _ = baca.interpreter(
    ...     score,
    ...     commands.commands,
    ...     commands.time_signatures,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> abjad.setting(score).autoBeaming = False
    >>> lilypond_file = baca.make_lilypond_file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
            \context Staff = "Music_Staff"
            <<
                \context Voice = "GlobalSkips"
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
                \context Voice = "MusicVoice"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        e'16
                    }
                    \scaleDurations #'(1 . 1)
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
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                    }
                    \scaleDurations #'(1 . 1)
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


def example():
    """
    Read module-level examples.
    """

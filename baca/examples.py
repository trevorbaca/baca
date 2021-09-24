r"""
Segment-maker scope examples.

Wraps each command in ``commands`` with each scope in ``scopes``.

..  container:: example

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.make_empty_score_maker(1),
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.label(lambda _: abjad.label.with_indices(_)),
    ... )

    >>> lilypond_file = maker.run(
    ...     environment="docs",
    ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Voice = "Global_Skips"
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
                \context Voice = "Music_Voice"
                {
                    b'8
                    ^ \markup { 0 }
                    [
                    b'8
                    ^ \markup { 1 }
                    b'8
                    ^ \markup { 2 }
                    b'8
                    ^ \markup { 3 }
                    ]
                    b'8
                    ^ \markup { 4 }
                    [
                    b'8
                    ^ \markup { 5 }
                    b'8
                    ^ \markup { 6 }
                    ]
                    b'8
                    ^ \markup { 7 }
                    [
                    b'8
                    ^ \markup { 8 }
                    b'8
                    ^ \markup { 9 }
                    b'8
                    ^ \markup { 10 }
                    ]
                    b'8
                    ^ \markup { 11 }
                    [
                    b'8
                    ^ \markup { 12 }
                    b'8
                    ^ \markup { 13 }
                    ]
                }
            >>
        }

..  container:: example

    Commands may be grouped into lists:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.make_empty_score_maker(1),
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )

    >>> commands = []
    >>> commands.append(baca.make_even_divisions())
    >>> commands.append(baca.label(lambda _: abjad.label.with_indices(_)))

    >>> maker(
    ...     "Music_Voice",
    ...     commands,
    ... )

    >>> lilypond_file = maker.run(
    ...     environment="docs",
    ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Voice = "Global_Skips"
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
                \context Voice = "Music_Voice"
                {
                    b'8
                    ^ \markup { 0 }
                    [
                    b'8
                    ^ \markup { 1 }
                    b'8
                    ^ \markup { 2 }
                    b'8
                    ^ \markup { 3 }
                    ]
                    b'8
                    ^ \markup { 4 }
                    [
                    b'8
                    ^ \markup { 5 }
                    b'8
                    ^ \markup { 6 }
                    ]
                    b'8
                    ^ \markup { 7 }
                    [
                    b'8
                    ^ \markup { 8 }
                    b'8
                    ^ \markup { 9 }
                    b'8
                    ^ \markup { 10 }
                    ]
                    b'8
                    ^ \markup { 11 }
                    [
                    b'8
                    ^ \markup { 12 }
                    b'8
                    ^ \markup { 13 }
                    ]
                }
            >>
        }

..  container:: example exception

    Raises exception on noncommand input:

    >>> maker(
    ...     "Music_Voice",
    ...     "text",
    ... )
    Traceback (most recent call last):
        ...
    Exception:
    Must be command:
    'text'

..  container:: example exception

    Raises exception on unknown voice name:

    >>> maker(
    ...     "Percussion_Voice",
    ...     baca.make_repeated_duration_notes([(1, 4)]),
    ... )
    Traceback (most recent call last):
        ...
    Exception: unknown voice name 'Percussion_Voice'.

..  container:: example

    Colors octaves:

    >>> def closure():
    ...     return baca.make_empty_score(1, 1)

    >>> maker = baca.SegmentMaker(
    ...     score_template=closure,
    ...     time_signatures=[(6, 4)],
    ... )

    >>> maker(
    ...     ("Music_Voice_1", 1),
    ...     baca.music(abjad.Container("d'4 e' f' g' a' b'")[:]),
    ... )

    >>> maker(
    ...     ("Music_Voice_2", 1),
    ...     baca.music(abjad.Container("a4 g f e d c")[:]),
    ...     baca.clef("bass"),
    ... )

    >>> lilypond_file = maker.run(
    ...     color_octaves=True,
    ...     environment="docs",
    ...     includes=["baca.ily"],
    ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                    \context Voice = "Global_Skips"
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
                        ^ \markup { OCTAVE }
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
                        ^ \markup { OCTAVE }
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
    >>> maker = baca.SegmentMaker(
    ...     instruments=instruments,
    ...     score_template=baca.make_empty_score_maker(1),
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.instrument(instruments["clarinet"]),
    ...     baca.make_even_divisions(),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> lilypond_file = maker.run(
    ...     environment="docs",
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ...     transpose_score=True,
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
                \context Voice = "Global_Skips"
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
                \context Voice = "Music_Voice"
                {
                    fs'!8
                    [
                    g'8
                    fs'!8
                    g'8
                    ]
                    fs'!8
                    [
                    g'8
                    fs'!8
                    ]
                    g'8
                    [
                    fs'!8
                    g'8
                    fs'!8
                    ]
                    g'8
                    [
                    fs'!8
                    g'8
                    ]
                }
            >>
        }

..  container:: example

    Does not transpose score:

    >>> instruments = {}
    >>> instruments["clarinet"] = abjad.ClarinetInBFlat()
    >>> maker = baca.SegmentMaker(
    ...     instruments=instruments,
    ...     score_template=baca.make_empty_score_maker(1),
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.instrument(instruments["clarinet"]),
    ...     baca.make_even_divisions(),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> lilypond_file = maker.run(
    ...     environment="docs",
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ...     transpose_score=False,
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
                \context Voice = "Global_Skips"
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
                \context Voice = "Music_Voice"
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

"""


def example():
    """
    Read module-level examples.
    """

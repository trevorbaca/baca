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

    >>> lilypond_file = maker.run(environment="docs")
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

    >>> lilypond_file = maker.run(environment="docs")
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

"""


def example():
    """
    Read module-level examples.
    """

r"""
Examples: spanners.

..  container:: example

    Beams everything and sets beam direction down:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier(fallback_duration=(1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch(voice, "C4")
    >>> _ = baca.beam(voice, direction=abjad.DOWN)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    c'8
                    _ [
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    ]
                }
            >>
        }

..  container:: example

    Attaches ottava indicators to trimmed leaves:

    >>> container = abjad.Container("r8 d'4 e' r8")
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> _ = baca.ottava(baca.select.tleaves(container))
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \time 3/4
                        r8
                        \ottava 1
                        d'4
                        e'4
                        \ottava 0
                        r8
                    }
                }
            }
        }

..  container:: example

    Attaches ottava bassa indicators to trimmed leaves:

    >>> container = abjad.Container("r8 d'4 e' r8")
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> _ = baca.ottava_bassa(baca.select.tleaves(container))
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \time 3/4
                        r8
                        \ottava -1
                        d'4
                        e'4
                        \ottava 0
                        r8
                    }
                }
            }
        }

..  container:: example

    Attaches slur to trimmed leaves:

    >>> container = abjad.Container("r8 d'4 e' r8")
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> _ = baca.slur(baca.select.tleaves(container))
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \time 3/4
                        r8
                        d'4
                        (
                        e'4
                        )
                        r8
                    }
                }
            }
        }

..  container:: example

    Pedals leaves:

    >>> container = abjad.Container("r8 d'4 e' r8")
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> _ = baca.sustain_pedal(container, context="Staff")
    >>> _ = baca.override.sustain_pedal_staff_padding(container, 6)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \override Staff.SustainPedalLineSpanner.staff-padding = 6
                        \time 3/4
                        r8
                        \sustainOn
                        d'4
                        e'4
                        r8
                        \sustainOff
                        \revert Staff.SustainPedalLineSpanner.staff-padding
                    }
                }
            }
        }

..  container:: example

    Attaches trill spanner to trimmed leaves (leaked to the right):

    >>> container = abjad.Container("r8 d'4 e' r8")
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> _ = baca.trill_spanner(baca.select.tleaves(container, rleak=True))
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \time 3/4
                        r8
                        d'4
                        \startTrillSpan
                        e'4
                        r8
                        \stopTrillSpan
                    }
                }
            }
        }

..  container:: example

    Tweaks trill spanner:

    >>> container = abjad.Container("r8 d'4 e' r8")
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> _ = baca.trill_spanner(
    ...     baca.select.tleaves(container, rleak=True),
    ...     abjad.Tweak(r"- \tweak color #red"),
    ...     alteration="M2",
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \time 3/4
                        r8
                        \pitchedTrill
                        d'4
                        - \tweak color #red
                        \startTrillSpan e'
                        e'4
                        r8
                        \stopTrillSpan
                    }
                }
            }
        }

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass

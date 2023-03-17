r"""
articulations.py examples.

..  container:: example

    **COLOR FINGERINGS.**

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.time_signatures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch(voice, "E4")
    >>> _ = baca.color_fingerings(voice, numbers=[0, 1, 2, 1])
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    e'2
                    e'4.
                    ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                    e'2
                    ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }
                    e'4.
                    ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                }
            >>
        }

..  container:: example

    **STOP-ON-STRING.**

    >>> container = abjad.Container("c'4 d' e'")
    >>> _ = baca.stop_on_string(container[0])
    >>> lilypond_file = abjad.illustrators.components([container], includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \time 3/4
                    c'4
                    - \baca-stop-on-string
                    d'4
                    e'4
                }
            }
        >>

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass

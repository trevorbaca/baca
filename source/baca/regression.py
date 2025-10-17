"""
Regression.
"""


def test():
    r"""
    Regression.

    ..  container:: example

        Unbeams 1 note:

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[:1])
        >>> baca.rhythm._repair_unmatched_beams(voice[:1])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        [
                        e'8
                        f'8
                        g'8
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[1:2])
        >>> baca.rhythm._repair_unmatched_beams(voice[1:2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        [
                        f'8
                        g'8
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[2:3])
        >>> baca.rhythm._repair_unmatched_beams(voice[2:3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        [
                        d'8
                        ]
                        e'8
                        f'8
                        [
                        g'8
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[3:4])
        >>> baca.rhythm._repair_unmatched_beams(voice[3:4])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        [
                        d'8
                        e'8
                        ]
                        f'8
                        g'8
                        [
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[4:5])
        >>> baca.rhythm._repair_unmatched_beams(voice[4:5])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        [
                        d'8
                        e'8
                        f'8
                        ]
                        g'8
                        a'8
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[5:6])
        >>> baca.rhythm._repair_unmatched_beams(voice[5:6])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        [
                        d'8
                        e'8
                        f'8
                        g'8
                        ]
                        a'8
                    }
                }
            >>

    ..  container:: example

        Unbeams 2 notes:

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[:2])
        >>> baca.rhythm._repair_unmatched_beams(voice[:2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        [
                        f'8
                        g'8
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[1:3])
        >>> baca.rhythm._repair_unmatched_beams(voice[1:3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                        [
                        g'8
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[2:4])
        >>> baca.rhythm._repair_unmatched_beams(voice[2:4])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        [
                        d'8
                        ]
                        e'8
                        f'8
                        g'8
                        [
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[3:5])
        >>> baca.rhythm._repair_unmatched_beams(voice[3:5])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        [
                        d'8
                        e'8
                        ]
                        f'8
                        g'8
                        a'8
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' e' f' g' a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[4:])
        >>> baca.rhythm._repair_unmatched_beams(voice[4:])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        [
                        d'8
                        e'8
                        f'8
                        ]
                        g'8
                        a'8
                    }
                }
            >>

    ..  container:: example

        Unbeams 1 note:

        >>> voice = abjad.Voice("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[:1])
        >>> baca.rhythm._repair_unmatched_beams(voice[:1])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        [
                        f'8
                        ]
                        g'8
                        [
                        a'8
                        ]
                    }
                }
            >>

        >>> voice = abjad.Voice("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(voice[1:2])
        >>> baca.rhythm._repair_unmatched_beams(voice[1:2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        [
                        f'8
                        ]
                        g'8
                        [
                        a'8
                        ]
                    }
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[2:3])
        >>> baca.rhythm._repair_unmatched_beams(staff[2:3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    f'8
                    g'8
                    [
                    a'8
                    ]
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[3:4])
        >>> baca.rhythm._repair_unmatched_beams(staff[3:4])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    f'8
                    g'8
                    [
                    a'8
                    ]
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[4:5])
        >>> baca.rhythm._repair_unmatched_beams(staff[4:5])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    [
                    f'8
                    ]
                    g'8
                    a'8
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[5:6])
        >>> baca.rhythm._repair_unmatched_beams(staff[5:6])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    [
                    f'8
                    ]
                    g'8
                    a'8
                }
            >>

    ..  container:: example

        Unbeams 2 notes:

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[:2])
        >>> baca.rhythm._repair_unmatched_beams(staff[:2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    [
                    f'8
                    ]
                    g'8
                    [
                    a'8
                    ]
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[1:3])
        >>> baca.rhythm._repair_unmatched_beams(staff[1:3])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                    [
                    a'8
                    ]
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[2:4])
        >>> baca.rhythm._repair_unmatched_beams(staff[2:4])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    f'8
                    g'8
                    [
                    a'8
                    ]
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[3:5])
        >>> baca.rhythm._repair_unmatched_beams(staff[3:5])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    f'8
                    g'8
                    a'8
                }
            >>

        >>> staff = abjad.Staff("c'8 [ d' ] e' [ f' ] g' [ a' ]")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(score).autoBeaming = False
        >>> rmakers.detach_beams_from_leaves(staff[4:])
        >>> baca.rhythm._repair_unmatched_beams(staff[4:])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                autoBeaming = ##f
            }
            <<
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    [
                    f'8
                    ]
                    g'8
                    a'8
                }
            >>


    """
    pass

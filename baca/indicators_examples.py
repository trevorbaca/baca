r"""
indicatorcommands.py examples.

..  container:: example

    Attaches RIGHT_BROKEN_BEAM to selector output.

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)

    >>> figures(
    ...     "Music.2",
    ...     [[0, 2, 10, 18], [16, 15, 23]],
    ...     baca.figure([1], 16),
    ...     rmakers.beam_groups(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 10],
    ...         baca.staccato(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...         baca.extend_beam(selector=lambda _: abjad.select.leaf(_, -1)),
    ...     ),
    ... )

    >>> figures(
    ...     "Music.2",
    ...     [[19, 13, 9, 8]],
    ...     baca.figure([1], 16),
    ...     rmakers.beam_groups(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [13, 9],
    ...         baca.staccato(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...     ),
    ... )

    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> baca.interpret.set_up_score(
    ...     score,
    ...     accumulator,
    ...     {},
    ...     accumulator.time_signatures,
    ...     docs=True,
    ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
    ... )
    >>> figures.populate_commands(score, accumulator)

    >>> accumulator(
    ...     "Music.1",
    ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
    ... )

    >>> accumulator(
    ...     "Music.2",
    ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
    ... )

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
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
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \baca-new-spacing-section #1 #32
                    \time 7/16
                    s1 * 7/16
                    \baca-new-spacing-section #1 #32
                    \time 1/4
                    s1 * 1/4
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceOne
                            s16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \staccato
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            s16
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            cs''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \staccato
                            s16
                            ]
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            \voiceTwo
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            fs''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            b''16
                            ]
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            g''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            cs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            af'16
                            ]
                        }
                    }
                }
            >>
        }

"""


def dummy():
    """
    Read module-level examples.
    """

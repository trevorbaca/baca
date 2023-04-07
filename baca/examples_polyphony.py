r"""
LilyPond polyphony examples.

..  container:: example

    >>> def make_score():
    ...     voice = abjad.Voice(name="Voice")
    ...     voice.extend(r"c'4 c'4 ( c'2 )")
    ...     voice.extend(r"c'4 c'4 c'2")
    ...     bgc = abjad.BeforeGraceContainer("c'16", command=r"\acciaccatura")
    ...     abjad.attach(bgc, voice[-2])
    ...     voice.extend(r"c'4 c'4 c'2")
    ...     bgc = abjad.BeforeGraceContainer("c'16 [ c'16 ]", command=r"\acciaccatura")
    ...     abjad.attach(bgc, voice[-2])
    ...     voice.extend(r"c'4 c'4 c'2")
    ...     bgc = abjad.BeforeGraceContainer("c'16 [ c'16 ]")
    ...     abjad.attach(bgc, voice[-2])
    ...     leaves = abjad.select.leaves(voice)
    ...     abjad.slur(leaves[-4:-1])
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff", name="Staff")
    ...     score = abjad.Score([staff], name="Score")
    ...     return score

..  container:: example

    **GRACED SLURS #1.** LilyPond engraves graced slurs correctly in monophony,
    both implicit and explicit:

    >>> def make_lilypond_file():
    ...     score = make_score()
    ...     lilypond_file_ = abjad.LilyPondFile([score])
    ...     return lilypond_file_

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> voice = lilypond_file["Voice"]
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \context Voice = "Voice"
        {
            c'4
            c'4
            (
            c'2
            )
            c'4
            \acciaccatura {
                c'16
            }
            c'4
            c'2
            c'4
            \acciaccatura {
                c'16
                [
                c'16
                ]
            }
            c'4
            c'2
            c'4
            \grace {
                c'16
                [
                (
                c'16
                ]
            }
            c'4
            )
            c'2
        }

    >>> def make_lilypond_file():
    ...     score = make_score()
    ...     leaf = abjad.select.leaf(score, 0)
    ...     command = abjad.VoiceNumber()
    ...     abjad.attach(command, leaf)
    ...     lilypond_file_ = abjad.LilyPondFile([score])
    ...     return lilypond_file_

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> voice = lilypond_file["Voice"]
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \context Voice = "Voice"
        {
            \oneVoice
            c'4
            c'4
            (
            c'2
            )
            c'4
            \acciaccatura {
                c'16
            }
            c'4
            c'2
            c'4
            \acciaccatura {
                c'16
                [
                c'16
                ]
            }
            c'4
            c'2
            c'4
            \grace {
                c'16
                [
                (
                c'16
                ]
            }
            c'4
            )
            c'2
        }

..  container:: example

    **GRACED SLURS #2.** In polyphony, LilyPond's graced slurs are sometimes a
    bit of a mess:

    >>> def make_lilypond_file():
    ...     score = make_score()
    ...     leaves = abjad.select.leaves(score)
    ...     command = abjad.VoiceNumber(1)
    ...     abjad.attach(command, leaves[0])
    ...     baca.color([leaves[-4:-1]])
    ...     baca.color([leaves[-9:-6]])
    ...     lilypond_file_ = baca.lilypond.file(score, includes=["abjad.ily"])
    ...     return lilypond_file_

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> voice = lilypond_file["Voice"]
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \context Voice = "Voice"
        {
            \voiceOne
            c'4
            c'4
            (
            c'2
            )
            c'4
            \acciaccatura {
                c'16
            }
            c'4
            c'2
            c'4
            \acciaccatura {
                \abjad-color-music #'red
                c'16
                [
                \abjad-color-music #'red
                c'16
                ]
            }
            \abjad-color-music #'red
            c'4
            c'2
            c'4
            \grace {
                \abjad-color-music #'red
                c'16
                [
                (
                \abjad-color-music #'red
                c'16
                ]
            }
            \abjad-color-music #'red
            c'4
            )
            c'2
        }

    >>> def make_lilypond_file():
    ...     score = make_score()
    ...     leaves = abjad.select.leaves(score)
    ...     command = abjad.VoiceNumber(2)
    ...     abjad.attach(command, leaves[0])
    ...     baca.color([leaves[-4:-1]])
    ...     baca.color([leaves[-9:-6]])
    ...     lilypond_file_ = baca.lilypond.file(score, includes=["abjad.ily"])
    ...     return lilypond_file_

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> voice = lilypond_file["Voice"]
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \context Voice = "Voice"
        {
            \voiceTwo
            c'4
            c'4
            (
            c'2
            )
            c'4
            \acciaccatura {
                c'16
            }
            c'4
            c'2
            c'4
            \acciaccatura {
                \abjad-color-music #'red
                c'16
                [
                \abjad-color-music #'red
                c'16
                ]
            }
            \abjad-color-music #'red
            c'4
            c'2
            c'4
            \grace {
                \abjad-color-music #'red
                c'16
                [
                (
                \abjad-color-music #'red
                c'16
                ]
            }
            \abjad-color-music #'red
            c'4
            )
            c'2
        }

"""


def sphinx():
    """
    Makes Sphinx read this module.
    """
    pass

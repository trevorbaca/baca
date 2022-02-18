"""
Pitch commands.
"""
import collections
import copy
import dataclasses
import numbers
import typing
from inspect import currentframe as _frame

import abjad

from . import const as _const
from . import pitchclasses as _pitchclasses
from . import scoping as _scoping
from . import selection as _selection
from . import selectors as _selectors


@dataclasses.dataclass
class AccidentalAdjustmentCommand(_scoping.Command):
    r"""
    Accidental adjustment command.

    ..  container:: example

        >>> baca.AccidentalAdjustmentCommand()
        AccidentalAdjustmentCommand()

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.force_accidental(selector=baca.selectors.pleaves((None, 2))),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        e'!2
                        f'!4.
                        e'2
                        f'4.
                    }
                >>
            }

    """

    cautionary: bool = None
    forced: bool = None
    parenthesized: bool = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.cautionary is not None:
            self.cautionary = bool(self.cautionary)
        if self.forced is not None:
            self.forced = bool(self.forced)
        if self.parenthesized is not None:
            self.parenthesized = bool(self.parenthesized)

    __repr__ = _scoping.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.tag:
            if not self.tag.only_edition() and not self.tag.not_editions():
                raise Exception(f"tag must have edition: {self.tag!r}.")
            tag = _scoping.site(_frame(), self)
            alternative_tag = self.tag.append(tag)
            primary_tag = alternative_tag.invert_edition_tags()
        pleaves = _selection.Selection(argument).pleaves()
        assert isinstance(pleaves, _selection.Selection)
        for pleaf in pleaves:
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                assert isinstance(pleaf, abjad.Chord)
                note_heads = pleaf.note_heads
            for note_head in note_heads:
                assert note_head is not None
                if not self.tag:
                    if self.cautionary:
                        note_head.is_cautionary = True
                    if self.forced:
                        note_head.is_forced = True
                    if self.parenthesized:
                        note_head.is_parenthesized = True
                else:
                    alternative = copy.copy(note_head)
                    if self.cautionary:
                        alternative.is_cautionary = True
                    if self.forced:
                        alternative.is_forced = True
                    if self.parenthesized:
                        alternative.is_parenthesized = True
                    note_head.alternative = (
                        alternative,
                        str(alternative_tag),
                        str(primary_tag),
                    )


@dataclasses.dataclass
class ClusterCommand(_scoping.Command):
    r"""
    Cluster command.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clusters([3, 4]),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        \time 9/16
                        <c' e' g'>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a' c''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <bf' d'' f''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <fs'' a'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'' g'' b''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <ef'' g'' b'' d'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <af'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g'' b'' d''' f'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <a' c'' e''>16
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                }
            >>

    ..  container:: example

        Hides flat markup:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitch("E4"),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.natural_clusters(widths=[3]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                    }
                >>
            }

    ..  container:: example

        Takes start pitch from input notes:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches("C4 D4 E4 F4"),
        ...     baca.clusters([3]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <c' e' g'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <f' a' c''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Sets start pitch explicitly:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.clusters([3], start_pitch="G4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Increasing widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.clusters([1, 2, 3, 4], start_pitch="E4"),
        ...     baca.make_notes(repeat_ties=True),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Patterned widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.clusters([1, 3], start_pitch="E4"),
        ...     baca.make_notes(repeat_ties=True),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Leaves notes and chords unchanged:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitch("E4"),
        ...     baca.clusters([]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        e'2
                        e'4.
                        e'2
                        e'4.
                    }
                >>
            }

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.

    """

    hide_flat_markup: bool = None
    selector: typing.Any = _selectors.plts()
    start_pitch: typing.Any = None
    widths: typing.Any = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        assert isinstance(self.hide_flat_markup, (bool, type(None)))
        if self.start_pitch is not None:
            self.start_pitch = abjad.NamedPitch(self.start_pitch)
        assert abjad.math.all_are_nonnegative_integers(self.widths)
        self.widths = abjad.CyclicTuple(self.widths)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = _selection.Selection(argument).leaf(0)
        root = abjad.get.parentage(leaf).root
        with abjad.ForbidUpdate(component=root):
            for i, plt in enumerate(_selection.Selection(argument).plts()):
                width = self.widths[i]
                self._make_cluster(plt, width)

    def _make_cluster(self, plt, width):
        assert plt.is_pitched, repr(plt)
        if not width:
            return
        if self.start_pitch is not None:
            start_pitch = self.start_pitch
        else:
            start_pitch = plt.head.written_pitch
        pitches = self._make_pitches(start_pitch, width)
        key_cluster = abjad.KeyCluster(include_flat_markup=not self.hide_flat_markup)
        for pleaf in plt:
            chord = abjad.Chord(pitches, pleaf.written_duration)
            indicators = abjad.detach(object, pleaf)
            for indicator in indicators:
                abjad.attach(indicator, chord)
            abjad.mutate.replace(pleaf, chord)
            abjad.attach(key_cluster, chord)
            abjad.attach(_const.ALLOW_REPEAT_PITCH, chord)
            abjad.detach(_const.NOT_YET_PITCHED, chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width - 1):
            pitch = pitches[-1] + abjad.NamedInterval("M3")
            pitch = abjad.NamedPitch(pitch, accidental="natural")
            assert pitch.accidental == abjad.Accidental("natural")
            pitches.append(pitch)
        return pitches

    def _mutates_score(self):
        return True


@dataclasses.dataclass
class ColorFingeringCommand(_scoping.Command):
    r"""
    Color fingering command.

    ..  container:: example

        With segment-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitch("E4"),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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

    """

    numbers: typing.Any = None
    tweaks: abjad.IndexedTweakManagers = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.numbers is not None:
            assert abjad.math.all_are_nonnegative_integers(self.numbers)
            self.numbers = abjad.CyclicTuple(self.numbers)
        _scoping.validate_indexed_tweaks(self.tweaks)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        pheads = _selection.Selection(argument).pheads()
        total = len(pheads)
        for i, phead in enumerate(pheads):
            number = self.numbers[i]
            if number != 0:
                fingering = abjad.ColorFingering(number)
                _scoping.apply_tweaks(fingering, self.tweaks, i=i, total=total)
                abjad.attach(fingering, phead)


@dataclasses.dataclass
class DiatonicClusterCommand(_scoping.Command):
    r"""
    Diatonic cluster command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> command = baca.diatonic_clusters([4, 6])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    """

    widths: typing.Any = None
    selector: typing.Any = _selectors.plts()

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        assert abjad.math.all_are_nonnegative_integers(self.widths)
        self.widths = abjad.CyclicTuple(self.widths)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, plt in enumerate(_selection.Selection(argument).plts()):
            width = self.widths[i]
            start = self._get_lowest_diatonic_pitch_number(plt)
            numbers = range(start, start + width)
            change = abjad.pitch._diatonic_pc_number_to_pitch_class_number
            numbers_ = [(12 * (x // 7)) + change[x % 7] for x in numbers]
            pitches = [abjad.NamedPitch(_) for _ in numbers_]
            for pleaf in plt:
                chord = abjad.Chord(pleaf)
                chord.note_heads[:] = pitches
                abjad.mutate.replace(pleaf, chord)

    def _get_lowest_diatonic_pitch_number(self, plt):
        if isinstance(plt.head, abjad.Note):
            pitch = plt.head.written_pitch
        elif isinstance(plt.head, abjad.Chord):
            pitch = plt.head.written_pitches[0]
        else:
            raise TypeError(plt)
        return pitch._get_diatonic_pitch_number()

    def _mutates_score(self):
        return True


@dataclasses.dataclass(slots=True)
class Loop(abjad.CyclicTuple):
    """
    Loop.

    ..  container:: example

        >>> loop = baca.Loop([0, 2, 4], intervals=[1])
        >>> loop
        Loop(items=CyclicTuple(items=(NamedPitch("c'"), NamedPitch("d'"), NamedPitch("e'"))), intervals=CyclicTuple(items=(1,)))

        >>> for i in range(12):
        ...     loop[i]
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("cs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("fs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("g'")

        >>> isinstance(loop, abjad.CyclicTuple)
        True

    ..  container:: example

        >>> command = baca.loop([0, 2, 4], [1])
        >>> command
        PitchCommand()

    """

    intervals: typing.Any = None

    def __post_init__(self):
        if self.items is not None:
            assert isinstance(self.items, collections.abc.Iterable), repr(self.items)
            self.items = [abjad.NamedPitch(_) for _ in self.items]
            self.items = abjad.CyclicTuple(self.items)
        if self.intervals is not None:
            assert isinstance(self.items, collections.abc.Iterable), repr(self.items)
            self.intervals = abjad.CyclicTuple(self.intervals)

    def __getitem__(self, i) -> abjad.Pitch:
        """
        Gets pitch ``i`` cyclically with intervals.
        """
        if isinstance(i, slice):
            raise NotImplementedError
        iteration = i // len(self)
        if self.intervals is None:
            transposition = 0
        else:
            transposition = sum(self.intervals[:iteration])
        pitch_ = abjad.CyclicTuple(list(self))[i]
        pitch = type(pitch_)(pitch_.number + transposition)
        return pitch


@dataclasses.dataclass
class MicrotoneDeviationCommand(_scoping.Command):
    r"""
    Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches("E4"),
        ...     baca.make_even_divisions(),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        eqs'8
                        e'8
                        eqf'8
                        ]
                        e'8
                        [
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        ]
                    }
                >>
            }

    """

    deviations: typing.Any = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.deviations is not None:
            assert isinstance(self.deviations, collections.abc.Iterable)
            assert all(isinstance(_, numbers.Number) for _ in self.deviations)
        self.deviations = abjad.CyclicTuple(self.deviations)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.deviations:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(_selection.Selection(argument).plts()):
            deviation = self.deviations[i]
            self._adjust_pitch(plt, deviation)

    def _adjust_pitch(self, plt, deviation):
        assert deviation in (0.5, 0, -0.5)
        if deviation == 0:
            return
        for pleaf in plt:
            pitch = pleaf.written_pitch
            accidental = pitch.accidental.semitones + deviation
            pitch = abjad.NamedPitch(pitch, accidental=accidental)
            pleaf.written_pitch = pitch
            annotation = {"color microtone": True}
            abjad.attach(annotation, pleaf)


@dataclasses.dataclass
class OctaveDisplacementCommand(_scoping.Command):
    r"""
    Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.suite(
        ...         baca.pitch("G4"),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        g'8
                        [
                        g'8
                        g''8
                        g''8
                        ]
                        g'8
                        [
                        g'8
                        g8
                        ]
                        g8
                        [
                        g'''8
                        g'''8
                        g'8
                        ]
                        g'8
                        [
                        g''8
                        g''8
                        ]
                    }
                >>
            }

    """

    displacements: typing.Any = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.displacements is not None:
            self.displacements = tuple(self.displacements)
            assert self._is_octave_displacement_vector(self.displacements)
            self.displacements = abjad.CyclicTuple(self.displacements)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.displacements is None:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(_selection.Selection(argument).plts()):
            displacement = self.displacements[i]
            interval = abjad.NumberedInterval(12 * displacement)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitch += interval
                    pleaf.written_pitch = pitch
                elif isinstance(pleaf, abjad.Chord):
                    pitches = abjad.PitchSegment(
                        [_ + interval for _ in pleaf.written_pitches]
                    )
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, (tuple, list)):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False


def _parse_string(string):
    items, current_chord = [], []
    for part in string.split():
        if "<" in part:
            assert not current_chord
            current_chord.append(part)
        elif ">" in part:
            assert current_chord
            current_chord.append(part)
            item = " ".join(current_chord)
            items.append(item)
            current_chord = []
        elif current_chord:
            current_chord.append(part)
        else:
            items.append(part)
    assert not current_chord, repr(current_chord)
    return items


def _coerce_pitches(pitches):
    if isinstance(pitches, str):
        pitches = _parse_string(pitches)
    items = []
    for item in pitches:
        if isinstance(item, str) and "<" in item and ">" in item:
            item = item.strip("<")
            item = item.strip(">")
            item = abjad.PitchSet(item, abjad.NamedPitch)
        elif isinstance(item, str):
            item = abjad.NamedPitch(item)
        elif isinstance(item, collections.abc.Iterable):
            item = abjad.PitchSet(item, abjad.NamedPitch)
        else:
            item = abjad.NamedPitch(item)
        items.append(item)
    if isinstance(pitches, Loop):
        pitches = type(pitches)(items=items, intervals=pitches.intervals)
    else:
        pitches = abjad.CyclicTuple(items)
    return pitches


def _set_lt_pitch(
    lt,
    pitch,
    *,
    allow_repitch=False,
    mock=False,
    set_chord_pitches_equal=False,
):
    new_lt = None
    already_pitched = _const.ALREADY_PITCHED
    for leaf in lt:
        abjad.detach(_const.NOT_YET_PITCHED, leaf)
        if mock is True:
            abjad.attach(_const.MOCK, leaf)
        if allow_repitch:
            continue
        if abjad.get.has_indicator(leaf, already_pitched):
            voice = abjad.get.parentage(leaf).get(abjad.Voice)
            if voice is None:
                name = "no voice"
            else:
                name = voice.name
            raise Exception(f"already pitched {repr(leaf)} in {name}.")
        abjad.attach(already_pitched, leaf)
    if pitch is None:
        if not lt.is_pitched:
            pass
        else:
            for leaf in lt:
                rest = abjad.Rest(leaf.written_duration, multiplier=leaf.multiplier)
                abjad.mutate.replace(leaf, rest, wrappers=True)
            new_lt = abjad.get.logical_tie(rest)
    elif isinstance(pitch, collections.abc.Iterable):
        if isinstance(lt.head, abjad.Chord):
            for chord in lt:
                chord.written_pitches = pitch
        else:
            assert isinstance(lt.head, (abjad.Note, abjad.Rest))
            for leaf in lt:
                chord = abjad.Chord(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, chord, wrappers=True)
            new_lt = abjad.get.logical_tie(chord)
    else:
        if isinstance(lt.head, abjad.Note):
            for note in lt:
                note.written_pitch = pitch
        elif set_chord_pitches_equal is True and isinstance(lt.head, abjad.Chord):
            for chord in lt:
                for note_head in chord.note_heads:
                    note_head.written_pitch = pitch
        else:
            assert isinstance(lt.head, (abjad.Chord, abjad.Rest))
            for leaf in lt:
                note = abjad.Note(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, note, wrappers=True)
            new_lt = abjad.get.logical_tie(note)
    return new_lt


@dataclasses.dataclass
class PitchCommand(_scoping.Command):
    r"""
    Pitch command.

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        g''8
                        [
                        cs''8
                        ef''8
                        e''8
                        ]
                        f''8
                        [
                        b''8
                        g''8
                        ]
                        cs''8
                        [
                        ef''8
                        e''8
                        f''8
                        ]
                        b''8
                        [
                        g''8
                        cs''8
                        ]
                    }
                >>
            }

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("C4 F4 F#4 <B4 C#5> D5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        c'8
                        [
                        f'8
                        fs'8
                        <b' cs''>8
                        ]
                        d''8
                        [
                        c'8
                        f'8
                        ]
                        fs'8
                        [
                        <b' cs''>8
                        d''8
                        c'8
                        ]
                        f'8
                        [
                        fs'8
                        <b' cs''>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Large chord:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("<C4 D4 E4 F4 G4 A4 B4 C4>", allow_repeats=True)
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with Abjad container:

        >>> command = baca.PitchCommand(
        ...     cyclic=True,
        ...     pitches=[19, 13, 15, 16, 17, 23],
        ... )

        >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                g''8
                cs''8
                ef''8
                e''8
                f''8
                b''8
                g''8
                cs''8
            }


    """

    allow_octaves: bool = None
    allow_out_of_range: bool = None
    allow_repeats: bool = None
    allow_repitch: bool = None
    mock: bool = None
    cyclic: bool = None
    do_not_transpose: bool = None
    ignore_incomplete: bool = None
    persist: str = None
    pitches: typing.Union[typing.Sequence, Loop] = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.allow_octaves is not None:
            self.allow_octaves = bool(self.allow_octaves)
        if self.allow_out_of_range is not None:
            self.allow_out_of_range = bool(self.allow_out_of_range)
        if self.allow_repeats is not None:
            self.allow_repeats = bool(self.allow_repeats)
        if self.allow_repitch is not None:
            self.allow_repitch = bool(self.allow_repitch)
        if self.mock is not None:
            self.mock = bool(self.mock)
        if self.cyclic is not None:
            self.cyclic = bool(self.cyclic)
        if self.do_not_transpose is not None:
            self.do_not_transpose = bool(self.do_not_transpose)
        if self.ignore_incomplete is not None:
            self.ignore_incomplete = bool(self.ignore_incomplete)
        self._mutated_score = False
        if self.persist is not None:
            assert isinstance(self.persist, str), repr(self.persist)
        if self.pitches is not None:
            self.pitches = _coerce_pitches(self.pitches)
        self._state = {}

    __repr__ = _scoping.Command.__repr__

    def _call(self, argument=None):
        if argument is None:
            return
        if not self.pitches:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        plts = []
        for pleaf in _selection.Selection(argument).pleaves():
            plt = abjad.get.logical_tie(pleaf)
            if plt.head is pleaf:
                plts.append(plt)
        self._check_length(plts)
        pitches = self.pitches
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        previous_pitches_consumed = self._previous_pitches_consumed()
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        pitches_consumed = 0
        for i, plt in enumerate(plts):
            pitch = pitches[i + previous_pitches_consumed]
            new_plt = _set_lt_pitch(
                plt, pitch, allow_repitch=self.allow_repitch, mock=self.mock
            )
            if new_plt is not None:
                self._mutated_score = True
                plt = new_plt
            if self.allow_octaves:
                for pleaf in plt:
                    abjad.attach(_const.ALLOW_OCTAVE, pleaf)
            if self.allow_out_of_range:
                for pleaf in plt:
                    abjad.attach(_const.ALLOW_OUT_OF_RANGE, pleaf)
            if self.allow_repeats:
                for pleaf in plt:
                    abjad.attach(_const.ALLOW_REPEAT_PITCH, pleaf)
            if self.do_not_transpose is True:
                for pleaf in plt:
                    abjad.attach(_const.DO_NOT_TRANSPOSE, pleaf)
            pitches_consumed += 1
        self._state = {}
        pitches_consumed += previous_pitches_consumed
        self.state["pitches_consumed"] = pitches_consumed

    def _check_length(self, plts):
        if self.cyclic:
            return
        if len(self.pitches) < len(plts):
            message = f"only {len(self.pitches)} pitches"
            message += f" for {len(plts)} logical ties:\n\n"
            message += f"{self!r} and {plts!r}."
            raise Exception(message)

    def _mutates_score(self):
        pitches = self.pitches or []
        if any(isinstance(_, collections.abc.Iterable) for _ in pitches):
            return True
        return self._mutated_score

    def _previous_pitches_consumed(self):
        dictionary = self.runtime.get("previous_segment_voice_metadata", None)
        if not dictionary:
            return 0
        dictionary = dictionary.get(_const.PITCH, None)
        if not dictionary:
            return 0
        if dictionary.get("name") != self.persist:
            return 0
        pitches_consumed = dictionary.get("pitches_consumed", None)
        if not pitches_consumed:
            return 0
        assert 1 <= pitches_consumed
        if self.ignore_incomplete:
            return pitches_consumed
        dictionary = self.runtime["previous_segment_voice_metadata"]
        dictionary = dictionary.get(_const.RHYTHM, None)
        if dictionary:
            if dictionary.get("incomplete_final_note", False):
                pitches_consumed -= 1
        return pitches_consumed

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.PitchCommand().parameter
            'PITCH'

        """
        return _const.PITCH

    @property
    def state(self):
        """
        Gets state dictionary.
        """
        return self._state


@dataclasses.dataclass
class RegisterCommand(_scoping.Command):
    r"""
    Register command.

    ..  container:: example

        With music-commands:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [("[A0, C8]", 15)],
        ...         ),
        ...     ),
        ... )
        >>> selection = stack([[10, 12, 14], [10, 12, 14], [10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 9/16
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With segment-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches("G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4"),
        ...     baca.make_even_divisions(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([("[A0, C8]", 15)]),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([("[A0, C8]", -6)]),
        ...     ),
        ... )
        >>> selection = stack([{10, 12, 14}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <bf c' d'>16
                    }
                }
            >>

    """

    registration: typing.Any = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.registration is not None:
            prototype = _pitchclasses.Registration
            assert isinstance(self.registration, prototype), repr(self.registration)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.registration is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = _selection.Selection(argument).plts()
        assert isinstance(plts, _selection.Selection)
        for plt in plts:
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitches = self.registration([pitch])
                    pleaf.written_pitch = pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    pitches = pleaf.written_pitches
                    pitches = self.registration(pitches)
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(_const.NOT_YET_REGISTERED, pleaf)


@dataclasses.dataclass
class RegisterInterpolationCommand(_scoping.Command):
    r"""
    Register interpolation command.

    ..  container:: example

        With music-commands:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c''16
                        b'16
                        af'16
                        g''16
                        cs''16
                        d''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        f''16
                        a''16
                        bf''16
                        c'''16
                        b''16
                        af''16
                        g'''16
                        cs'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = [
        ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
        ... ]
        >>> collections = [set(_) for _ in collections]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/8
                        <e' fs'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <f' ef''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <a' bf'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' b''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g'' af''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <cs''' d'''>16
                    }
                }
            >>

    ..  container:: example

        Holds register constant:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, 12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf''8
                        c''8
                        ]
                        b''8
                        [
                        af''8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs''8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a''8
                        bf''8
                        ]
                        c''8
                        [
                        b''8
                        af''8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to 0:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, 0),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d'8
                        fs'8
                        ]
                        e'8
                        [
                        ef'8
                        f'8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 0 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(0, 12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        fs'8
                        [
                        e'8
                        ef'8
                        f'8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to -12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, -12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf8
                        ]
                        c'8
                        [
                        b8
                        af8
                        ]
                        g8
                        [
                        cs'8
                        d'8
                        fs8
                        ]
                        e8
                        [
                        ef8
                        f8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from -12 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(-12, 12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

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
                        fs8
                        [
                        e8
                        ef8
                        f8
                        ]
                        a8
                        [
                        bf8
                        c'8
                        ]
                        b8
                        [
                        af8
                        g'8
                        cs'8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Selects tuplet 0:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(baca.selectors.tuplet(0), lone=True),
        ...     baca.register(0, 24, selector=baca.selectors.tuplet(0)),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        \abjad-color-music #'green
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Selects tuplet -1:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(baca.selectors.tuplet(-1), lone=True),
        ...     baca.register(0, 24, selector=baca.selectors.tuplet(-1)),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        Maps to tuplets:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(baca.selectors.tuplets()),
        ...     baca.new(
        ...         baca.register(0, 24),
        ...         map=baca.selectors.tuplets(),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        \abjad-color-music #'red
                        fs'16
                        [
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        ef''16
                        \abjad-color-music #'red
                        f''16
                        \abjad-color-music #'red
                        a'16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        c''16
                        \abjad-color-music #'red
                        b''16
                        \abjad-color-music #'red
                        af''16
                        \abjad-color-music #'red
                        g''16
                        \abjad-color-music #'red
                        cs'''16
                        \abjad-color-music #'red
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        fs'16
                        [
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'blue
                        f''16
                        \abjad-color-music #'blue
                        a'16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'blue
                        c''16
                        \abjad-color-music #'blue
                        b''16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'blue
                        g''16
                        \abjad-color-music #'blue
                        cs'''16
                        \abjad-color-music #'blue
                        d'''16
                        ]
                    }
                }
            >>

    """

    start_pitch: typing.Union[abjad.Number, abjad.NumberedPitch] = 0
    stop_pitch: typing.Union[abjad.Number, abjad.NumberedPitch] = 0

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        self.start_pitch = abjad.NumberedPitch(self.start_pitch)
        self.stop_pitch = abjad.NumberedPitch(self.stop_pitch)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = _selection.Selection(argument).plts()
        length = len(plts)
        for i, plt in enumerate(plts):
            registration = self._get_registration(i, length)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    written_pitches = registration([pleaf.written_pitch])
                    pleaf.written_pitch = written_pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    written_pitches = registration(pleaf.written_pitches)
                    pleaf.written_pitches = written_pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(_const.NOT_YET_REGISTERED, pleaf)

    def _get_registration(self, i, length):
        start_pitch = self.start_pitch.number
        stop_pitch = self.stop_pitch.number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(i, length)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        return _pitchclasses.Registration([("[A0, C8]", current_pitch)])


@dataclasses.dataclass
class RegisterToOctaveCommand(_scoping.Command):
    r"""
    Register-to-octave command.

    ..  container:: example

        Chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c' d'' e'''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c d' e''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c, d e'>16
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c'16
                        [
                        d''16
                        e'''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c16
                        [
                        d'16
                        e''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c,16
                        [
                        d16
                        e'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf'16
                        [
                        c''16
                        d''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        >>> baca.RegisterToOctaveCommand()
        RegisterToOctaveCommand()

    ..  container:: example

        Bass anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.Down,
        ...     octave_number=5,
        ... )
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    ..  container:: example

        Center anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.Center,
        ...     octave_number=5,
        ... )
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        Soprano anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.Up,
        ...     octave_number=5,
        ... )
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> staff = abjad.Staff([chord])
        >>> abjad.attach(abjad.Clef("bass"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            \clef "bass"
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=1)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c,, d, e>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=2)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=3)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=4)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=5)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    """

    anchor: typing.Any = None
    octave_number: typing.Any = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.anchor is not None:
            prototype = (abjad.Center, abjad.Down, abjad.Up)
            assert self.anchor in prototype, repr(self.anchor)
        if self.octave_number is not None:
            assert isinstance(self.octave_number, int), repr(self.octave_number)

    __repr__ = _scoping.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.octave_number is None:
            return
        if self.selector:
            argument = self.selector(argument)
        target_octave_number = self.octave_number or 4
        current_octave_number = self._get_anchor_octave_number(argument)
        octave_adjustment = target_octave_number - current_octave_number
        pleaves = _selection.pleaves(argument)
        for pleaf in pleaves:
            self._set_pitch(pleaf, lambda _: _.transpose(n=12 * octave_adjustment))

    def _get_anchor_octave_number(self, argument):
        pitches = []
        for leaf in abjad.iterate.leaves(argument, pitched=True):
            if isinstance(leaf, abjad.Note):
                pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                pitches.extend(leaf.written_pitches)
            else:
                raise TypeError(leaf)
        pitches = list(set(pitches))
        pitches.sort()
        anchor = self.anchor or abjad.Down
        if anchor == abjad.Down:
            pitch = pitches[0]
        elif anchor == abjad.Up:
            pitch = pitches[-1]
        elif anchor == abjad.Center:
            soprano = max(pitches)
            bass = min(pitches)
            centroid = (soprano.number + bass.number) / 2.0
            pitch = abjad.NumberedPitch(centroid)
        else:
            raise ValueError(anchor)
        return pitch.octave.number

    def _set_pitch(self, leaf, transposition):
        if isinstance(leaf, abjad.Note):
            pitch = transposition(leaf.written_pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            pitches = [transposition(_) for _ in leaf.written_pitches]
            leaf.written_pitches = pitches
        abjad.detach(_const.NOT_YET_REGISTERED, leaf)


@dataclasses.dataclass
class StaffPositionCommand(_scoping.Command):
    r"""
    Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("treble"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                b'4
                d''4
                b'4
                d''4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("percussion"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    """

    numbers: typing.Any = ()
    allow_out_of_range: bool = None
    allow_repeats: bool = None
    allow_repitch: bool = None
    exact: bool = None
    mock: bool = None
    selector: typing.Any = _selectors.plts()
    set_chord_pitches_equal: bool = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        prototype = (int, list, abjad.StaffPosition)
        assert all(isinstance(_, prototype) for _ in self.numbers), repr(self.numbers)
        self.numbers = abjad.CyclicTuple(self.numbers)
        if self.allow_out_of_range is not None:
            self.allow_out_of_range = bool(self.allow_out_of_range)
        if self.allow_repeats is not None:
            self.allow_repeats = bool(self.allow_repeats)
        if self.allow_repitch is not None:
            self.allow_repitch = bool(self.allow_repitch)
        if self.mock is not None:
            self.mock = bool(self.mock)
        if self.exact is not None:
            self.exact = bool(self.exact)
        self._mutated_score = False
        if self.set_chord_pitches_equal is not None:
            self.set_chord_pitches_equal = bool(self.set_chord_pitches_equal)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        plt_count = 0
        for i, plt in enumerate(_selection.Selection(argument).plts()):
            clef = abjad.get.effective(
                plt.head,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            number = self.numbers[i]
            if isinstance(number, list):
                positions = [abjad.StaffPosition(_) for _ in number]
                pitches = [_.to_pitch(clef) for _ in positions]
                new_lt = _set_lt_pitch(
                    plt,
                    pitches,
                    allow_repitch=self.allow_repitch,
                    mock=self.mock,
                    set_chord_pitches_equal=self.set_chord_pitches_equal,
                )
                if new_lt is not None:
                    self._mutated_score = True
                    plt = new_lt
            else:
                position = abjad.StaffPosition(number)
                pitch = position.to_pitch(clef)
                new_lt = _set_lt_pitch(
                    plt,
                    pitch,
                    allow_repitch=self.allow_repitch,
                    mock=self.mock,
                    set_chord_pitches_equal=self.set_chord_pitches_equal,
                )
                if new_lt is not None:
                    self._mutated_score = True
                    plt = new_lt
            plt_count += 1
            for pleaf in plt:
                abjad.attach(_const.STAFF_POSITION, pleaf)
                if self.allow_out_of_range:
                    abjad.attach(_const.ALLOW_OUT_OF_RANGE, pleaf)
                if self.allow_repeats:
                    abjad.attach(_const.ALLOW_REPEAT_PITCH, pleaf)
                    abjad.attach(_const.DO_NOT_TRANSPOSE, pleaf)
        if self.exact and plt_count != len(self.numbers):
            message = f"PLT count ({plt_count}) does not match"
            message += f" staff position count ({len(self.numbers)})."
            raise Exception(message)

    def _mutates_score(self):
        numbers = self.numbers or []
        if any(isinstance(_, collections.abc.Iterable) for _ in numbers):
            return True
        return self._mutated_score


@dataclasses.dataclass
class StaffPositionInterpolationCommand(_scoping.Command):
    """
    Staff position interpolation command.
    """

    start: typing.Union[int, str, abjad.NamedPitch, abjad.StaffPosition] = None
    stop: typing.Union[int, str, abjad.NamedPitch, abjad.StaffPosition] = None
    mock: bool = None
    pitches_instead_of_staff_positions: bool = None
    selector: typing.Any = _selectors.plts()

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        prototype = (abjad.NamedPitch, abjad.StaffPosition)
        if isinstance(self.start, str):
            self.start = abjad.NamedPitch(self.start)
        elif isinstance(self.start, int):
            self.start = abjad.StaffPosition(self.start)
        assert isinstance(self.start, prototype), repr(self.start)
        if isinstance(self.stop, str):
            self.stop = abjad.NamedPitch(self.stop)
        elif isinstance(self.stop, int):
            self.stop = abjad.StaffPosition(self.stop)
        assert isinstance(self.stop, prototype), repr(self.stop)
        if self.mock is not None:
            self.mock = bool(self.mock)
        if self.pitches_instead_of_staff_positions is not None:
            self.pitches_instead_of_staff_positions = bool(
                self.pitches_instead_of_staff_positions
            )

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = _selection.Selection(argument).plts()
        if not plts:
            return
        count = len(plts)
        if isinstance(self.start, abjad.StaffPosition):
            start_staff_position = self.start
        else:
            start_phead = plts[0].head
            clef = abjad.get.effective(start_phead, abjad.Clef)
            start_staff_position = abjad.StaffPosition.from_pitch_and_clef(
                self.start,
                clef,
            )
        if isinstance(self.stop, abjad.StaffPosition):
            stop_staff_position = self.stop
        else:
            stop_phead = plts[-1].head
            clef = abjad.get.effective(
                stop_phead,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            stop_staff_position = abjad.StaffPosition.from_pitch_and_clef(
                self.stop,
                clef,
            )
        unit_distance = abjad.Fraction(
            stop_staff_position.number - start_staff_position.number, count - 1
        )
        for i, plt in enumerate(plts):
            staff_position = unit_distance * i + start_staff_position.number
            staff_position = round(staff_position)
            staff_position = abjad.StaffPosition(staff_position)
            clef = abjad.get.effective(
                plt.head,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            pitch = staff_position.to_pitch(clef)
            new_lt = _set_lt_pitch(plt, pitch, allow_repitch=True, mock=self.mock)
            assert new_lt is None, repr(new_lt)
            for leaf in plt:
                abjad.attach(_const.ALLOW_REPEAT_PITCH, leaf)
                if not self.pitches_instead_of_staff_positions:
                    abjad.attach(_const.STAFF_POSITION, leaf)
        if isinstance(self.start, abjad.NamedPitch):
            start_pitch = self.start
        else:
            clef = abjad.get.effective(
                plts[0],
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            start_pitch = self.start.to_pitch(clef)
        new_lt = _set_lt_pitch(plts[0], start_pitch, allow_repitch=True, mock=self.mock)
        assert new_lt is None, repr(new_lt)
        if isinstance(self.stop, abjad.NamedPitch):
            stop_pitch = self.stop
        else:
            clef = abjad.get.effective(
                plts[0],
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            stop_pitch = self.stop.to_pitch(clef=clef)
        new_lt = _set_lt_pitch(plts[-1], stop_pitch, allow_repitch=True, mock=self.mock)
        assert new_lt is None, repr(new_lt)


def bass_to_octave(
    n: int,
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the lowest note in the entire selection appears
        in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.bass_to_octave(3),
        ...     baca.color(baca.selectors.plts(), lone=True),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        \abjad-color-music #'green
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'green
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f'8
                        ~
                        [
                        \abjad-color-music #'green
                        f'32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef' e' fs''>8
                        ~
                        [
                        \abjad-color-music #'green
                        <ef' e' fs''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g af'>8
                        ~
                        [
                        \abjad-color-music #'green
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a8
                        ~
                        [
                        \abjad-color-music #'green
                        a32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the lowest pitch in each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.bass_to_octave(3),
        ...         map=baca.selectors.plts(),
        ...     ),
        ...     baca.color(baca.selectors.plts()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        \abjad-color-music #'red
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        ~
                        [
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        ~
                        [
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g af'>8
                        ~
                        [
                        \abjad-color-music #'blue
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        ~
                        [
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.Down, octave_number=n, selector=selector
    )


def center_to_octave(
    n: int,
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the centroid of all PLTs appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.center_to_octave(3),
        ...     baca.color(baca.selectors.plts(), lone=True),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        \abjad-color-music #'green
                        <c, d, bf,>8
                        ~
                        [
                        \abjad-color-music #'green
                        <c, d, bf,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f8
                        ~
                        [
                        \abjad-color-music #'green
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef e fs'>8
                        ~
                        [
                        \abjad-color-music #'green
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g, af>8
                        ~
                        [
                        \abjad-color-music #'green
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,8
                        ~
                        [
                        \abjad-color-music #'green
                        a,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the centroid of each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.center_to_octave(3),
        ...         map=baca.selectors.plts(),
        ...     ),
        ...     baca.color(baca.selectors.plts()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        \abjad-color-music #'red
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        ~
                        [
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        ~
                        [
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        ~
                        [
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        ~
                        [
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.Center, octave_number=n, selector=selector
    )


def clusters(
    widths: typing.List[int],
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
) -> ClusterCommand:
    """
    Makes clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(selector=selector, start_pitch=start_pitch, widths=widths)


def color_fingerings(
    numbers: typing.List[abjad.Number],
    *tweaks: abjad.IndexedTweakManager,
    selector=_selectors.pheads(exclude=_const.HIDDEN),
) -> ColorFingeringCommand:
    """
    Adds color fingerings.
    """
    return ColorFingeringCommand(numbers=numbers, selector=selector, tweaks=tweaks)


def deviation(
    deviations: typing.List[abjad.Number],
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> MicrotoneDeviationCommand:
    """
    Sets microtone ``deviations``.
    """
    return MicrotoneDeviationCommand(deviations=deviations, selector=selector)


def diatonic_clusters(
    widths: typing.List[int],
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> DiatonicClusterCommand:
    """
    Makes diatonic clusters with ``widths``.
    """
    return DiatonicClusterCommand(selector=selector, widths=widths)


def displacement(
    displacements: typing.List[int],
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> OctaveDisplacementCommand:
    r"""
    Octave-displaces ``selector`` output.

    ..  container:: example

        Octave-displaces PLTs:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack(3 * [[0, 2, 3]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 27/16
                        r8
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        c16
                        [
                        d''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/12
                    {
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Octave-displaces chords:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [4],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ... )
        >>> selection = stack(6 * [{0, 2, 3}])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 15/8
                        r8
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                        r4
                    }
                }
            >>

    """
    return OctaveDisplacementCommand(displacements=displacements, selector=selector)


def force_accidental(
    selector=_selectors.pleaf(0, exclude=_const.HIDDEN),
) -> AccidentalAdjustmentCommand:
    r"""
    Forces accidental.

    ..  container:: example

        Inverts edition-specific tags:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.not_parts(
        ...         baca.force_accidental(
        ...             selector=baca.selectors.pleaves((None, 2)),
        ...         ),
        ...     ),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
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
                        e'2
                        %@% e'!2
                        f'4.
                        %@% f'!4.
                        e'2
                        f'4.
                    }
                >>
            }

    """
    return AccidentalAdjustmentCommand(forced=True, selector=selector)


def interpolate_pitches(
    start: typing.Union[int, str, abjad.NamedPitch],
    stop: typing.Union[int, str, abjad.NamedPitch],
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    mock: bool = None,
) -> StaffPositionInterpolationCommand:
    r"""
    Interpolates from staff position of ``start`` pitch to staff position of ``stop``
    pitch.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble"),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        \clef "treble"
                        ef'16
                        [
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        fs''16
                        ]
                    }
                }
            >>

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble"),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ...     baca.glissando(
        ...         allow_repeats=True,
        ...         hide_middle_note_heads=True,
        ...     ),
        ...     baca.glissando_thickness(3),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \override Glissando.thickness = 3
                        \time 3/2
                        \clef "treble"
                        ef'16
                        [
                        \glissando
                        \hide NoteHead
                        \override Accidental.stencil = ##f
                        \override NoteColumn.glissando-skip = ##t
                        \override NoteHead.no-ledgers = ##t
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        \revert Accidental.stencil
                        \revert NoteColumn.glissando-skip
                        \revert NoteHead.no-ledgers
                        \undo \hide NoteHead
                        fs''16
                        ]
                        \revert Glissando.thickness
                    }
                }
            >>

    """
    start_ = abjad.NamedPitch(start)
    stop_ = abjad.NamedPitch(stop)
    return StaffPositionInterpolationCommand(
        start=start_,
        stop=stop_,
        mock=mock,
        pitches_instead_of_staff_positions=True,
        selector=selector,
    )


def interpolate_staff_positions(
    start: typing.Union[int, abjad.StaffPosition],
    stop: typing.Union[int, abjad.StaffPosition],
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    mock: bool = None,
) -> StaffPositionInterpolationCommand:
    r"""
    Interpolates from ``start`` staff position to ``stop`` staff position.
    """
    start_ = abjad.StaffPosition(start)
    stop_ = abjad.StaffPosition(stop)
    return StaffPositionInterpolationCommand(
        start=start_, stop=stop_, mock=mock, selector=selector
    )


def levine_multiphonic(n: int) -> abjad.Markup:
    """
    Makes Levine multiphonic markup.
    """
    assert isinstance(n, int), repr(n)
    return abjad.Markup(rf'\baca-boxed-markup "L.{n}"')


def loop(
    items: typing.Sequence,
    intervals: typing.Sequence,
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> PitchCommand:
    """
    Loops ``items`` at ``intervals``.
    """
    loop = Loop(items=items, intervals=intervals)
    return pitches(loop, selector=selector)


def natural_clusters(
    widths: typing.Sequence[int],
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
) -> ClusterCommand:
    """
    Makes natural clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(
        hide_flat_markup=True,
        selector=selector,
        start_pitch=start_pitch,
        widths=widths,
    )


def pitch(
    pitch,
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    allow_out_of_range: bool = None,
    allow_repitch: bool = None,
    mock: bool = None,
    do_not_transpose: bool = None,
    persist: str = None,
) -> PitchCommand:
    r"""
    Makes pitch command.

    ..  container:: example

        REGRESSION. Preserves duration multipliers when leaves cast from one type to
        another (note to chord in this example):

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.rhythm(
        ...         rmakers.note(),
        ...         rmakers.written_duration(1),
        ...     ),
        ...     baca.pitch("<C4 D4 E4>"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
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
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    """
    if isinstance(pitch, (list, tuple)) and len(pitch) == 1:
        raise Exception(f"one-note chord {pitch!r}?")
    if allow_out_of_range not in (None, True, False):
        raise Exception(
            f"allow_out_of_range must be boolean (not {allow_out_of_range!r})."
        )
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        cyclic=True,
        do_not_transpose=do_not_transpose,
        mock=mock,
        persist=persist,
        pitches=[pitch],
        selector=selector,
    )


def pitches(
    pitches,
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    allow_octaves: bool = None,
    allow_repeats: bool = None,
    allow_repitch: bool = None,
    mock: bool = None,
    do_not_transpose: bool = None,
    exact: bool = None,
    ignore_incomplete: bool = None,
    persist: str = None,
) -> PitchCommand:
    """
    Makes pitch command.
    """
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception(
            f"ignore_incomplete must be boolean (not {ignore_incomplete!r})."
        )
    if ignore_incomplete is True and not persist:
        raise Exception("ignore_incomplete is ignored when persist is not set.")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        allow_repitch=allow_repitch,
        cyclic=cyclic,
        do_not_transpose=do_not_transpose,
        ignore_incomplete=ignore_incomplete,
        mock=mock,
        persist=persist,
        pitches=pitches,
        selector=selector,
    )


def register(
    start: int,
    stop: int = None,
    *,
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> typing.Union[RegisterCommand, RegisterInterpolationCommand]:
    r"""
    Octave-transposes ``selector`` output.

    ..  container:: example

        Octave-transposes all PLTs to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf4
                        ~
                        bf16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs16
                        [
                        e'16
                        ]
                        ef'4
                        ~
                        ef'16
                        r16
                        af16
                        [
                        g16
                        ]
                    }
                    \times 4/5
                    {
                        a16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(baca.selectors.tuplet(1), lone=True),
        ...     baca.register(-6, selector=baca.selectors.tuplet(1)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af16
                        [
                        \abjad-color-music #'green
                        g16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Octave-transposes all PLTs to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6, 18),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs'16
                        [
                        e'16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a''16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(baca.selectors.tuplet(1), lone=True),
        ...     baca.register(-6, 18, selector=baca.selectors.tuplet(1)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af'16
                        [
                        \abjad-color-music #'green
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    if stop is None:
        return RegisterCommand(
            registration=_pitchclasses.Registration([("[A0, C8]", start)]),
            selector=selector,
        )
    return RegisterInterpolationCommand(
        selector=selector, start_pitch=start, stop_pitch=stop
    )


def soprano_to_octave(
    n: int,
    selector=_selectors.plts(exclude=_const.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the highest note in the collection of all PLTs
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.color(baca.selectors.plts(), lone=True),
        ...     baca.soprano_to_octave(3),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        \abjad-color-music #'green
                        <c,, d,, bf,,>8
                        ~
                        [
                        \abjad-color-music #'green
                        <c,, d,, bf,,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f,8
                        ~
                        [
                        \abjad-color-music #'green
                        f,32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef, e, fs>8
                        ~
                        [
                        \abjad-color-music #'green
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g,, af,>8
                        ~
                        [
                        \abjad-color-music #'green
                        <g,, af,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,,8
                        ~
                        [
                        \abjad-color-music #'green
                        a,,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music that such that the highest note in each pitched logical
        tie appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.soprano_to_octave(3),
        ...         map=baca.selectors.plts(),
        ...     ),
        ...     baca.color(baca.selectors.plts()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        \abjad-color-music #'red
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        ~
                        [
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef, e, fs>8
                        ~
                        [
                        \abjad-color-music #'red
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        ~
                        [
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        ~
                        [
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(anchor=abjad.Up, octave_number=n, selector=selector)


def staff_position(
    argument: typing.Union[int, list, abjad.StaffPosition],
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    allow_out_of_range: bool = None,
    allow_repitch: bool = None,
    mock: bool = None,
    set_chord_pitches_equal: bool = None,
) -> StaffPositionCommand:
    """
    Makes staff position command; allows repeats.
    """
    assert isinstance(argument, (int, list, abjad.StaffPosition)), repr(argument)
    if isinstance(argument, list):
        assert all(isinstance(_, (int, abjad.StaffPosition)) for _ in argument)
    return StaffPositionCommand(
        numbers=[argument],
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        mock=mock,
        selector=selector,
        set_chord_pitches_equal=set_chord_pitches_equal,
    )


def staff_positions(
    numbers,
    selector=_selectors.plts(exclude=_const.HIDDEN),
    *,
    allow_out_of_range: bool = None,
    allow_repeats: bool = None,
    mock: bool = None,
    exact: bool = None,
) -> StaffPositionCommand:
    """
    Makes staff position command; does not allow repeats.
    """
    if allow_repeats is None and len(numbers) == 1:
        allow_repeats = True
    return StaffPositionCommand(
        numbers=numbers,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=allow_repeats,
        exact=exact,
        mock=mock,
        selector=selector,
    )

# -*- coding: utf-8 -*-
import abjad
import baca
from baca.tools.Tree import Tree


class PitchTree(Tree):
    r'''Pitch tree.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes numbered pitch tree:

        ::

            >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> show(tree) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            } <<
                \new Staff {
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                    } {
                        \time 1/8
                        e''8 \startGroup ^ \markup { 0 }
                        fs''8
                        bf'8 \stopGroup
                        s8
                        a'8 \startGroup ^ \markup { 1 }
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8 \stopGroup
                        s8
                        c'8 \startGroup ^ \markup { 2 }
                        d'8
                        ef'8
                        f'8 \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes named pitch tree:

        ::

            >>> items = [
            ...     ['E5', 'F#5', 'Bb4'],
            ...     ['A4', 'G4', 'Ab4', 'B4', 'A4', 'C#4'],
            ...     ['C4', 'D4', 'Eb4', 'F4'],
            ...     ]
            >>> tree = baca.PitchTree(
            ...     items=items,
            ...     item_class=abjad.NamedPitch,
            ...     )
            >>> show(tree) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            } <<
                \new Staff {
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                    } {
                        \time 1/8
                        e''8 \startGroup ^ \markup { 0 }
                        fs''8
                        bf'8 \stopGroup
                        s8
                        a'8 \startGroup ^ \markup { 1 }
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8 \stopGroup
                        s8
                        c'8 \startGroup ^ \markup { 2 }
                        d'8
                        ef'8
                        f'8 \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes numbered pitch-class tree:

        ::

            >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(
            ...     items=items,
            ...     item_class=abjad.NumberedPitchClass,
            ...     )
            >>> show(tree) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            } <<
                \new Staff {
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                    } {
                        \time 1/8
                        e'8 \startGroup ^ \markup { 0 }
                        fs'8
                        bf'8 \stopGroup
                        s8
                        a'8 \startGroup ^ \markup { 1 }
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8 \stopGroup
                        s8
                        c'8 \startGroup ^ \markup { 2 }
                        d'8
                        ef'8
                        f'8 \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes named pitch-class tree:

        ::

            >>> items = [
            ...     ['E5', 'F#5', 'Bb4'],
            ...     ['A4', 'G4', 'Ab4', 'B4', 'A4', 'C#4'],
            ...     ['C4', 'D4', 'Eb4', 'F4'],
            ...     ]
            >>> tree = baca.PitchTree(
            ...     items=items,
            ...     item_class=abjad.NamedPitchClass,
            ...     )
            >>> show(tree) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            } <<
                \new Staff {
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                    } {
                        \time 1/8
                        e'8 \startGroup ^ \markup { 0 }
                        fs'8
                        bf'8 \stopGroup
                        s8
                        a'8 \startGroup ^ \markup { 1 }
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8 \stopGroup
                        s8
                        c'8 \startGroup ^ \markup { 2 }
                        d'8
                        ef'8
                        f'8 \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes from other trees:

        ::

            >>> items = [
            ...     baca.PitchTree([4, 6, 10]),
            ...     baca.PitchTree([9, 7, 8, 11, 9, 1]),
            ...     baca.PitchTree([0, 2, 3, 5]),
            ...     ]
            >>> tree = baca.PitchTree(items=items)
            >>> lilypond_file = tree.__illustrate__(
            ...     cell_indices=False,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            } <<
                \new Staff {
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                    } {
                        \time 1/8
                        e'8 \startGroup
                        fs'8
                        bf'8 \stopGroup
                        s8
                        a'8 \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8 \stopGroup
                        s8
                        c'8 \startGroup
                        d'8
                        ef'8
                        f'8 \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes from pitch segments:

        ::

            >>> items = [
            ...     abjad.PitchClassSegment([4, 6, 10]),
            ...     abjad.PitchClassSegment([9, 7, 8, 11, 9, 1]),
            ...     abjad.PitchClassSegment([0, 2, 3, 5]),
            ...     ]
            >>> items = [segment.rotate(n=1) for segment in items]
            >>> tree = baca.PitchTree(items=items)
            >>> show(tree, cell_indices=False) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__(cell_indices=False)
            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            } <<
                \new Staff {
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                    } {
                        \time 1/8
                        bf'8 \startGroup
                        e'8
                        fs'8 \stopGroup
                        s8
                        cs'8 \startGroup
                        a'8
                        g'8
                        af'8
                        b'8
                        a'8 \stopGroup
                        s8
                        f'8 \startGroup
                        c'8
                        d'8
                        ef'8 \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes nested tree:

        ::

            >>> segment_1 = abjad.PitchClassSegment([4, 6, 10])
            >>> segment_2 = abjad.PitchClassSegment([9, 7, 8, 11, 9, 1])
            >>> segment_3 = abjad.PitchClassSegment([0, 2, 3, 5])
            >>> segment_1 = segment_1.transpose(n=1)
            >>> segment_2 = segment_2.transpose(n=1)
            >>> segment_3 = segment_3.transpose(n=1)
            >>> items = [[segment_1, segment_2], segment_3]
            >>> tree = baca.PitchTree(items=items)
            >>> graph(tree) # doctest: +SKIP

        ..  docs::

            >>> graph_ = tree.__graph__()
            >>> f(graph_)
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="",
                    shape=circle];
                node_1 [label="",
                    shape=circle];
                node_2 [label="",
                    shape=circle];
                node_3 [label="5",
                    shape=box];
                node_4 [label="7",
                    shape=box];
                node_5 [label="11",
                    shape=box];
                node_6 [label="",
                    shape=circle];
                node_7 [label="10",
                    shape=box];
                node_8 [label="8",
                    shape=box];
                node_9 [label="9",
                    shape=box];
                node_10 [label="0",
                    shape=box];
                node_11 [label="10",
                    shape=box];
                node_12 [label="2",
                    shape=box];
                node_13 [label="",
                    shape=circle];
                node_14 [label="1",
                    shape=box];
                node_15 [label="3",
                    shape=box];
                node_16 [label="4",
                    shape=box];
                node_17 [label="6",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_13;
                node_1 -> node_2;
                node_1 -> node_6;
                node_2 -> node_3;
                node_2 -> node_4;
                node_2 -> node_5;
                node_6 -> node_7;
                node_6 -> node_8;
                node_6 -> node_9;
                node_6 -> node_10;
                node_6 -> node_11;
                node_6 -> node_12;
                node_13 -> node_14;
                node_13 -> node_15;
                node_13 -> node_16;
                node_13 -> node_17;
            }

        ::

            >>> show(tree, cell_indices=False) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__(cell_indices=False)
            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            } <<
                \new Staff {
                    \new Voice \with {
                        \consists Horizontal_bracket_engraver
                    } {
                        \time 1/8
                        f'8 \startGroup \startGroup
                        g'8
                        b'8 \stopGroup
                        s8
                        bf'8 \startGroup
                        af'8
                        a'8
                        c'8
                        bf'8
                        d'8 \stopGroup \stopGroup
                        s8
                        cs'8 \startGroup
                        ef'8
                        e'8
                        fs'8 \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    '''
    
    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        item_class = item_class or abjad.NumberedPitch
        Tree.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __graph__(self, **keywords):
        r'''Graphs pitch tree.

        ..  container:: example

            Graphs numbered pitch tree:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)

            ::

                >>> graph(tree) # doctest: +SKIP

            ..  docs::

                >>> tree_graph = tree.__graph__()
                >>> f(tree_graph)
                digraph G {
                    graph [bgcolor=transparent,
                        truecolor=true];
                    node_0 [label="",
                        shape=circle];
                    node_1 [label="",
                        shape=circle];
                    node_2 [label="4",
                        shape=box];
                    node_3 [label="6",
                        shape=box];
                    node_4 [label="10",
                        shape=box];
                    node_5 [label="",
                        shape=circle];
                    node_6 [label="9",
                        shape=box];
                    node_7 [label="7",
                        shape=box];
                    node_8 [label="8",
                        shape=box];
                    node_9 [label="11",
                        shape=box];
                    node_10 [label="9",
                        shape=box];
                    node_11 [label="1",
                        shape=box];
                    node_12 [label="",
                        shape=circle];
                    node_13 [label="0",
                        shape=box];
                    node_14 [label="2",
                        shape=box];
                    node_15 [label="3",
                        shape=box];
                    node_16 [label="5",
                        shape=box];
                    node_0 -> node_1;
                    node_0 -> node_5;
                    node_0 -> node_12;
                    node_1 -> node_2;
                    node_1 -> node_3;
                    node_1 -> node_4;
                    node_5 -> node_6;
                    node_5 -> node_7;
                    node_5 -> node_8;
                    node_5 -> node_9;
                    node_5 -> node_10;
                    node_5 -> node_11;
                    node_12 -> node_13;
                    node_12 -> node_14;
                    node_12 -> node_15;
                    node_12 -> node_16;
                }

        ..  container:: example

            Graphs named pitch tree:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(
                ...     items=items,
                ...     item_class=abjad.NamedPitch,
                ...     )

            ::

                >>> graph(tree) # doctest: +SKIP

            ..  docs::

                >>> tree_graph = tree.__graph__()
                >>> f(tree_graph)
                digraph G {
                    graph [bgcolor=transparent,
                        truecolor=true];
                    node_0 [label="",
                        shape=circle];
                    node_1 [label="",
                        shape=circle];
                    node_2 [label="e'",
                        shape=box];
                    node_3 [label="fs'",
                        shape=box];
                    node_4 [label="bf'",
                        shape=box];
                    node_5 [label="",
                        shape=circle];
                    node_6 [label="a'",
                        shape=box];
                    node_7 [label="g'",
                        shape=box];
                    node_8 [label="af'",
                        shape=box];
                    node_9 [label="b'",
                        shape=box];
                    node_10 [label="a'",
                        shape=box];
                    node_11 [label="cs'",
                        shape=box];
                    node_12 [label="",
                        shape=circle];
                    node_13 [label="c'",
                        shape=box];
                    node_14 [label="d'",
                        shape=box];
                    node_15 [label="ef'",
                        shape=box];
                    node_16 [label="f'",
                        shape=box];
                    node_0 -> node_1;
                    node_0 -> node_5;
                    node_0 -> node_12;
                    node_1 -> node_2;
                    node_1 -> node_3;
                    node_1 -> node_4;
                    node_5 -> node_6;
                    node_5 -> node_7;
                    node_5 -> node_8;
                    node_5 -> node_9;
                    node_5 -> node_10;
                    node_5 -> node_11;
                    node_12 -> node_13;
                    node_12 -> node_14;
                    node_12 -> node_15;
                    node_12 -> node_16;
                }
     
        Returns Graphviz graph.
        '''
        superclass = super(PitchTree, self)
        return superclass.__graph__(**keywords)
        
    def __illustrate__(
        self,
        after_cell_spacing=True,
        brackets=True,
        cell_indices=True,
        color_repeats=True,
        global_staff_size=16,
        markup_direction=Up,
        set_classes=False,
        **keywords
        ):
        r'''Illustrates pitch tree.

        ..  container:: example

            Illustrate tree:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)
                >>> lilypond_file = tree.__illustrate__()
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e'8 \startGroup ^ \markup { 0 }
                            fs'8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Illustrates tree with set-classes:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)
                >>> lilypond_file = tree.__illustrate__(
                ...     cell_indices=Down,
                ...     set_classes=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e'8 \startGroup
                                ^ \markup {
                                    \small
                                        \line
                                            {
                                                "SC(3-8){0, 2, 5}"
                                            }
                                    }
                                - \tweak staff-padding #7
                                _ \markup { 0 }
                            fs'8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup
                                ^ \markup {
                                    \small
                                        \line
                                            {
                                                "SC(5-6){0, 1, 2, 4, 6}"
                                            }
                                    }
                                - \tweak staff-padding #7
                                _ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup
                                ^ \markup {
                                    \small
                                        \line
                                            {
                                                "SC(4-18){0, 2, 3, 4}"
                                            }
                                    }
                                - \tweak staff-padding #7
                                _ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Illustrates nested tree:

            ::

                >>> segment_1 = abjad.PitchClassSegment([4, 6, 10])
                >>> segment_2 = abjad.PitchClassSegment([9, 7, 8, 11, 9, 1])
                >>> segment_3 = abjad.PitchClassSegment([0, 2, 3, 5])
                >>> segment_1 = segment_1.transpose(n=1)
                >>> segment_2 = segment_2.transpose(n=1)
                >>> segment_3 = segment_3.transpose(n=1)
                >>> items = [[segment_1, segment_2], segment_3]
                >>> tree = baca.PitchTree(items=items)
                >>> lilypond_file = tree.__illustrate__(
                ...     cell_indices=Down,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            f'8 \startGroup \startGroup
                                - \tweak staff-padding #7
                                _ \markup { 0 }
                            g'8
                            b'8 \stopGroup
                            s8
                            bf'8 \startGroup
                                - \tweak staff-padding #7
                                _ \markup { 1 }
                            af'8
                            a'8
                            c'8
                            bf'8
                            d'8 \stopGroup \stopGroup
                            s8
                            cs'8 \startGroup
                                - \tweak staff-padding #7
                                _ \markup { 2 }
                            ef'8
                            e'8
                            fs'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        Returns LilyPond file.
        '''
        assert cell_indices in (True, False, Up, Down), repr(cell_indices)
        voice = abjad.Voice()
        voice.consists_commands.append('Horizontal_bracket_engraver')
        staff = abjad.Staff([voice])
        score = abjad.Score([staff])
        leaf_list_stack = []
        self._populate_voice(
            leaf_list_stack,
            self,
            voice,
            after_cell_spacing=after_cell_spacing,
            brackets=brackets,
            markup_direction=markup_direction,
            )
        assert leaf_list_stack == [], repr(leaf_list_stack)
        first_leaf = abjad.inspect(voice).get_leaf(n=0)
        abjad.attach(abjad.TimeSignature((1, 8)), first_leaf)
        self._color_repeats(color_repeats, voice)
        self._attach_cell_indices(cell_indices, voice)
        self._label_set_classes(set_classes, voice)
        score.add_final_bar_line()
        abjad.override(score).bar_line.transparent = True
        abjad.override(score).bar_number.stencil = False
        abjad.override(score).beam.stencil = False
        abjad.override(score).flag.stencil = False
        abjad.override(score).horizontal_bracket.staff_padding = 4
        abjad.override(score).stem.stencil = False
        abjad.override(score).text_script.staff_padding = 2
        abjad.override(score).time_signature.stencil = False
        string = 'override Score.BarLine.transparent = ##f'
        command = abjad.LilyPondCommand(string, format_slot='after')
        last_leaf = abjad.select().by_leaf()(score)[-1][-1]
        abjad.attach(command, last_leaf)
        moment = abjad.schemetools.SchemeMoment((1, 16))
        abjad.set_(score).proportional_notation_duration = moment
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(
            global_staff_size=global_staff_size,
            music=score,
            )
        abjad.override(score).spacing_spanner.strict_grace_spacing = True
        abjad.override(score).spacing_spanner.strict_note_spacing = True
        abjad.override(score).spacing_spanner.uniform_stretching = True
        abjad.override(score).text_script.X_extent = False
        if 'title' in keywords:
            title = keywords.get('title') 
            if not isinstance(title, abjad.Markup):
                title = abjad.Markup(title)
            lilypond_file.header_block.title = title
        if 'subtitle' in keywords:
            markup = abjad.Markup(keywords.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        string = 'accidentalStyle dodecaphonic'
        command = abjad.LilyPondCommand(string)
        lilypond_file.layout_block.items.append(command)
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.line_width = 287.5
        lilypond_file.layout_block.ragged_right = True
        string = 'markup-system-spacing.padding = 8'
        command = abjad.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'system-system-spacing.padding = 10'
        command = abjad.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'top-markup-spacing.padding = 4'
        command = abjad.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        return lilypond_file

    ### PRIVATE METHODS ###

    def _attach_cell_indices(self, cell_indices, voice):
        if not cell_indices:
            return
        cell_spanners = self._get_cell_spanners(voice)
        cell_spanners.sort(
            key=lambda x: abjad.inspect(x).get_timespan().start_offset
            )
        if cell_indices is True:
            direction = Up
        else:
            direction = cell_indices
        cell_index = 0
        for cell_spanner in cell_spanners:
            negative_level = abjad.inspect(cell_spanner).get_indicator(int)
            if negative_level != -2:
                continue
            markup = abjad.Markup(cell_index, direction=direction)
            if direction is Down:
                abjad.tweak(markup).staff_padding = 7
            first_leaf = cell_spanner.components[0]
            abjad.attach(markup, first_leaf)
            cell_index += 1
            
    def _color_repeats(self, color_repeats, voice):
        if not color_repeats:
            return
        leaves = abjad.iterate(voice).by_class(prototype=abjad.Note)
        pairs = abjad.Sequence(leaves).nwise(n=2, wrapped=True)
        current_color = 'red'
        for left, right in pairs:
            if not left.written_pitch == right.written_pitch:
                continue
            abjad.label(left).color_leaves(current_color)
            abjad.label(right).color_leaves(current_color)
            if current_color == 'red':
                current_color = 'blue'
            else:
                current_color = 'red'

    def _get_cell_spanners(self, voice):
        spanners = set()
        for leaf in abjad.iterate(voice).by_leaf():
            spanners_ = abjad.inspect(leaf).get_spanners()
            spanners.update(spanners_)
        class_ = abjad.Spanner
        spanners = [_ for _ in spanners if _.__class__ is class_]
        return spanners

    def _label_set_classes(
        self,
        set_classes,
        voice,
        ):
        if not set_classes:
            return
        spanners = self._get_cell_spanners(voice)
        for spanner in spanners:
            leaves = spanner.components
            pitch_class_set = baca.PitchClassSet.from_selection(leaves)
            if not pitch_class_set:
                continue
            set_class = abjad.SetClass.from_pitch_class_set(
                pitch_class_set,
                lex_rank=True,
                transposition_only=True,
                )
            string = str(set_class)
            command = abjad.markuptools.MarkupCommand('line', [string])
            label = abjad.markuptools.Markup(command, direction=Up)
            if label is not None:
                label = label.small()
                first_leaf = leaves[0]
                abjad.attach(label, first_leaf)

    def _populate_voice(
        self,
        leaf_list_stack,
        node,
        voice,
        after_cell_spacing=False,
        brackets=True,
        markup_direction=None,
        ):
        if len(node):
            if node._get_level():
                leaf_list_stack.append([])
            for child_node in node:
                self._populate_voice(
                    leaf_list_stack,
                    child_node,
                    voice,
                    after_cell_spacing=after_cell_spacing,
                    brackets=brackets,
                    markup_direction=markup_direction,
                    )
            if node._get_level():
                first_note = leaf_list_stack[-1][0]
                last_note = leaf_list_stack[-1][-1]
                leaves_with_skips = []
                leaf = first_note
                while leaf is not last_note:
                    leaves_with_skips.append(leaf)
                    leaf = abjad.inspect(leaf).get_leaf(n=1)
                leaves_with_skips.append(leaf)
                spanner = abjad.Spanner()
                negative_level = node._get_level(negative=True)
                abjad.attach(negative_level, spanner)
                abjad.attach(spanner, leaves_with_skips)
                if brackets:
                    bracket = abjad.HorizontalBracketSpanner()
                    abjad.attach(bracket, leaves_with_skips)
                leaf_list_stack.pop()
        else:
            assert node._payload is not None
            note = abjad.Note(
                node._payload,
                abjad.Duration(1, 8),
                )
            if node._is_leftmost_leaf():
                for parent in node._get_parentage(include_self=True):
                    #node_markup = parent._get_node_markup(
                    #    direction=markup_direction,
                    #    )
                    if parent._expression is not None:
                        node_markup = parent._expression.get_markup()
                        if node_markup is not None:
                            node_markup = abjad.new(
                                node_markup,
                                direction=markup_direction,
                                )
                            abjad.attach(node_markup, note)
            voice.append(note)
            if node._is_rightmost_leaf():
                if after_cell_spacing:
                    skip = abjad.Skip((1, 8))
                    voice.append(skip)
            for leaf_list in leaf_list_stack:
                leaf_list.append(note)

    ### PUBLIC METHODS ###

    def has_repeats(self):
        r'''Is true when tree has repeats.

        ..  container:: example

            Has repeats:

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [1, 2, 2, 4]]
                >>> tree = baca.PitchTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ::

                >>> tree.has_repeats()
                True

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            \time 1/8
                            e'8 \startGroup ^ \markup { 0 }
                            fs'8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            cs'8 \stopGroup
                            s8
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            cs'8 \startGroup ^ \markup { 2 }
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'8
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'8
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Doesn't have repeats:

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ::

                >>> tree.has_repeats()
                False

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e'8 \startGroup ^ \markup { 0 }
                            fs'8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        Returns true or false.
        '''
        leaves = self.iterate(level=-1)
        for left, right in abjad.Sequence(leaves).nwise(n=2, wrapped=True):
            if left == right:
                return True
        return False

    def invert(self, axis=None):
        r"""Inverts pitch tree.

        ..  container:: example

            Example tree:

            ::

                >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e''8 \startGroup ^ \markup { 0 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Inverts tree about first pitch when axis is none:

            ::

                >>> inversion = tree.invert()
                >>> show(inversion) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e''8 \startGroup ^ \markup { 0 }
                            d''8
                            bf''8 \stopGroup
                            s8
                            b''8 \startGroup ^ \markup { 1 }
                            cs'''8
                            c'''8
                            a''8
                            b''8
                            g'''8 \stopGroup
                            s8
                            af'''8 \startGroup ^ \markup { 2 }
                            fs'''8
                            f'''8
                            ef'''8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Inverts tree about pitch 0:

            ::

                >>> inversion = tree.invert(axis=0)
                >>> show(inversion) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            af,8 \startGroup ^ \markup { 0 }
                            fs,8
                            d8 \stopGroup
                            s8
                            ef8 \startGroup ^ \markup { 1 }
                            f8
                            e8
                            cs8
                            ef8
                            b8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            bf8
                            a8
                            g8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Inverts tree about pitch 13:

            ::

                >>> inversion = tree.invert(axis=13)
                >>> show(inversion) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            bf'8 \startGroup ^ \markup { 0 }
                            af'8
                            e''8 \stopGroup
                            s8
                            f''8 \startGroup ^ \markup { 1 }
                            g''8
                            fs''8
                            ef''8
                            f''8
                            cs'''8 \stopGroup
                            s8
                            d'''8 \startGroup ^ \markup { 2 }
                            c'''8
                            b''8
                            a''8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            ::

                >>> isinstance(inversion, baca.PitchTree)
                True

        """
        if axis is None and self:
            payload = self.get_payload()
            axis = payload[0]
        operator = abjad.Inversion(axis=axis)
        return self._apply_to_leaves_and_emit_new_tree(operator)

    def retrograde(self):
        r"""Gets retrograde of tree.

        ..  container:: example

            Example tree:

            ::

                >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e''8 \startGroup ^ \markup { 0 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Gets retrograde of tree:

            ::

                >>> retrograde = tree.retrograde()
                >>> show(retrograde) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = retrograde.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            c'8 \startGroup ^ \markup { 0 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            e''8 \startGroup ^ \markup { 2 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            ::

                >>> isinstance(retrograde, baca.PitchTree)
                True

        """
        items = list(self.items)
        items.reverse()
        result = abjad.new(self, items=items)
        return result

    def rotate(self, n=0):
        r"""Rotates tree by index `n`.

        ..  container:: example

            Example tree:

            ::

                >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e''8 \startGroup ^ \markup { 0 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Rotates tree to the right:

            ::

                >>> rotation = tree.rotate(n=1)
                >>> show(rotation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            c'8 \startGroup ^ \markup { 0 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            e''8 \startGroup ^ \markup { 1 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 2 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Rotates tree to the left:

            ::

                >>> rotation = tree.rotate(n=-1)
                >>> show(rotation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            a'8 \startGroup ^ \markup { 0 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 1 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            e''8 \startGroup ^ \markup { 2 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Rotates by zero:

            ::

                >>> rotation = tree.rotate(n=0)
                >>> show(rotation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e''8 \startGroup ^ \markup { 0 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            ::

                >>> isinstance(rotation, baca.PitchTree)
                True

        """
        items = list(self.items)
        items = abjad.sequence(items)
        items = items.rotate(n=n)
        result = abjad.new(self, items=items)
        return result

    def transpose(self, n=0):
        r"""Transposes pitch tree.

        ..  container:: example

            Example tree:

            ::

                >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.PitchTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e''8 \startGroup ^ \markup { 0 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Transposes tree by positive index:

            ::

                >>> transposition = tree.transpose(n=13)
                >>> show(transposition) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            f'''8 \startGroup ^ \markup { 0 }
                            g'''8
                            b''8 \stopGroup
                            s8
                            bf''8 \startGroup ^ \markup { 1 }
                            af''8
                            a''8
                            c'''8
                            bf''8
                            d''8 \stopGroup
                            s8
                            cs''8 \startGroup ^ \markup { 2 }
                            ef''8
                            e''8
                            fs''8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Transposes tree by negative index:

            ::

                >>> transposition = tree.transpose(n=-13)
                >>> show(transposition) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            ef'8 \startGroup ^ \markup { 0 }
                            f'8
                            a8 \stopGroup
                            s8
                            af8 \startGroup ^ \markup { 1 }
                            fs8
                            g8
                            bf8
                            af8
                            c8 \stopGroup
                            s8
                            b,8 \startGroup ^ \markup { 2 }
                            cs8
                            d8
                            e8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Transposes tree by zero index:

            ::

                >>> transposition = tree.transpose(n=0)
                >>> show(transposition) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            e''8 \startGroup ^ \markup { 0 }
                            fs''8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup ^ \markup { 1 }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup ^ \markup { 2 }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            ::

                >>> isinstance(transposition, baca.PitchTree)
                True

        """
        operator = abjad.Transposition(n=n)
        return self._apply_to_leaves_and_emit_new_tree(operator)

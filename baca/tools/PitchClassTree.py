# -*- coding: utf-8 -*-
import abjad
from baca.tools.Tree import Tree


class PitchClassTree(Tree):
    r'''Pitch-class tree.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Numbered pitch-class tree:

        ::

            >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.tools.PitchClassTree(items=items)
            >>> show(tree) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = tree.__illustrate__()
            >>> f(lilypond_file.score_block)
            \score {
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
            }

    ..  container:: example

        Named pitch-class tree:

        ::

            >>> items = [
            ...     ['e', 'fs', 'bf'],
            ...     ['a', 'g', 'af', 'b', 'a', 'cs'],
            ...     ['c', 'd', 'ef', 'f'],
            ...     ]
            >>> tree = baca.tools.PitchClassTree(
            ...     items=items,
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )
            >>> show(tree) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = tree.__illustrate__()
            >>> f(lilypond_file.score_block)
            \score {
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
            }

    ..  container:: example

        From other trees:

        ::

            >>> items = [
            ...     baca.tools.PitchClassTree([4, 6, 10], name='J'),
            ...     baca.tools.PitchClassTree([9, 7, 8, 11, 9, 1], name='K'),
            ...     baca.tools.PitchClassTree([0, 2, 3, 5], name='L'),
            ...     ]
            >>> tree = baca.tools.PitchClassTree(items=items)
            >>> lilypond_file = tree.__illustrate__(
            ...     cell_indices=False,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file.score_block)
            \score {
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
                                    \bold
                                        J
                                    }
                            fs'8
                            bf'8 \stopGroup
                            s8
                            a'8 \startGroup
                                ^ \markup {
                                    \bold
                                        K
                                    }
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8 \stopGroup
                            s8
                            c'8 \startGroup
                                ^ \markup {
                                    \bold
                                        L
                                    }
                            d'8
                            ef'8
                            f'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>
            }

    ..  container:: example

        From segments:

        ::

            >>> items = [
            ...     pitchtools.PitchClassSegment([4, 6, 10], name='J'),
            ...     pitchtools.PitchClassSegment([9, 7, 8, 11, 9, 1], name='K'),
            ...     pitchtools.PitchClassSegment([0, 2, 3, 5], name='L'),
            ...     ]
            >>> items = [segment.rotate(n=1) for segment in items]
            >>> tree = baca.tools.PitchClassTree(items=items)
            >>> show(tree, cell_indices=False) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = tree.__illustrate__(cell_indices=False)
            >>> f(lilypond_file.score_block)
            \score {
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
                                ^ \markup {
                                    \concat
                                        {
                                            r
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        J
                                                }
                                        }
                                    }
                            e'8
                            fs'8 \stopGroup
                            s8
                            cs'8 \startGroup
                                ^ \markup {
                                    \concat
                                        {
                                            r
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        K
                                                }
                                        }
                                    }
                            a'8
                            g'8
                            af'8
                            b'8
                            a'8 \stopGroup
                            s8
                            f'8 \startGroup
                                ^ \markup {
                                    \concat
                                        {
                                            r
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        L
                                                }
                                        }
                                    }
                            c'8
                            d'8
                            ef'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>
            }

    ..  container:: example

        Nested:

        ::

            >>> segment_1 = pitchtools.PitchClassSegment([4, 6, 10], name='J')
            >>> segment_2 = pitchtools.PitchClassSegment([9, 7, 8, 11, 9, 1], name='K')
            >>> segment_3 = pitchtools.PitchClassSegment([0, 2, 3, 5], name='L')
            >>> segment_1 = segment_1.transpose(n=1)
            >>> segment_2 = segment_2.transpose(n=1)
            >>> segment_3 = segment_3.transpose(n=1)
            >>> items = [[segment_1, segment_2], segment_3]
            >>> tree = baca.tools.PitchClassTree(items=items)
            >>> graph(tree) # doctest: +SKIP

        ..  doctest::

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

        ..  doctest::

            >>> lilypond_file = tree.__illustrate__(cell_indices=False)
            >>> f(lilypond_file.score_block)
            \score {
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
                                ^ \markup {
                                    \concat
                                        {
                                            T
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        J
                                                }
                                        }
                                    }
                            g'8
                            b'8 \stopGroup
                            s8
                            bf'8 \startGroup
                                ^ \markup {
                                    \concat
                                        {
                                            T
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        K
                                                }
                                        }
                                    }
                            af'8
                            a'8
                            c'8
                            bf'8
                            d'8 \stopGroup \stopGroup
                            s8
                            cs'8 \startGroup
                                ^ \markup {
                                    \concat
                                        {
                                            T
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        L
                                                }
                                        }
                                    }
                            ef'8
                            e'8
                            fs'8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>
            }

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
        name=None,
        name_markup=None,
        ):
        item_class = item_class or abjad.pitchtools.NumberedPitchClass
        Tree.__init__(
            self,
            items=items,
            item_class=item_class,
            name=name,
            name_markup=name_markup,
            )

    ### SPECIAL METHODS ###

    def __graph__(self, **keywords):
        r'''Graphs pitch-class tree.

        ..  container:: example

            Graphs numbered pitch-class tree:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.tools.PitchClassTree(items=items)

            ::

                >>> graph(tree) # doctest: +SKIP

            ..  doctest::

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

            Graphs named pitch-class tree:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.tools.PitchClassTree(
                ...     items=items,
                ...     item_class=pitchtools.NamedPitch,
                ...     )

            ::

                >>> graph(tree) # doctest: +SKIP

            ..  doctest::

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
        superclass = super(PitchClassTree, self)
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
        r'''Illustrates pitch-class tree.

        ..  container:: example

            Default:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.tools.PitchClassTree(items=items)
                >>> lilypond_file = tree.__illustrate__()
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file.score_block)
                \score {
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
                }

        ..  container:: example

            With set-classes:

            ::

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.tools.PitchClassTree(items=items)
                >>> lilypond_file = tree.__illustrate__(
                ...     cell_indices=Down,
                ...     set_classes=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file.score_block)
                \score {
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
                }

        ..  container:: example

            Nested:

            ::

                >>> segment_1 = pitchtools.PitchClassSegment([4, 6, 10], name='J')
                >>> segment_2 = pitchtools.PitchClassSegment([9, 7, 8, 11, 9, 1], name='K')
                >>> segment_3 = pitchtools.PitchClassSegment([0, 2, 3, 5], name='L')
                >>> segment_1 = segment_1.transpose(n=1)
                >>> segment_2 = segment_2.transpose(n=1)
                >>> segment_3 = segment_3.transpose(n=1)
                >>> items = [[segment_1, segment_2], segment_3]
                >>> tree = baca.tools.PitchClassTree(items=items)
                >>> lilypond_file = tree.__illustrate__(
                ...     cell_indices=Down,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file.score_block)
                \score {
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
                                    ^ \markup {
                                        \concat
                                            {
                                                T
                                                \hspace
                                                    #-0.2
                                                \sub
                                                    1
                                                \concat
                                                    {
                                                        \hspace
                                                            #0.4
                                                        \bold
                                                            J
                                                    }
                                            }
                                        }
                                    - \tweak staff-padding #7
                                    _ \markup { 0 }
                                g'8
                                b'8 \stopGroup
                                s8
                                bf'8 \startGroup
                                    ^ \markup {
                                        \concat
                                            {
                                                T
                                                \hspace
                                                    #-0.2
                                                \sub
                                                    1
                                                \concat
                                                    {
                                                        \hspace
                                                            #0.4
                                                        \bold
                                                            K
                                                    }
                                            }
                                        }
                                    - \tweak staff-padding #7
                                    _ \markup { 1 }
                                af'8
                                a'8
                                c'8
                                bf'8
                                d'8 \stopGroup \stopGroup
                                s8
                                cs'8 \startGroup
                                    ^ \markup {
                                        \concat
                                            {
                                                T
                                                \hspace
                                                    #-0.2
                                                \sub
                                                    1
                                                \concat
                                                    {
                                                        \hspace
                                                            #0.4
                                                        \bold
                                                            L
                                                    }
                                            }
                                        }
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
                }

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
        first_leaf = abjad.inspect_(voice).get_leaf(n=0)
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
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(
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
        command = abjad.indicatortools.LilyPondCommand(string)
        lilypond_file.layout_block.items.append(command)
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.line_width = 287.5
        lilypond_file.layout_block.ragged_right = True
        string = 'markup-system-spacing.padding = 8'
        command = abjad.indicatortools.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'system-system-spacing.padding = 10'
        command = abjad.indicatortools.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'top-markup-spacing.padding = 4'
        command = abjad.indicatortools.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        return lilypond_file

    ### PRIVATE METHODS ###

    def _attach_cell_indices(self, cell_indices, voice):
        if not cell_indices:
            return
        cell_spanners = self._get_cell_spanners(voice)
        cell_spanners.sort(
            key=lambda x: abjad.inspect_(x).get_timespan().start_offset
            )
        if cell_indices is True:
            direction = Up
        else:
            direction = cell_indices
        cell_index = 0
        for cell_spanner in cell_spanners:
            negative_level = abjad.inspect_(cell_spanner).get_indicator(int)
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
        pairs = abjad.sequencetools.iterate_sequence_nwise(
            leaves,
            n=2,
            wrapped=True,
            )
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
            spanners_ = abjad.inspect_(leaf).get_spanners()
            spanners.update(spanners_)
        class_ = abjad.spannertools.Spanner
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
            pitch_class_set = abjad.pitchtools.PitchClassSet.from_selection(
                leaves
                )
            if not pitch_class_set:
                continue
            set_class = abjad.pitchtools.SetClass.from_pitch_class_set(
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
                    leaf = abjad.inspect_(leaf).get_leaf(n=1)
                leaves_with_skips.append(leaf)
                spanner = abjad.spannertools.Spanner()
                negative_level = node._get_level(negative=True)
                abjad.attach(negative_level, spanner)
                abjad.attach(spanner, leaves_with_skips)
                if brackets:
                    bracket = abjad.spannertools.HorizontalBracketSpanner()
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
                    node_markup = parent._get_node_markup(
                        direction=markup_direction,
                        )
                    if node_markup is not None:
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
                >>> tree = baca.tools.PitchClassTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ::

                >>> tree.has_repeats()
                True

            ..  doctest::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file.score_block)
                \score {
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
                }

        ..  container:: example

            Doesn't have repeats:

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
                >>> tree = baca.tools.PitchClassTree(items=items)
                >>> show(tree) # doctest: +SKIP

            ::

                >>> tree.has_repeats()
                False

            ..  doctest::

                >>> lilypond_file = tree.__illustrate__()
                >>> f(lilypond_file.score_block)
                \score {
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
                }

        Returns true or false.
        '''
        leaves = self.iterate(level=-1)
        pairs = abjad.sequencetools.iterate_sequence_nwise(
            leaves,
            n=2,
            wrapped=True,
            )
        for left, right in pairs:
            if left == right:
                return True
        return False

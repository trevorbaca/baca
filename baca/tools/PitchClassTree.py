# -*- coding: utf-8 -*-
import abjad
from baca.tools.PayloadTree import PayloadTree


class PitchClassTree(PayloadTree):
    r'''Pitch-class tree.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Numbered pitch-class tree:

        ::

            >>> tree = baca.tools.PitchClassTree(
            ...     items=[[0, 4, 7, 8], [9, 2, 3, 11]],
            ...     item_class=pitchtools.NumberedPitchClass,
            ...     )

        ::

            >>> print(format(tree, 'storage'))
            baca.tools.PitchClassTree(
                [
                    [
                        pitchtools.NumberedPitchClass(0),
                        pitchtools.NumberedPitchClass(4),
                        pitchtools.NumberedPitchClass(7),
                        pitchtools.NumberedPitchClass(8),
                        ],
                    [
                        pitchtools.NumberedPitchClass(9),
                        pitchtools.NumberedPitchClass(2),
                        pitchtools.NumberedPitchClass(3),
                        pitchtools.NumberedPitchClass(11),
                        ],
                    ]
                )

    ..  container:: example

        **Example 2.** Named pitch-class tree:

        ::

            >>> tree = baca.tools.PitchClassTree(
            ...     items=[['c', 'e', 'g', 'af'], ['a', 'd', 'ef', 'b']],
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )

        ::

            >>> print(format(tree, 'storage'))
            baca.tools.PitchClassTree(
                [
                    [
                        pitchtools.NamedPitchClass('c'),
                        pitchtools.NamedPitchClass('e'),
                        pitchtools.NamedPitchClass('g'),
                        pitchtools.NamedPitchClass('af'),
                        ],
                    [
                        pitchtools.NamedPitchClass('a'),
                        pitchtools.NamedPitchClass('d'),
                        pitchtools.NamedPitchClass('ef'),
                        pitchtools.NamedPitchClass('b'),
                        ],
                    ]
                )

    Pitch-class trees are treated as immutable.
    '''
    
    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        PayloadTree.__init__(
            self,
            expr=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __illustrate__(self, **kwargs):
        r'''Illustrates pitch-class tree.

        ..  container:: example

            **Example.** Illustrates pitch-class tree:

            ::

                >>> tree = baca.tools.PitchClassTree(
                ...     items=[[0, 4, 7, 8], [9, 2, 3, 11]],
                ...     item_class=pitchtools.NumberedPitchClass,
                ...     )
                >>> show(tree) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = tree.__illustrate__()
                >>> score_block = lilypond_file.score_block
                >>> f(score_block)
                \score {
                    \new Score \with {
                        \override BarLine.transparent = ##t
                        \override BarNumber.stencil = ##f
                        \override Beam.stencil = ##f
                        \override Flag.stencil = ##f
                        \override HorizontalBracket.staff-padding = #4
                        \override Stem.stencil = ##f
                        \override TextScript.staff-padding = #2
                        \override TimeSignature.stencil = ##f
                        proportionalNotationDuration = #(ly:make-moment 1 14)
                    } <<
                        \new Staff {
                            \new Voice \with {
                                \consists Horizontal_bracket_engraver
                            } {
                                c'8 \startGroup ^ \markup { 0 }
                                e'8
                                g'8
                                af'8 \stopGroup
                                a'8 \startGroup ^ \markup { 1 }
                                d'8
                                ef'8
                                b'8 \stopGroup
                                \bar "|."
                                \override Score.BarLine.transparent = ##f
                            }
                        }
                    >>
                }

        Returns LilyPond file.
        '''
        voice = abjad.Voice()
        voice.consists_commands.append('Horizontal_bracket_engraver')
        staff = abjad.Staff([voice])
        score = abjad.Score([staff])
        leaf_list_stack = []
        self._bracket_inner_nodes(leaf_list_stack, self, voice)
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
        command = abjad.indicatortools.LilyPondCommand(
            string, format_slot='after')
        last_leaf = abjad.select().by_leaf()(score)[-1][-1]
        abjad.attach(command, last_leaf)
        moment = abjad.schemetools.SchemeMoment((1, 14))
        abjad.set_(score).proportional_notation_duration = moment
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(
            global_staff_size=12,
            music=score,
            )
        if 'title' in kwargs:
            title = kwargs.get('title') 
            if not isinstance(title, abjad.Markup):
                title = abjad.Markup(title)
            lilypond_file.header_block.title = title
        if 'subtitle' in kwargs:
            markup = bajda.Markup(kwargs.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        command = abjad.indicatortools.LilyPondCommand(
            'accidentalStyle forget')
        lilypond_file.layout_block.items.append(command)
        lilypond_file.layout_block.indent = 0
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

    def _bracket_inner_nodes(self, leaf_list_stack, node, voice):
        if len(node):
            if node.level:
                leaf_list_stack.append([])
            for child_node in node:
                self._bracket_inner_nodes(
                    leaf_list_stack,
                    child_node,
                    voice,
                    )
            if node.level:
                bracket = abjad.spannertools.HorizontalBracketSpanner()
                abjad.attach(bracket, leaf_list_stack[-1])
                if node.level == 1:
                    node_index = node.parent.index(node)
                    level_one_first_leaf = leaf_list_stack[-1][0]
                    markup = abjad.Markup(node_index, direction=Up)
                    abjad.attach(markup, level_one_first_leaf)
                leaf_list_stack.pop()
        elif node.payload:
            note = abjad.Note(
                node.payload,
                abjad.durationtools.Duration(1, 8),
                )
            voice.append(note)
            for leaf_list in leaf_list_stack:
                leaf_list.append(note)
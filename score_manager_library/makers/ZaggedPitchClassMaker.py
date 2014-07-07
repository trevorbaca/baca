# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import lilypondfiletools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from scoremanager import idetools
import baca


class ZaggedPitchClassMaker(AbjadObject):
    r'''Zagged pitch-class maker.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_division_cells',
        '_grouping_counts',
        '_pc_cells',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pc_cells=None,
        division_cells=None,
        grouping_counts=None,
        ):
        self._pc_cells = pc_cells
        self._division_cells = division_cells
        self._grouping_counts = grouping_counts

    ### SPECIAL METHODS ###

    def __call__(self):
        pc_cells = baca.utilities.helianthate(
            self.pc_cells, 
            -1, 
            1,
            )
        division_cells = baca.utilities.helianthate(
            self.division_cells, 
            -1, 
            1,
            )
        division_cells = sequencetools.flatten_sequence(
            division_cells, 
            depth=1,
            )
        division_cells = datastructuretools.CyclicTuple(division_cells)
        tmp = []
        for i, pc_segment in enumerate(pc_cells):
            parts = sequencetools.partition_sequence_by_ratio_of_lengths(
                pc_segment, 
                division_cells[i],
                )
            tmp.extend(parts)
        pc_cells = tmp
        pc_cells = sequencetools.partition_sequence_by_counts(
            pc_cells, 
            self.grouping_counts, 
            cyclic=True, 
            overhang=True,
            )
        pc_cells = [sequencetools.join_subsequences(x) for x in pc_cells]
        pc_cells = sequencetools.partition_sequence_by_counts(
            pc_cells, 
            self.grouping_counts, 
            cyclic=True, 
            overhang=True,
            )
        material = datastructuretools.CyclicPayloadTree(pc_cells)
        material = datastructuretools.StatalServer(material)
        return material

    def __eq__(self, expr):
        r'''Is true when `expr` is a zagged pitch-class with type and 
        public properties equal to those of this zagged pitch-class maker.
        Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes zagged pitch-class maker.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    def __illustrate__(self, **kwargs):
        r'''Illustrates zagged pitch-class maker.

        Returns LilyPond file.
        '''
        statal_server = self()
        material = statal_server.cyclic_tree
        pcs = list(material.iterate_payload())
        leaves = scoretools.make_leaves(pcs, [durationtools.Duration(1, 8)])
        voice = scoretools.Voice(leaves)
        staff = scoretools.Staff([voice])
        score = scoretools.Score([staff])
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        configuration = idetools.Configuration()
        stylesheet = os.path.join(
            configuration.abjad_stylesheets_directory,
            'rhythm-letter-16.ly',
            )
        lilypond_file.file_initial_user_includes.append(stylesheet)
        voice.consists_commands.append('Horizontal_bracket_engraver')
        for level in (1, 2):
            level_sizes = []
            for x in material.iterate_at_level(level):
                size = len(list(x.iterate_payload()))
                level_sizes.append(size)
            for part in sequencetools.partition_sequence_by_counts(
                voice.select_leaves(), 
                level_sizes, 
                cyclic=False, 
                overhang=False,
                ):
                spannertools.HorizontalBracketSpanner(part)
        current_group = 0
        for leaf in voice.select_leaves():
            spanner_classes = spannertools.HorizontalBracketSpanner
            brackets = inspect_(leaf).get_spanners(spanner_classes)
            brackets = tuple(brackets)
            if brackets[0][0] is leaf:
                if brackets[1][0] is leaf:
                    string = r'\bold {{ {} }}'.format(current_group)
                    markup = markuptools.Markup(string, Up)
                    markup.attach(leaf)
                    current_group += 1
        bar_line = score.add_double_bar()
        score.override.bar_line.stencil = False
        score.override.flag.stencil = False
        score.override.stem.stencil = False
        score.override.text_script.staff_padding = 3
        score.override.time_signature.stencil = False
        if 'title' in kwargs:
            markup = markuptools.Markup(kwargs.get('title'))
            lilypond_file.header_block.title = markup
        if 'subtitle' in kwargs:
            markup = markuptools.Markup(kwargs.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        command = marktools.LilyPondCommandMark('accidentalStyle forget')
        lilypond_file.layout_block.append(command)
        score.override.note_head.color = 'red'
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='pc_cells',
                command='pc',
                editor=idetools.getters.get_lists,
                ),
            systemtools.AttributeDetail(
                name='division_cells',
                command='dc',
                editor=idetools.getters.get_lists,
                ),
            systemtools.AttributeDetail(
                name='grouping_counts',
                command='gc',
                editor=idetools.getters.get_nonnegative_integers,
                ),
            )

    @property
    def _input_demo_values(self):
        return [
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', 
            [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),
        ]

    ### PRIVATE METHODS ###

    ### PUBLIC PROPERTIES ###

    @property
    def division_cells(self):
        r'''Gets division cells of maker.

        Returns list of lists.
        '''
        return self._division_cells

    @property
    def grouping_counts(self):
        r'''Gets grouping counts of maker.

        Returns nonempty list of positive integers.
        '''
        return self._grouping_counts

    @property
    def pc_cells(self):
        r'''Gets pitch-class cells of maker.

        Returns list of number lists.
        '''
        return self._pc_cells
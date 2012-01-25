from baca.scf.BasicModuleProxy import BasicModuleProxy


class IllustrationBuilderModuleProxy(BasicModuleProxy):

    ### PUBLIC METHODS ###

    def write_stub_to_disk(self, prompt=True):
        self.clear()
        self.setup_statements.append('from abjad import *\n')
        line = 'from output_material import {}\n'.format(self.module_short_name)
        self.setup_statements.append(line)
        line = 'score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves({})\n'
        line = line.format(self.module_short_name)
        self.body_lines.append(line)
        self.body_lines.append('illustration = lilypondfiletools.make_basic_lilypond_file(score)\n')
        self.write_to_disk()
        self.proceed('stub illustration builder written to disk.', prompt=prompt)

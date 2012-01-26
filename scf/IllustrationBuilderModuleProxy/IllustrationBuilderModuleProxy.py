from abjad.tools import markuptools
from baca.scf.BasicModuleProxy import BasicModuleProxy
from baca.scf.helpers import safe_import


class IllustrationBuilderModuleProxy(BasicModuleProxy):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def illustration_ly_file_name(self):
        return self.full_file_name.replace('.py', '.ly')

    @property
    def illustration_pdf_file_name(self):
        return self.full_file_name.replace('.py', '.pdf')

    ### PUBLIC METHODS ###

    def import_illustration(self):
        self.unimport()
        # TODO: port unimport
        #self.unimport_output_material_module()
        illustration = safe_import(locals(), self.module_short_name, 'illustration', 
            source_parent_module_importable_nmae=self.parent_module_importable_name)
        illustration.header_block.title = markuptools.Markup(self.material_spaced_name)
        return illustration

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

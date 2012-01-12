from abjad.tools import durationtools
from abjad.tools import measuretools
from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf.editors.InteractiveEditor import InteractiveEditor
import os


class SargassoMeasureMaker(InteractiveEditor):

    def __init__(self, session=None, target=None, **kwargs):
        InteractiveEditor.__init__(self, session=session, target=target)
        self.stylesheet = os.path.join(os.path.dirname(__file__), 'stylesheet.ly')
        self._generic_output_name = 'sargasso measures'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.class_name

    output_file_import_statements = [
        'from abjad.tools.measuretools.Measure import Measure',]
            
    user_input_import_statements = [
        'from abjad.tools.durationtools import Duration',
        'from baca.scf.makers import SargassoMeasureMaker',
        'from baca.scf import UserInputWrapper',]

    user_input_template = UserInputWrapper([
        ('measure_denominator', 4),
        ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
        ('measure_division_denominator', 16),
        ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
        ('total_duration', durationtools.Duration(44, 8)),
        ('measures_are_scaled', True),
        ('measures_are_split', True),
        ('measures_are_shuffled', True),])

    ### PUBLIC METHODS ###

    def get_output_file_lines(self, measures, material_underscored_name):
        output_file_lines = []
        output_file_lines.append('%s = [' % material_underscored_name)
        for measure in measures[:-1]:
            line = measuretools.measure_to_one_line_input_string(measure)
            output_file_lines.append('\t%s,' % line)
        line = measuretools.measure_to_one_line_input_string(measures[-1])
        output_file_lines.append('\t%s]' % line)
        return output_file_lines

    def make(self, measure_denominator, measure_numerator_talea, 
        measure_division_denominator, measure_division_talea, total_duration,
        measures_are_scaled, measures_are_split, measures_are_shuffled):
        import baca
        return baca.music.make_sargasso_measures(measure_denominator, measure_numerator_talea,
            measure_division_denominator, measure_division_talea, total_duration,
            measures_are_scaled, measures_are_split, measures_are_shuffled)

    def make_lilypond_file_from_output_material(self, material):
        from baca.music.make_sargasso_measures import make_lilypond_file_from_output_material
        return make_lilypond_file_from_output_material(material)

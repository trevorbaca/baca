from abjad import *
import handlers


def test_ReiteratedArticulationHandler___repr___01():

    handler = handlers.articulations.ReiteratedArticulationHandler(
        articulation_list = ['.', '^'],
        minimum_prolated_duration = Duration(1, 16),
        maximum_prolated_duration = Duration(1, 8))

    assert repr(handler) == "ReiteratedArticulationHandler(articulation_list=['.', '^'], minimum_prolated_duration=Fraction(1, 16), maximum_prolated_duration=Fraction(1, 8))"

    assert handler._tools_package_qualified_indented_repr == "handlers.articulations.ReiteratedArticulationHandler(\n\tarticulation_list=['.', '^'],\n\tminimum_prolated_duration=Fraction(1, 16),\n\tmaximum_prolated_duration=Fraction(1, 8)\n\t)"

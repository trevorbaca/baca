from abjad import *
from experimental.tools import handlertools


def test_ReiteratedArticulationHandler___repr___01():

    handler = handlertools.articulations.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_prolated_duration=Duration(1, 16),
        maximum_prolated_duration=Duration(1, 8),
        )

    assert repr(handler) == "ReiteratedArticulationHandler(articulation_list=['.', '^'], minimum_prolated_duration=Duration(1, 16), maximum_prolated_duration=Duration(1, 8))"

    assert handler.storage_format == "handlertools.articulations.ReiteratedArticulationHandler(\n\tarticulation_list=['.', '^'],\n\tminimum_prolated_duration=durationtools.Duration(1, 16),\n\tmaximum_prolated_duration=durationtools.Duration(1, 8)\n\t)"

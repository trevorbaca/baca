from abjad.tools import *
from baca.specification.Directive import Directive
from baca.specification.DirectiveInventory import DirectiveInventory
from baca.specification.ScoreSpecification import ScoreSpecification
from baca.specification.Selection import Selection


def test_DirectiveInventory___repr___01():
    '''Repr is evaluable.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives
    directive_inventory_2 = eval(repr(directive_inventory_1))

    assert isinstance(directive_inventory_1, DirectiveInventory)
    assert isinstance(directive_inventory_2, DirectiveInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2

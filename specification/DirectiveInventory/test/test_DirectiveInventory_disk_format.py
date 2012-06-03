from abjad.tools import *
from baca.specification.DirectiveInventory import DirectiveInventory
from baca.specification.ScoreSpecification import ScoreSpecification
from baca import specification


def test_DirectiveInventory_disk_format_01():
    '''Disk format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives

    disk_format = directive_inventory_1._disk_format

    r'''
    specification.DirectiveInventory([
        specification.Directive(
            specification.Selection(
                '1'
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False
            )
        ])
    '''

    assert disk_format == "specification.DirectiveInventory([\n\tspecification.Directive(\n\t\tspecification.Selection(\n\t\t\t'1'\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    directive_inventory_2 = eval(disk_format)

    assert isinstance(directive_inventory_1, DirectiveInventory)
    assert isinstance(directive_inventory_2, DirectiveInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2

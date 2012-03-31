from abjad.tools import contexttools
from abjad.tools import durationtools
import scf


def test_ScorePackageProxy_tempo_inventory_01():

    score_package_proxy = scf.proxies.ScorePackageProxy('betoerung')

    assert score_package_proxy.tempo_inventory == contexttools.TempoMarkInventory([
        contexttools.TempoMark(durationtools.Duration(1, 4), 72), 
        contexttools.TempoMark(durationtools.Duration(1, 4), 108), 
        contexttools.TempoMark(durationtools.Duration(1, 4), 90), 
        contexttools.TempoMark(durationtools.Duration(1, 4), 135)])

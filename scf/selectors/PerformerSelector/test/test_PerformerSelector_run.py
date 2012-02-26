from abjad.tools.scoretools.Performer import Performer
from abjad.tools.instrumenttools.FrenchHorn import FrenchHorn
import scf


def test_PerformerSelector_run_01():

    selector = scf.selectors.PerformerSelector()
    selector.session._current_score_package_short_name = 'betoerung'
    result = selector.run(user_input='1')
    
    assert result == Performer(name='hornist', instruments=[FrenchHorn()])

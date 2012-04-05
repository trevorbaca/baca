from abjad.tools import timetokentools
import scf


def test_PackageContentSelector_run_01():

    selector = scf.selectors.PackageContentSelector()
    selector.asset_container_package_importable_names = ['abjad.tools.timetokentools']

    assert selector.run(user_input='notefilled') == timetokentools.NoteFilledTimeTokenMaker

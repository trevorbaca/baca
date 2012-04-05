import handlers
import scf


def test_PackageContentSelector_run_01():

    selector = scf.selectors.PackageContentSelector()
    selector.asset_container_package_importable_names = ['handlers.kaleids']

    assert selector.run(user_input='notefilled') == handlers.kaleids.NoteFilledTimeTokenMaker

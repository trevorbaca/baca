import kaleids
import scf


def test_PackageContentSelector_run_01():

    selector = scf.selectors.PackageContentSelector()
    selector.asset_container_package_importable_names = ['kaleids']

    assert selector.run(user_input='notefilled') == kaleids.NoteFilledTokens

from rhythm import kaleids
import os
import scf


def test_DirectoryContentSelector_run_01():

    selector = scf.selectors.DirectoryContentSelector()
    selector.asset_container_path_names = [os.environ.get('KALEIDPATH')]

    assert selector.run(user_input='notefilled') == 'NoteFilledTokens'

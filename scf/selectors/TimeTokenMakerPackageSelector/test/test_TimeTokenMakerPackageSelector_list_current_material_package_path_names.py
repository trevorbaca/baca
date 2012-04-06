import os
import scf


def test_TimeTokenMakerPackageSelector_list_current_material_package_path_names_01():

    selector = scf.selectors.TimeTokenMakerPackageSelector()
    selector.session._current_score_package_short_name = 'betoerung'
    speckled_kaleid_path_name = os.path.join(
        os.environ.get('SCORES'), 'betoerung', 'mus', 'materials', 'speckled_kaleid')

    assert speckled_kaleid_path_name in selector.list_current_material_package_path_names()

import os
import scf


def test_KaleidPackageSelector_list_material_package_path_names_in_current_score_01():

    selector = scf.selectors.KaleidPackageSelector()
    selector.session._current_score_package_short_name = 'betoerung'
    speckled_kaleid_path_name = os.path.join(
        os.environ.get('SCORES'), 'betoerung', 'mus', 'materials', 'speckled_kaleid')

    assert speckled_kaleid_path_name in selector.list_material_package_path_names_in_current_score()

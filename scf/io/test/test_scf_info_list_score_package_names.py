from baca import scf


def test_scf_info_list_score_package_names_01( ):

   score_package_names = scf.io.list_score_package_names( )

   assert 'aracilik' in score_package_names
   assert 'archipel' in score_package_names
   assert 'sekka' in score_package_names

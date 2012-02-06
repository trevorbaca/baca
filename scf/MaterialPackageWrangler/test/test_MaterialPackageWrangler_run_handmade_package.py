import baca
import py


def test_MaterialPackageWrangler_run_handmade_package_01():
    '''Make handmade package.
    Delete package.
    '''
    
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testnotes')

    try:
        studio.run(user_input='m h testnotes default default q')
        assert studio.package_exists('baca.materials.testnotes')
        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
        assert mpp.directory_contents == ['__init__.py', 'illustration_builder.py', 'material_definition.py']
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('baca.materials.testnotes')


#def test_MaterialPackageWrangler_run_handmade_package_02():
#    '''Make data package. Corrupt initializer.
#    Verify faulty initializer. Remove package.
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes incanned canned_exception.py default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert     mpp.directory_contents == ['__init__.py', 'material_definition.py']
#        assert     mpp.has_faulty_initializer
#        assert not mpp.has_faulty_output_material_module
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')
#
#
#def test_MaterialPackageWrangler_run_handmade_package_03():
#    '''Make data package. Corrupt initializer. Restore initializer.
#    Verify nonfaulty initializer. Remove package.
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes incanned canned_exception.py default '
#            'inr yes no default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert     mpp.directory_contents == ['__init__.py', 'material_definition.py']
#        assert not mpp.has_faulty_initializer
#        assert not mpp.has_faulty_output_material_module
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')
#
#
#def test_MaterialPackageWrangler_run_handmade_package_04():
#    '''Make data package. Create output material.
#    Delete package." 
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes mdcanned canned_testnotes_material_definition.py default '
#            'omm default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        # TODO: add more assets like the following
#        assert baca.materials.testnotes == [1, 2, 3, 4, 5]
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'output_material.py']
#        assert mpp.has_material_definition
#        assert mpp.has_material_definition_module
#        assert mpp.has_output_material
#        assert mpp.has_output_material_module
#        assert mpp.is_data_only
#        assert mpp.is_handmade
#        assert mpp.material_definition == [1, 2, 3, 4, 5]
#        assert mpp.output_material == [1, 2, 3, 4, 5]
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')
#
#
#def test_MaterialPackageWrangler_run_handmade_package_05():
#    '''Make data package. Delete material definition module.
#    Remove package.
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes mddelete default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert mpp.directory_contents == ['__init__.py']
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')
#
#
#def test_MaterialPackageWrangler_run_handmade_package_06():
#    '''Make data package. Overwrite material definition module with stub.
#    Delete package.
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes mdstub default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')
#
#
#def test_MaterialPackageWrangler_run_handmade_package_07():
#    '''Make data package. Copy canned material definition. Make output material. Remove output material.
#    Remove package.
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes mdcanned canned_testnotes_material_definition.py default '
#            'omm default '
#            'omdelete default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
#        assert not mpp.initializer_file_proxy.has_safe_import('output_material', 'testnotes')
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')
#
#
#def test_MaterialPackageWrangler_run_handmade_package_08():
#    '''Make data package. Copy canned material definition with exception.
#    Examine package state. Remove package.
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes mdcanned canned_testnotes_material_definition_with_exception.py default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert mpp.directory_contents == ['__init__.py', 'material_definition.py']
#        assert mpp.has_faulty_material_definition_module
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')
#
#
#def test_MaterialPackageWrangler_run_handmade_package_09():
#    '''Make data package. Copy canned material definition module. Make output data. Corrupt output data.
#    Verify faulty output material module. Remove package.
#    '''
#
#    studio = baca.scf.Studio()
#    assert not studio.package_exists('baca.materials.testnotes')
#
#    try:
#        studio.run(user_input=
#            'm h testnotes default default '
#            'testnotes mdcanned canned_testnotes_material_definition.py default '
#            'omm default '
#            'omcanned canned_exception.py default q')
#        assert studio.package_exists('baca.materials.testnotes')
#        mpp = baca.scf.MaterialPackageProxy('baca.materials.testnotes')
#        assert     mpp.directory_contents == ['__init__.py', 'material_definition.py', 'output_material.py']
#        assert not mpp.has_faulty_material_definition_module
#        assert     mpp.has_faulty_output_material_module
#    finally:
#        studio.run(user_input='m testnotes del remove default q')
#        assert not studio.package_exists('baca.materials.testnotes')

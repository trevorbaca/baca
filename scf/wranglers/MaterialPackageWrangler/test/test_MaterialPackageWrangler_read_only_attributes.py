from abjad.tools import iotools
import baca


def test_MaterialPackageWrangler_read_only_attributes_01():

    mpw = baca.scf.wranglers.MaterialPackageWrangler()
    
    assert mpw.breadcrumb == 'materials'
    assert isinstance(mpw.material_package_maker_wrangler, baca.scf.wranglers.MaterialPackageMakerWrangler)

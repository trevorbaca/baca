from abjad.tools import iotools
import baca


def test_MaterialPackageWrangler_read_only_attributes_01():

    mpw = baca.scf.MaterialPackageWrangler()
    
    assert mpw.breadcrumb == 'materials'
    assert isinstance(mpw.material_proxy_wrangler, baca.scf.MaterialPackageMakerWrangler)

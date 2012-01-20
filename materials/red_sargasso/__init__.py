from baca.scf.helpers import safe_import
from collections import OrderedDict

safe_import(globals(), 'output_material', 'red_sargasso')


tags = OrderedDict([
    ('material_package_maker_class_name', 'SargassoMeasureMaterialPackageMaker'),
    ('should_have_illustration', True)])

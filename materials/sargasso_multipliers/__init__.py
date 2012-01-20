from baca.scf.helpers import safe_import
from collections import OrderedDict
safe_import(globals(), 'output_material', 'sargasso_multipliers')


tags = OrderedDict([
    ('should_have_illustration', False),
    ('material_package_maker_class_name', None)])

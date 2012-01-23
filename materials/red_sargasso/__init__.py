from baca.scf.helpers import safe_import
from collections import OrderedDict
safe_import(globals(), 'output_material', 'red_sargasso')
#from output_material import red_sargasso


tags = OrderedDict([
    ('user_input_handler_class_name', 'SargassoMeasureMaterialProxy'),
    ('should_have_illustration', True)])

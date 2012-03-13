from scf.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class KaleidClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###
    
    asset_container_package_importable_names = ['handlers.kaleids']
    asset_container_path_names = [os.path.join(os.environ.get('HANDLERS'), 'kaleids')]
    target_human_readable_name = 'kaleid class name'

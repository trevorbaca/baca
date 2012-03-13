from scf.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class DynamicHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = ['dynamics']
    asset_container_path_names = [os.environ.get('DYNAMICHANDLERSPATH')]
    target_human_readable_name = 'dynamic handler class name'

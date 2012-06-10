from scf.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class DynamicHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = ['handlertools.dynamics']
    asset_container_path_names = [os.path.join(os.environ.get('HANDLERS'), 'dynamics')]
    target_human_readable_name = 'dynamic handler class name'

    forbidden_names = (
        'DynamicHandler',
        )

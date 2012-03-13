from scf.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class ArticulationHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = ['handlers.articulations']
    asset_container_path_names = [os.path.join(os.environ.get('HANDLERS'), 'articulations')]
    target_human_readable_name = 'articulation handler class name'

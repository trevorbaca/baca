from scf.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class TimeTokenMakerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###
    
    asset_container_package_importable_names = ['abjad.tools.timetokentools']
    asset_container_path_names = [os.path.join(os.environ.get('ABJAD'), 'tools', 'timetokentools')]
    target_human_readable_name = 'time-token maker class name'

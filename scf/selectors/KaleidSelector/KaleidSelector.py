from scf.selectors.DirectoryContentSelector import DirectoryContentSelector
import os


class KaleidSelector(DirectoryContentSelector):

    ### CLASS ATTRIBUTES ###
    
    asset_container_package_importable_names = ['kaleids']
    asset_container_path_names = [os.environ.get('KALEIDPATH')]
    target_human_readable_name = 'kaleid'

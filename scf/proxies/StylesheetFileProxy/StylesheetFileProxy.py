from abjad.tools import iotools
from scf.proxies.FileProxy import FileProxy
import os


class StylesheetFileProxy(FileProxy):

    ### CLASS ATTRIBUTES ###

    extension = '.ly'
    generic_class_name = 'stylesheet'
    temporary_asset_short_name = 'temporary_stylesheet.ly'

    ### PUBLIC METHODS ###

    # TODO: implement later
    def audit_stylesheet(self):
        self.print_not_yet_implemented()

    def fix(self):
        self.print_not_yet_implemented()
        
    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'audit':
            self.audit_stylesheet()
        elif result == 'cp':
            self.copy_interactively()
        elif result == 'rm':
            self.remove_interactively()
            self.session.is_backtracking_locally = True
        elif result == 'ren':
            self.rename_interactively()
        elif result == 'vi':
            self.edit()
        else:
            raise ValueError

    def human_readable_name_to_asset_short_name(self, human_readable_name):
        asset_short_name = FileProxy.human_readable_name_to_asset_short_name(self, human_readable_name)
        if not asset_short_name.endswith(self.extension):
            asset_short_name += self.extension
        return asset_short_name

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where)
        section.append(('audit', 'audit stylesheet'))
        section.append(('cp', 'copy stylesheet'))
        section.append(('rm', 'delete stylesheet'))
        section.append(('ren', 'rename stylesheet'))
        section.append(('vi', 'vi stylesheet'))
        return menu

    # TODO: rename to rename_interactively() and subclass AssetProxy.rename_interactively()
    # TODO: implement rename() to subclass AssetProxy.renam()
    def rename_stylesheet_interactively(self, prompt=True):
        getter = self.make_getter()
        getter.append_string('new file name')
        new_short_name = getter.run()
        if self.backtrack():
            return
        new_short_name = iotools.string_to_strict_directory_name(new_short_name)
        if not new_short_name.endswith('.ly'):
            new_short_name = new_short_name + '.ly'
        new_path_name = os.path.join(self.parent_directory_name, new_short_name)
        self.rename(new_path_name)
        line = 'stylesheet renamed.'
        self.proceed(line, prompt=prompt)

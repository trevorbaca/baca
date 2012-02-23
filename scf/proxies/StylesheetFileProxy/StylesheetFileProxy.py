from abjad.tools import iotools
from baca.scf.proxies.FileProxy import FileProxy
import os


class StylesheetFileProxy(FileProxy):

    def __init__(self, path_name, session=None):
        FileProxy.__init__(self, path_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.short_name

    @property
    def temporary_asset_short_name(self):
        return '__temporary_stylesheet.ly'

    ### PUBLIC METHODS ###

    # TODO: implement
    def audit_stylesheet(self):
        self.print_not_implemented()

    def copy_stylesheet_interactively(self, prompt=True):
        getter = self.make_getter()
        getter.append_string('new file name')
        new_short_name = getter.run()
        if self.backtrack():
            return
        new_short_name = iotools.string_to_strict_directory_name(new_short_name)
        if not new_short_name.endswith('.ly'):
            new_short_name = new_short_name + '.ly'
        new_path_name = os.path.join(self.parent_directory_name, new_short_name)
        self.copy_file(new_path_name)
        line = 'file copied.'
        self.proceed(line, prompt=prompt)

    def fix(self):
        self.print_not_implemented()
        
    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'audit':
            self.audit_stylesheet()
        elif result == 'cp':
            self.copy_stylesheet_interactively()
        elif result == 'del':
            self.remove_stylesheet_interactively()
            self.session.is_backtracking_locally = True
        elif result == 'ren':
            self.rename_stylesheet_interactively()
        elif result == 'vi':
            self.edit()
        else:
            raise ValueError

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where)
        section.append(('audit', 'audit stylesheet'))
        section.append(('cp', 'copy stylesheet'))
        section.append(('del', 'delete stylesheet'))
        section.append(('ren', 'rename stylesheet'))
        section.append(('vi', 'vi stylesheet'))
        return menu

    def remove_stylesheet_interactively(self, prompt=True):
        self.remove()
        line = 'stylesheet deleted.'
        self.proceed(line, prompt=prompt)

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
        self.rename_file(new_path_name)
        line = 'stylesheet renamed.'
        self.proceed(line, prompt=prompt)

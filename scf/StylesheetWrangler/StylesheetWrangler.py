from abjad.tools import iotools
from baca.scf.PackageWrangler import PackageWrangler
from baca.scf.StylesheetFileProxy import StylesheetFileProxy
import os


class StylesheetWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, self.stylesheets_package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'stylesheets'

    # TODO: write test
    @property
    def stylesheet_file_names(self):
        result = []
        for file_name in os.listdir(self.stylesheets_directory):
            if file_name.endswith('.ly'):
                result.append(file_name)
        return result

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_new_stylesheet_interactively()
        else:
            stylesheet_file_name = os.path.join(self.stylesheets_directory, result)  
            stylesheet_proxy = StylesheetFileProxy(stylesheet_file_name, session=self.session)
            stylesheet_proxy.run()
         
    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.stylesheet_file_names
        section = menu.make_new_section()
        section.append(('new', 'make new stylesheet'))
        return menu

    # TODO: write test
    def make_new_stylesheet_interactively(self):
        getter = self.make_new_getter()
        getter.append_string('stylesheet name')
        stylesheet_name = getter.run()
        if self.backtrack():
            return
        stylesheet_name = iotools.string_to_strict_directory_name(stylesheet_name)
        if not stylesheet_name.endswith('.ly'):
            stylesheet_name = stylesheet_name + '.ly'
        stylesheet_file_name = os.path.join(self.stylesheets_directory, stylesheet_name)
        #self.edit_stylesheet(stylesheet_file_name)
        stylesheet_proxy = StylesheetFileProxy(stylesheet_file_name, session=self.session)
        stylesheet_proxy.edit_stylesheet()

    def run(self, user_input=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        
    # TODO: write test
    def select_stylesheet_file_name_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.stylesheet_file_names
        while True:
            self.push_breadcrumb('select stylesheet')
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                self.pop_breadcrumb()
                break
        self.restore_breadcrumbs(cache=cache)
        result = os.path.join(self.stylesheets_directory, result)
        return result

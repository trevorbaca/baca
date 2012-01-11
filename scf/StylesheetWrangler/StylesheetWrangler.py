from abjad.tools import iotools
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.StylesheetProxy import StylesheetProxy
import os


class StylesheetWrangler(DirectoryProxy):

    def __init__(self, session=None):
        directory_name = self.stylesheets_directory
        DirectoryProxy.__init__(self, directory_name=directory_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'stylesheets'

    ### PUBLIC METHODS ###

    # TODO: write test
    def create_new_stylesheet_interactively(self):
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
        stylesheet_proxy = StylesheetProxy(stylesheet_file_name, session=self.session)
        stylesheet_proxy.edit_stylesheet()

#    def edit_stylesheet(self, stylesheet_file_name):
#        os.system('vi {}'.format(stylesheet_file_name))

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.create_new_stylesheet_interactively()
        else:
            stylesheet_file_name = os.path.join(self.stylesheets_directory, result)  
            #self.edit_stylesheet(stylesheet_file_name)
            stylesheet_proxy = StylesheetProxy(stylesheet_file_name, session=self.session)
            stylesheet_proxy.run()
         
    # TODO: write test
    def list_stylesheet_file_names(self):
        result = []
        for file_name in os.listdir(self.stylesheets_directory):
            if file_name.endswith('.ly'):
                result.append(file_name)
        return result

    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_stylesheet_file_names()
        section = menu.make_new_section()
        section.append(('new', 'make new stylesheet'))
        return menu

    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        while True:
            self.append_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run()
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
        
    # TODO: write test
    def select_stylesheet_file_name_interactively(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_stylesheet_file_names()
        while True:
            self.append_breadcrumb('select stylesheet')
            result = menu.run()
            if self.backtrack():
                self.pop_breadcrumb()
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                self.pop_breadcrumb()
                break
        result = os.path.join(self.stylesheets_directory, result)
        return result

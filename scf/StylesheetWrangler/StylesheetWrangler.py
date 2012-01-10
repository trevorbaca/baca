from baca.scf.DirectoryProxy import DirectoryProxy
import os


class StylesheetWrangler(DirectoryProxy):

    def __init__(self, session=None):
        #directory_name = '/Users/trevorbaca/Documents/other/baca/scf/stylesheets'
        directory_name = self.stylesheets_directory
        DirectoryProxy.__init__(self, directory_name=directory_name, session=session)
        #self._score_wrangler = ScoreWrangler(session=self.session)

#    ### READ-ONLY PUBLIC ATTRIBUTES ###
#
#    @property   
#    def score_wrangler(self):
#        return self._score_wrangler

    ### PUBLIC METHODS ###

    # TODO: write test
    def list_stylesheet_file_names(self):
        result = []
        for file_name in os.listdir(self.stylesheets_directory):
            if file_name.endswith('.ly'):
                result.append(file_name)
        return result
        
    # TODO: write test
    def select_stylesheet_file_name_interactively(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.menu_entry_tokens = self.list_stylesheet_file_names()
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

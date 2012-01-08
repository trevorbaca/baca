from baca.scf.PackageWrangler import PackageWrangler
import os


class StylesheetWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, session=session)
        self._score_wrangler = ScoreWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property   
    def score_wrangler(self):
        return self._score_wrangler

    ### PUBLIC METHODS ###

    # TODO: write test
    def list_stylesheet_file_names(self):
        result = []
        for file_name in os.listdir(self.stylesheets_directory):
            result.extend(file_name)
        return result
        
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
        return result

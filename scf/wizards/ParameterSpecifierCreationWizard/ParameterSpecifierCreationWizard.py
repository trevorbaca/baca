from scf import selectors
from scf.wizards.Wizard import Wizard


class ParameterSpecifierCreationWizard(Wizard):

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'parameter specifier creation wizard'

    ### PUBLIC METHODS ###

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        selector = selectors.ParameterEditorClassNameSelector(session=self.session)
        self.push_backtrack()
        editor_class_name = selector.run()
        self.pop_backtrack()
        if self.backtrack():
            self.pop_breadcrumb()
            self.restore_breadcrumbs(cache=cache)
            return
        command = 'from scf.editors import {} as editor_class'.format(editor_class_name)
        exec(command)
        editor = editor_class(session=self.session)
        self.push_backtrack()
        editor.run()
        self.pop_backtrack()
        if self.backtrack():
            self.pop_breadcrumb()
            self.restore_breadcrumbs(cache=cache)
            return
        self.target = editor.target
        return self.target

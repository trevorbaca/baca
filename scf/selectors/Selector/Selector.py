from scf.core.SCFObject import SCFObject


class Selector(SCFObject):

    def __init__(self, items=None, session=None):
        SCFObject.__init__(self, session=session) 
        self.items = items or []

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        if hasattr(self, 'target_human_readable_name'):
            return 'select {}:'.format(self.target_human_readable_name)
        else:
            return 'select:'

    ### READ / WRITE ATTRIBUTES ###

    @apply
    def items():
        def fget(self):
            return self._items
        def fset(self, items):
            self._items = items
        return property(**locals())

    ### PUBLIC METHODS ###

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True, is_keyed=False)
        section.tokens = self.make_menu_tokens(head=head)
        section.return_value_attribute = 'prepopulated'
        return menu

    def make_menu_tokens(self, head=None):
        return [self.change_expr_to_menu_token(item) for item in self.items]

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu(head=head)
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                break
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return result

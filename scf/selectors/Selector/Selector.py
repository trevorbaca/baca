from abc import ABCMeta
from abc import abstractmethod
from scf.core.SCFObject import SCFObject


class Selector(SCFObject):
    __metaclass__ = ABCMeta

    def __init__(self, session=None):
        SCFObject.__init__(self, session=session) 

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        if hasattr(self, 'target_human_readable_name'):
            return 'select {}:'.format(self.target_human_readable_name)
        else:
            return 'select:'

    ### PUBLIC METHODS ###

    @abstractmethod
    def make_menu_tokens(self, head=None):
        pass

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True, is_keyed=False)
        section.tokens = self.make_menu_tokens(head=head)
        assert section.has_prepopulated_return_value_tuple_tokens, self
        section.return_value_attribute = 'prepopulated'
        return menu

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

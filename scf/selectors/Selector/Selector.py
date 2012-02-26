from abc import ABCMeta
from abc import abstractmethod
from scf.core.SCFObject import SCFObject


class Selector(SCFObject):
    __metaclass__ = ABCMeta

    def __init__(self, session=None):
        SCFObject.__init__(self, session=session) 

    ### PUBLIC METHODS ###

    @abstractmethod
    def handle_main_menu_result(self, result):
        pass

    @abstractmethod
    def make_main_menu(self):
        pass

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
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

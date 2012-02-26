from scf.editors.InteractiveEditor import InteractiveEditor
from scf.selectors.Selector import Selector
import types


class AttributeDetail(object):

    def __init__(self, name, menu_key, editor_callable, allow_none=True):
        self.name = name
        self.menu_key = menu_key
        self.editor_callable = editor_callable
        self.allow_none = allow_none

    ### OVERLOADS ###

    def __repr__(self):
        parts = [repr(self.name), repr(self.menu_key), self.editor_callable.__name__]
        if not self.allow_none:
            parts.append('allow_none=False')
        parts = ', '.join(parts)
        return '{}({})'.format(type(self).__name__, parts)

    ### PUBLIC METHODS ###

    def get_editor(self, attribute_spaced_name, existing_value, session=None):
        if isinstance(self.editor_callable, types.FunctionType):
            editor = self.editor_callable(attribute_spaced_name, 
                session=session, existing_value=existing_value, allow_none=self.allow_none)
        #elif isinstance(self.editor_callable, types.TypeType):
        elif isinstance(self.editor_callable, InteractiveEditor):
            editor = self.editor_callable(session=session, target=existing_value)
        elif isinstance(self.editor_callable, Selector):
            editor = self.editor_callable(session=session) 
        else:
            raise ValueError
        return editor

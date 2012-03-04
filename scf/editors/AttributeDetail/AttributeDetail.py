from scf.editors.InteractiveEditor import InteractiveEditor
from scf.selectors.Selector import Selector
import types


class AttributeDetail(object):

    def __init__(self, *args, **kwargs):
        is_null = False
        if len(args) == 0:
            name = human_readable_name = menu_key = editor_callable = is_mandatory = None
            is_null = True
        elif len(args) == 3:
            name, menu_key, editor_callable = args
            #human_readable_name = name.replace('_', ' ')
            human_readable_name = None
            is_mandatory = True
        elif len(args) == 4:
            name, human_readable_name, menu_key, editor_callable = args
            is_mandatory = True
        elif len(args) == 5:
            name, human_readable_name, menu_key, editor_callable, is_mandatory = args
        else:
            raise ValueError('can not parse attribute detail {!r}.'.format(args)) 
        if not human_readable_name and name:
            human_readable_name = name.replace('_', ' ')
        self.name = name
        self.human_readable_name = human_readable_name 
        self.menu_key = menu_key
        self.editor_callable = editor_callable
        self.is_mandatory = is_mandatory
        self.allow_none = kwargs.get('allow_none', True)
        self.is_null = is_null

    ### OVERLOADS ###

    def __repr__(self):
        parts = [repr(self.human_readable_name), repr(self.menu_key), self.editor_callable.__name__]
        if not self.allow_none:
            parts.append('allow_none=False')
        parts = ', '.join(parts)
        return '{}({})'.format(type(self).__name__, parts)

    ### PUBLIC METHODS ###

    def get_editor(self, attribute_spaced_name, existing_value, session=None, **kwargs):
        if isinstance(self.editor_callable, types.FunctionType):
            editor = self.editor_callable(attribute_spaced_name, 
                session=session, existing_value=existing_value, allow_none=self.allow_none, **kwargs)
        elif issubclass(self.editor_callable, InteractiveEditor):
            editor = self.editor_callable(session=session, target=existing_value, **kwargs)
        elif issubclass(self.editor_callable, Selector):
            editor = self.editor_callable(session=session, **kwargs) 
        else:
            raise ValueError('what is {!r}?'.format(self.editor_callable))
        return editor

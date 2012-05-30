from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Scope import Scope
from baca.specification.Selection import Selection
import copy


class Setting(AbjadObject):

    ### CLASS ATTRIBUTES ###

    initializer_attribute_names = (
        'segment_name', 'context_name', 'scope', 'attribute_name', 'source', 
        'persistent', 'fresh', 'value',
        )

    ### INITIALIZER ###

    def __init__(self, segment_name, context_name, scope, attribute_name, source, persistent, 
        fresh=True, value=None):
        assert isinstance(segment_name, str), segment_name
        assert isinstance(context_name, (str, type(None))), context_name
        assert isinstance(attribute_name, str), attribute_name
        assert isinstance(persistent, bool), persistent
        assert isinstance(scope, (Scope, type(None))), scope
        assert isinstance(fresh, type(True)), fresh
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
        self.attribute_name = attribute_name
        self.source = source
        self.persistent = persistent
        self.fresh = fresh
        self.value = value

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        body = [
            self._one_line_target_format,
            self._get_one_line_source_format(self.source),
            ]
        if self.value is not None:
            body.append(self._get_one_line_source_format(self.value))
        if not self.persistent:
            body.append(self.persistent)
        body = ', '.join([str(x) for x in body])
        return '{}: {}'.format(self.attribute_name, body)

    @property
    def _one_line_target_format(self):
        body = []
        for attribute_name in ('segment_name', 'context_name', 'scope'):
            attribute_value = getattr(self, attribute_name, None)
            if attribute_value is not None:
                body.append(attribute_value)
        body = ', '.join(body)
        return '({})'.format(body)

    ### PRIVATE METHODS ###

    def _get_one_line_source_format(self, source):
        if hasattr(source, '_one_line_format'):
            return source._one_line_format
        elif hasattr(source, 'name'):
            return source.name
        else:
            return str(source)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_absolute(self):
        return not self.is_relative

    @property
    def is_relative(self):
        return isinstance(self.source, Selection)

    ### PUBLIC METHODS ###

    def copy(self, segment_name=None, context_name=None, scope=None, attribute_name=None, 
        source=None, persistent=None, fresh=None, value=None):
        new = copy.deepcopy(self)
        for name in self.initializer_attribute_names:
            if locals()[name] is not None:
                setattr(new, name, locals()[name])
        return new

from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Scope import Scope
from baca.specification.Selection import Selection


class Setting(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, segment_name, context_name, scope, attribute_name, source, persistent, fresh=True):
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        body = [
            self._one_line_target_format,
            self._get_one_line_source_format(self.source),
            ]
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

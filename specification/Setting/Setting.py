from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Scope import Scope
from baca.specification.Selection import Selection


class Setting(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        values = self._get_mandatory_argument_values(*args)
        segment_name, context_name, scope, attribute_name, source, persistent, truncate = values
        fresh = kwargs.get('fresh', True)
        assert isinstance(segment_name, str), segment_name
        assert isinstance(context_name, (str, type(None))), context_name
        assert isinstance(scope, (Scope, type(None))), scope
        assert isinstance(attribute_name, str), attribute_name
        assert isinstance(persistent, bool), persistent
        assert isinstance(truncate, bool), truncate
        assert isinstance(fresh, type(True)), fresh
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
        self.attribute_name = attribute_name
        self.source = source
        self.persistent = persistent
        self.truncate = truncate
        self.fresh = fresh

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return (
            'fresh',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            self.segment_name,
            self.context_name,
            self.scope,
            self.attribute_name,
            self.source,
            self.persistent,
            self.truncate,
            )

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

    def _get_mandatory_argument_values(self, *args):
        if len(args) == 1:
            assert isinstance(args[0], type(self)), repr(args[0])
            return args[0]._mandatory_argument_values
        else:
            assert len(args) == 7, repr(args)
            return args

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

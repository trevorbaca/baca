# -*- coding: utf-8 -*-
import abjad


# TODO: write examples
class OverrideSpecifier(abjad.abctools.AbjadObject):
    r'''Override specifier.
    
    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.OverrideSpecifier()
            OverrideSpecifier()

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_attribute_name',
        '_attribute_value',
        '_context_name',
        '_grob_name',
        '_maximum_settings',
        '_maximum_written_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        context_name=None,
        grob_name=None, 
        attribute_name=None,
        attribute_value=None,
        maximum_written_duration=None,
        maximum_settings=None,
        ):
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        self._context_name = context_name
        if grob_name is not None:
            assert isinstance(grob_name, str), repr(grob_name)
        self._grob_name = grob_name
        if attribute_name is not None:
            assert isinstance(attribute_name, str), repr(attribute_name)
        self._attribute_name = attribute_name
        self._attribute_value = attribute_value
        if maximum_written_duration is not None:
            maximum_written_duration = abjad.durationtools.Duration(
                maximum_written_duration)
        self._maximum_written_duration = maximum_written_duration
        if maximum_settings is not None:
            assert isinstance(maximum_settings, dict), maximum_settings
        self._maximum_settings = maximum_settings

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls specifier.

        Returns none.
        '''
        leaves = abjad.iterate(expr).by_leaf()
        # TODO: use named string format fields
        if self.context_name is not None:
            statement = 'abjad.override(leaf).{}.{}.{} = {}'
            statement = statement.format(
                self.context_name,
                self.grob_name,
                self.attribute_name,
                self.attribute_value,
                )
        else:
            statement = 'abjad.override(leaf).{}.{} = {}'
            statement = statement.format(
                self.grob_name,
                self.attribute_name,
                self.attribute_value,
                )
        if self.maximum_written_duration is not None:
            maximum_statement = 'abjad.override(leaf).{}.{} = {}'
            maximum_statement = maximum_statement.format(
                self.maximum_settings['grob_name'],
                self.maximum_settings['attribute_name'],
                self.maximum_settings['attribute_value'],
                )
        for leaf in leaves:
            if self.maximum_written_duration is not None:
                if self.maximum_written_duration <= leaf.written_duration:
                    if maximum_statement is not None:
                        exec(maximum_statement, globals(), locals())
                    continue
            exec(statement, globals(), locals())

    ### PUBLIC PROPERTIES ###

    @property
    def attribute_name(self):
        r'''Gets attribute name.

        Set to string or none.
        '''
        return self._attribute_name

    @property
    def attribute_value(self):
        r'''Gets attribute value.

        Set to string or none.
        '''
        return self._attribute_value

    @property
    def context_name(self):
        r'''Gets context name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return self._context_name

    @property
    def grob_name(self):
        r'''Gets grob name.

        Set to string or none.
        '''
        return self._grob_name

    @property
    def maximum_settings(self):
        r'''Gets maximum settings for leaves with written duration
        greater than or equal to maximum written duration of specifier.

        ..  todo: Write examples and tests.

        Set to dictionary or none.
        '''
        return self._maximum_settings

    @property
    def maximum_written_duration(self):
        r'''Gets maximum written duration.

        Written durations equal to or greater than this will
        not be handled.

        Set to duration or none.
        '''
        return self._maximum_written_duration

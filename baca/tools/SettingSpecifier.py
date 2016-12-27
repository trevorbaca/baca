# -*- coding: utf-8 -*-
import abjad


# TODO: write examples
class SettingSpecifier(abjad.abctools.AbjadObject):
    r'''Setting specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.SettingSpecifier()
            SettingSpecifier()

    '''

    ### CLASS settingS ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_context_name',
        '_selector',
        '_setting_name',
        '_setting_value',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        context_name=None,
        selector=None,
        setting_name=None,
        setting_value=None,
        ):
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        self._context_name = context_name
        if selector is not None:
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector
        if setting_name is not None:
            assert isinstance(setting_name, str), repr(setting_name)
        self._setting_name = setting_name
        self._setting_value = setting_value

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls specifier on `expr`.

        Returns none.
        '''
        # TODO: use named string format fields
        if self.context_name is not None:
            statement = 'abjad.set_(item).{}.{} = {!r}'
            statement = statement.format(
                self.context_name,
                self.setting_name,
                self.setting_value,
                )
        else:
            statement = 'abjad.set_(item).{} = {!r}'
            statement = statement.format(
                self.setting_name,
                self.setting_value,
                )
        selector = self._get_selector()
        items = selector(expr)
        globals_ = globals()
        globals_.update(abjad.__dict__.copy())
        globals_['SchemeMoment'] = abjad.schemetools.SchemeMoment
        for item in items:
            exec(statement, globals_, locals())

    ### PRIVATE METHODS ###

    def _get_selector(self):
        if self.selector is None:
            return abjad.select().by_leaf(flatten=True)
        return self.selector

    ### PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        r'''Gets context name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return self._context_name

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def setting_name(self):
        r'''Gets setting name.

        Set to string or none.
        '''
        return self._setting_name

    @property
    def setting_value(self):
        r'''Gets setting value.

        Set to string or none.
        '''
        return self._setting_value

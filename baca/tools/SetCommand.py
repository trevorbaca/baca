import abjad
import baca
from .Command import Command


# TODO: write examples
class SetCommand(Command):
    r'''Set command.

    ..  container:: example

        ::

            >>> baca.SetCommand()
            SetCommand()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

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
            assert isinstance(selector, abjad.Selector)
        self._selector = selector
        if setting_name is not None:
            assert isinstance(setting_name, str), repr(setting_name)
        self._setting_name = setting_name
        self._setting_value = setting_value

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        context = self.context_name
        setting = self.setting_name
        value = self.setting_value
        if self.context_name is not None:
            statement = f'abjad.setting(item).{context}.{setting} = {value!r}'
        else:
            statement = 'abjad.setting(item).{setting} = {value!r}'
        globals_ = globals()
        globals_.update(abjad.__dict__.copy())
        globals_['SchemeMoment'] = abjad.SchemeMoment
        selector = self.selector or baca.select_leaf(0)
        selections = selector(argument)
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            for item in selection:
                exec(statement, globals_, locals())

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

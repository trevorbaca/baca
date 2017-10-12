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

    __slots__ = (
        '_context_name',
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
        target=None,
        ):
        Command.__init__(self, selector=selector, target=target)
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        self._context_name = context_name
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
        if self.selector is not None:
            argument = self.selector(argument)
        selections = baca.MusicMaker._normalize_selections(argument)
        if self.target is not None:
            selections = [self.target(_) for _ in selections]
        selections = baca.MusicMaker._normalize_selections(selections)
        context = self.context_name
        setting = self.setting_name
        value = self.setting_value
        if self.context_name is not None:
            statement = f'abjad.setting(item).{context}.{setting} = {value!r}'
        else:
            statement = f'abjad.setting(item).{setting} = {value!r}'
        globals_ = globals()
        globals_.update(abjad.__dict__.copy())
        globals_['SchemeMoment'] = abjad.SchemeMoment
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

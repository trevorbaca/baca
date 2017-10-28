import abjad
import baca
from .Command import Command


class SettingCommand(Command):
    r'''Set command.

    ..  container:: example

        ::

            >>> baca.SettingCommand()
            SettingCommand()

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
        ):
        Command.__init__(self, selector=selector)
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        self._context_name = context_name
        if setting_name is not None:
            assert isinstance(setting_name, str), repr(setting_name)
        self._setting_name = setting_name
        self._setting_value = setting_value

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls command on `music`.

        Returns none.
        '''
        selections = self._select(music)
        for selection in selections:
            context = self.context_name
            setting = self.setting_name
            value = self.setting_value
            if self.context_name is not None:
                string = f'abjad.setting(leaf).{context}.{setting} = {value!r}'
            else:
                string = f'abjad.setting(leaf).{setting} = {value!r}'
            globals_ = globals()
            globals_.update(abjad.__dict__.copy())
            for leaf in abjad.iterate(selection).leaves():
                exec(string, globals_, locals())

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

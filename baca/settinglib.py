import abjad
from .Command import Command


### CLASSES ###

class SettingCommand(Command):
    """
    Setting command.

    ..  container:: example

        >>> baca.SettingCommand()
        SettingCommand(selector=baca.leaf(0))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_setting',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        context=None,
        selector='baca.leaf(0)',
        setting=None,
        value=None,
        ):
        Command.__init__(self, selector=selector)
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if setting is not None:
            assert isinstance(setting, str), repr(setting)
        self._setting = setting
        self._value = value

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if self.setting is None:
            return
        if self.value is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaf = abjad.select(argument).leaf(0)
        context = self.context
        setting = self.setting
        value = self.value
        if self.context is not None:
            string = f'abjad.setting(leaf).{context}.{setting} = {value!r}'
        else:
            string = f'abjad.setting(leaf).{setting} = {value!r}'
        globals_ = globals()
        globals_.update(abjad.__dict__.copy())
        exec(string, globals_, locals())

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        """
        Gets context name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        """
        return self._context

    @property
    def setting(self):
        """
        Gets setting name.

        Set to string or none.
        """
        return self._setting

    @property
    def value(self):
        """
        Gets setting value.

        Set to string or none.
        """
        return self._value

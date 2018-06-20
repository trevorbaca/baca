import abjad
import baca
import typing
from .Command import Command


class Suite(abjad.AbjadObject):
    """
    Suite.

    ..  container:: example

        >>> baca.Suite()
        Suite()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_manifests',
        '_offset_to_measure_number',
        '_previous_segment_voice_metadata',
        '_score_template',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *commands: typing.Union[Command, 'Suite'],
        ) -> None:
        command_list: typing.List[typing.Union[Command, Suite]] = []
        for command in commands:
            if not isinstance(command, (Command, Suite)):
                message = '\n  Commands must contain only commands.'
                message += f'\n  Not {type(command).__name__}: {command!r}.'
                raise Exception(message)
            command_list.append(command)
        self._commands = tuple(command_list)
        self._manifests = None

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies commands to ``argument``.
        """
        if argument is None:
            return
        if not self.commands:
            return
        for command in self.commands:
            command(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Tuple[typing.Union[Command, 'Suite'], ...]:
        """
        Gets commands.
        """
        return self._commands

    @property
    def manifests(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets segment-maker manifests.
        """
        return self._manifests

    @manifests.setter
    def manifests(self, argument):
        prototype = (abjad.OrderedDict, type(None))
        if argument is not None:
            assert isinstance(argument, abjad.OrderedDict), repr(argument)
        self._manifests = argument
        for command in getattr(self, 'commands', []):
            command._manifests = argument
            
    @property
    def offset_to_measure_number(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets segment-maker offset-to-measure-number dictionary.
        """
        return self._offset_to_measure_number

    @offset_to_measure_number.setter
    def offset_to_measure_number(self, dictionary):
        prototype = (dict, type(None))
        assert isinstance(dictionary, prototype), repr(dictionary)
        self._offset_to_measure_number = dictionary
        for command in getattr(self, 'commands', []):
            command._offset_to_measure_number = dictionary

    @property
    def previous_segment_voice_metadata(self) -> typing.Optional[
        abjad.OrderedDict]:
        """
        Gets previous segment voice metadata.
        """
        return self._previous_segment_voice_metadata

    @previous_segment_voice_metadata.setter
    def previous_segment_voice_metadata(self, argument):
        if argument is not None:
            assert isinstance(argument, abjad.OrderedDict), repr(argument)
        self._previous_segment_voice_metadata = argument
        for command in getattr(self, 'commands', []):
            command._previous_segment_voice_metadata = argument

    @property
    def score_template(self) -> abjad.ScoreTemplate:
        """
        Gets score template.
        """
        return self._score_template

    @score_template.setter
    def score_template(self, argument):
        if argument is not None:
            assert isinstance(argument, abjad.ScoreTemplate), repr(argument)
        self._score_template = argument
        for command in getattr(self, 'commands', []):
            command._score_template = argument

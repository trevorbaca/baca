import abjad
import baca
import typing
from .IndicatorCommand import IndicatorCommand
from .Typing import Selector


class InstrumentChangeCommand(IndicatorCommand):
    """
    Instrument change command.
    """

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container and sets part assignment.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.indicators is None:
            return
        first_leaf = abjad.inspect(argument).get_leaf(0)
        if first_leaf is not None:
            parentage = abjad.inspect(first_leaf).get_parentage()
            staff = parentage.get_first(abjad.Staff)
            instrument = self.indicators[0]
            assert isinstance(instrument, abjad.Instrument), repr(instrument)
            if not self.runtime['score_template'].allows_instrument(
                staff.name,
                instrument,
                ):
                message = f'{staff.name} does not allow instrument:\n'
                message += f'  {instrument}'
                raise Exception(message)
        super(InstrumentChangeCommand, self).__call__(argument)

import abjad
import baca
from typing import List
from typing import Tuple
from typing import Union


class WellformednessManager(abjad.AbjadObject):
    r'''Wellformedness manager.

    ..  container:: example

        >>> baca.WellformednessManager()
        WellformednessManager()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(
        self,
        argument: Union[abjad.Score, None] = None,
        ) -> List[Tuple[list, int, str]]:
        r'''Calls wellformedness checks on `argument`.

        :param argument: input score.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> manager = baca.WellformednessManager()
            >>> result = manager(voice)
            >>> for violators, total, check in result:
            ...     print(check)
            ...     print(total)
            ...     print(violators)
            ...     print()
            check_repeat_pitch_classes
            4
            [LogicalTie([Note("c'4")]), LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")]), LogicalTie([Note("d'4")])]

        Returns (violators, total, check) triples.
        '''
        triples: list = []
        if argument is None:
            return triples
        names = [_ for _ in dir(self) if _.startswith('check_')]
        for name in sorted(names):
            check = getattr(self, name)
            violators, total = check(argument=argument)
            triples.append((violators, total, name))
        return triples

    ### PRIVATE METHODS ###

    @staticmethod
    def _find_repeat_pitch_classes(argument):
        violators = []
        for voice in abjad.iterate(argument).components(abjad.Voice):
            previous_lt, previous_pcs = None, []
            for lt in abjad.iterate(voice).logical_ties():
                if isinstance(lt.head, abjad.Note):
                    written_pitches = [lt.head.written_pitch]
                elif isinstance(lt.head, abjad.Chord):
                    written_pitches = lt.head.written_pitches
                else:
                    written_pitches = []
                pcs = [_.pitch_class for _ in written_pitches]
                inspection = abjad.inspect(lt.head)
                if (inspection.has_indicator(abjad.tags.NOT_YET_PITCHED) or
                    inspection.has_indicator(abjad.tags.ALLOW_REPEAT_PITCH)):
                    pass
                elif set(pcs) & set(previous_pcs):
                    if previous_lt not in violators:
                        violators.append(previous_lt)
                    if lt not in violators:
                        violators.append(lt)
                previous_lt = lt
                previous_pcs = pcs
        return violators

    ### PUBLIC METHODS ###

    @staticmethod
    def check_repeat_pitch_classes(argument=None):
        r'''Checks repeat pitch-classes by voice.

        ..  container:: example

            Finds no repeats:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> abjad.show(voice, strict=89) # doctest: +SKIP

            >>> manager = baca.WellformednessManager
            >>> manager.check_repeat_pitch_classes(voice)
            ([], 4)

        ..  container:: example

            Finds repeat pitches:

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> abjad.show(voice, strict=89) # doctest: +SKIP

            >>> manager = baca.WellformednessManager
            >>> manager.check_repeat_pitch_classes(voice)
            ([LogicalTie([Note("c'4")]), LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")]), LogicalTie([Note("d'4")])], 4)

        ..  container:: example

            Finds repeat pitch-classes:

            >>> voice = abjad.Voice("c'4 d' e' e''")
            >>> abjad.show(voice, strict=89) # doctest: +SKIP

            >>> manager = baca.WellformednessManager
            >>> manager.check_repeat_pitch_classes(voice)
            ([LogicalTie([Note("e'4")]), LogicalTie([Note("e''4")])], 4)

        Returns violators and total.
        '''
        total = len(baca.select(argument).plts())
        violators = WellformednessManager._find_repeat_pitch_classes(argument)
        return violators, total

    def is_well_formed(self, argument=None):
        r'''Is true when `argument` is well-formed.

        ..  container:: example

            Is well-formed:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> manager = baca.WellformednessManager()
            >>> manager.is_well_formed(voice)
            True

        ..  container:: example

            Repeat pitches are not well-formed:

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> manager = baca.WellformednessManager()
            >>> manager.is_well_formed(voice)
            False

        Returns true or false.
        '''
        triples = self(argument)
        for violators, total, check_name in triples:
            if violators:
                return False
        return True

    def tabulate_wellformedness(self, argument=None):
        r'''Tabulates wellformedness violations.

        ..  container:: example

            Is well-formed:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> manager = baca.WellformednessManager()
            >>> string = manager.tabulate_wellformedness(voice)
            >>> print(string)
            0 /	4 repeat pitch classes

        ..  container:: example

            Repeat pitches are not well-formed:

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> manager = baca.WellformednessManager()
            >>> string = manager.tabulate_wellformedness(voice)
            >>> print(string)
            4 /	4 repeat pitch classes

        Returns string.
        '''
        triples = self(argument)
        strings = []
        for violators, total, check_name in triples:
            count = len(violators)
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = f'{count} /\t{total} {check_name}'
            strings.append(string)
        return '\n'.join(strings)

# -*- coding: utf-8 -*-
import abjad


class WellformednessManager(abjad.abctools.AbjadObject):
    r'''Wellformedness manager.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.WellformednessManager()
            WellformednessManager()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls wellformedness checks on `argument`.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> manager = baca.tools.WellformednessManager()
                >>> manager(staff)
                [([LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")])], 4, 'check_duplicate_pitch_classes')]

        Returns violators, total, check triples.
        '''
        if argument is None:
            return
        check_names = [x for x in dir(self) if x.startswith('check_')]
        triples = []
        for current_check_name in sorted(check_names):
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check(argument=argument)
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    ### PUBLIC METHODS ###

    @staticmethod
    def check_duplicate_pitch_classes(argument=None):
        r'''Checks duplicate pitch-classes by voice.

        ..  container:: example

            Finds no duplicates:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.tools.WellformednessManager
                >>> manager.check_duplicate_pitch_classes(staff)
                ([], 4)

        ..  container:: example

            Finds duplicate pitches:

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.tools.WellformednessManager
                >>> manager.check_duplicate_pitch_classes(staff)
                ([LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")])], 4)

        ..  container:: example

            Finds duplicate pitch-classes:

            ::

                >>> staff = Staff("c'4 d' e' e''")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.tools.WellformednessManager
                >>> manager.check_duplicate_pitch_classes(staff)
                ([LogicalTie([Note("e''4")])], 4)

        ..  container:: example

            Finds duplicate pitch-classes between sequential voices:

            ::

                >>> voice_1 = Voice("c'4 d'")
                >>> voice_2 = Voice("d''4 e''")
                >>> staff = Staff([voice_1, voice_2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \new Voice {
                        c'4
                        d'4
                    }
                    \new Voice {
                        d''4
                        e''4
                    }
                }

            ::

                >>> manager = baca.tools.WellformednessManager
                >>> manager.check_duplicate_pitch_classes(staff)
                ([LogicalTie([Note("d''4")])], 4)

        Returns violators and total.
        '''
        violators = []
        total = 0
        not_yet_pitched_string = 'not yet pitched'
        notes = abjad.iterate(argument).by_logical_tie(
            pitched=True,
            with_grace_notes=True,
            )
        notes = list(notes)
        notes.sort(
            key=lambda _: abjad.inspect_(_.head).get_timespan().start_offset)
        for leaf_1, leaf_2 in abjad.Sequence(notes).nwise():
            if not isinstance(leaf_1.head, abjad.Note):
                continue
            if not isinstance(leaf_2.head, abjad.Note):
                continue
            total += 1
            if abjad.inspect_(leaf_1.head).has_indicator(not_yet_pitched_string):
                continue
            if abjad.inspect_(leaf_2.head).has_indicator(not_yet_pitched_string):
                continue
            pitch_class_1 = leaf_1.head.written_pitch.named_pitch_class
            pitch_class_2 = leaf_2.head.written_pitch.named_pitch_class
            if not pitch_class_1 == pitch_class_2:
                continue
            string = 'repeated pitch allowed'
            if (abjad.inspect_(leaf_1.head).has_indicator(string) and
                abjad.inspect_(leaf_2.head).has_indicator(string)):
                continue
            violators.append(leaf_2)
        total += 1
        return violators, total

    def is_well_formed(self, argument=None):
        r'''Is true when `argument` is well-formed.

        ..  container:: example

            Is well-formed:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> manager = baca.tools.WellformednessManager()
                >>> manager.is_well_formed(staff)
                True
                
        ..  container:: example

            Repeated pitches are not well-formed:

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> manager = baca.tools.WellformednessManager()
                >>> manager.is_well_formed(staff)
                False

        Returns true or false.
        '''
        triples = self(argument)
        for violators, total, check_name in triples:
            if violators:
                return False
        return True

    def tabulate_well_formedness_violations(self, argument=None):
        r'''Tabulates wellformedness violations.

        ..  container:: example

            Is well-formed:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> manager = baca.tools.WellformednessManager()
                >>> string = manager.tabulate_well_formedness_violations(staff)
                >>> print(string)
                0 /	4 duplicate pitch classes

        ..  container:: example

            Repeated pitches are not well-formed:

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> manager = baca.tools.WellformednessManager()
                >>> string = manager.tabulate_well_formedness_violations(staff)
                >>> print(string)
                2 /	4 duplicate pitch classes

        Returns string.
        '''
        triples = self(argument)
        strings = []
        for violators, total, check_name in triples:
            violator_count = len(violators)
            string = '{} /\t{} {}'
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = string.format(violator_count, total, check_name)
            strings.append(string)
        return '\n'.join(strings)

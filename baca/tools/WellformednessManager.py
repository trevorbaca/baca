# -*- coding: utf-8 -*-
import abjad


class WellformednessManager(abjad.abctools.AbjadObject):
    r'''Wellformedness manager.

    ::

        >>> import baca

    ..  container:: example

        **Example.** Initializes wellformedness manager:

        ::

            >>> baca.tools.WellformednessManager()
            WellformednessManager()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### SPECIAL METHODS ###

    def __call__(self, expr=None):
        r'''Calls wellformedness checks on `expr`.

        ..  container:: example

            **Example 1.**

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> manager = baca.tools.WellformednessManager()
                >>> manager(staff)
                [([Note("c'4"), Note("d'4")], 4, 'check_duplicate_pitch_classes')]

        Returns violators, total, check triples.
        '''
        if expr is None:
            return
        check_names = [x for x in dir(self) if x.startswith('check_')]
        triples = []
        for current_check_name in sorted(check_names):
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check(expr=expr)
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    ### PUBLIC METHODS ###

    @staticmethod
    def check_duplicate_pitch_classes(expr=None):
        r'''Checks duplicate pitch-classes by voice.

        ..  container:: example

            **Example 1.** Finds no duplicates:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.tools.WellformednessManager
                >>> manager.check_duplicate_pitch_classes(staff)
                ([], 4)

        ..  container:: example

            **Example 2.** Finds duplicate pitches:

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.tools.WellformednessManager
                >>> manager.check_duplicate_pitch_classes(staff)
                ([Note("c'4"), Note("d'4")], 4)

        ..  container:: example

            **Example 3.** Finds duplicate pitch-classes:

            ::

                >>> staff = Staff("c'4 d' e' e''")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.tools.WellformednessManager
                >>> manager.check_duplicate_pitch_classes(staff)
                ([Note("e''4")], 4)

        Returns violators and total.
        '''
        violators = []
        total = 0
        leaves = abjad.iterate(expr).by_leaf()
        not_yet_pitched_string = 'not yet pitched'
        allow_repeated_pitches_string = 'allow repeated pitches'
        for leaf_1 in abjad.iterate(expr).by_leaf():
            total += 1
            if not isinstance(leaf_1, abjad.Note):
                continue
            if abjad.inspect_(leaf_1).has_indicator(not_yet_pitched_string):
                continue
            leaf_2 = abjad.inspect_(leaf_1).get_leaf(1)
            if not isinstance(leaf_2, abjad.Note):
                continue
            if abjad.inspect_(leaf_2).has_indicator(not_yet_pitched_string):
                continue
            pitch_class_1 = leaf_1.written_pitch.named_pitch_class
            pitch_class_2 = leaf_2.written_pitch.named_pitch_class
            if not pitch_class_1 == pitch_class_2:
                continue
            string = 'repeated pitch allowed'
            if (abjad.inspect_(leaf_1).has_indicator(string) and
                abjad.inspect_(leaf_2).has_indicator(string)):
                continue
            violators.append(leaf_2)
        return violators, total

    def is_well_formed(self, expr=None):
        r'''Is true when `expr` is well-formed.

        ..  container:: example

            **Example 1.** Is well-formed:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> manager = baca.tools.WellformednessManager()
                >>> manager.is_well_formed(staff)
                True
                
        ..  container:: example

            **Example 2.** Repeated pitches are not well-formed:

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> manager = baca.tools.WellformednessManager()
                >>> manager.is_well_formed(staff)
                False

        Returns true or false.
        '''
        triples = self(expr)
        for violators, total, check_name in triples:
            if violators:
                return False
        return True

    def tabulate_well_formedness_violations(self, expr=None):
        r'''Tabulates wellformedness violations.

        ..  container:: example

            **Example 1.** Is well-formed:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> manager = baca.tools.WellformednessManager()
                >>> string = manager.tabulate_well_formedness_violations(staff)
                >>> print(string)
                0 /	4 duplicate pitch classes

        ..  container:: example

            **Example 2.** Repeated pitches are not well-formed:

            ::

                >>> staff = Staff("c'4 c' d' d'")
                >>> manager = baca.tools.WellformednessManager()
                >>> string = manager.tabulate_well_formedness_violations(staff)
                >>> print(string)
                2 /	4 duplicate pitch classes

        Returns string.
        '''
        triples = self(expr)
        strings = []
        for violators, total, check_name in triples:
            violator_count = len(violators)
            string = '{} /\t{} {}'
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = string.format(violator_count, total, check_name)
            strings.append(string)
        return '\n'.join(strings)
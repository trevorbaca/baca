import abjad


class WellformednessManager(abjad.AbjadObject):
    r'''Wellformedness manager.

    ..  container:: example

        ::

            >>> baca.WellformednessManager()
            WellformednessManager()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls wellformedness checks on `argument`.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 c' d' d'")
                >>> manager = baca.WellformednessManager()
                >>> manager(staff)
                [([LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")])], 4, 'check_repeat_pitch_classes')]

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
    def check_repeat_pitch_classes(argument=None):
        r'''Checks repeat pitch-classes by voice.

        ..  container:: example

            Finds no repeats:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.WellformednessManager
                >>> manager.check_repeat_pitch_classes(staff)
                ([], 4)

        ..  container:: example

            Finds repeat pitches:

            ::

                >>> staff = abjad.Staff("c'4 c' d' d'")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.WellformednessManager
                >>> manager.check_repeat_pitch_classes(staff)
                ([LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")])], 4)

        ..  container:: example

            Finds repeat pitch-classes:

            ::

                >>> staff = abjad.Staff("c'4 d' e' e''")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> manager = baca.WellformednessManager
                >>> manager.check_repeat_pitch_classes(staff)
                ([LogicalTie([Note("e''4")])], 4)

        ..  container:: example

            Finds repeat pitch-classes between sequential voices:

            ::

                >>> voice_1 = abjad.Voice("c'4 d'")
                >>> voice_2 = abjad.Voice("d''4 e''")
                >>> staff = abjad.Staff([voice_1, voice_2])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

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

                >>> manager = baca.WellformednessManager
                >>> manager.check_repeat_pitch_classes(staff)
                ([LogicalTie([Note("d''4")])], 4)

        Returns violators and total.
        '''
        violators = []
        total = 0
        not_yet_string = 'not yet pitched'
        plts = abjad.iterate(argument).logical_ties(
            pitched=True,
            grace_notes=True,
            )
        plts = list(plts)
        plts.sort(
            key=lambda _: abjad.inspect(_.head).get_timespan().start_offset)
        for plt_1, plt_2 in abjad.Sequence(plts).nwise():
            if not isinstance(plt_1.head, abjad.Note):
                continue
            if not isinstance(plt_2.head, abjad.Note):
                continue
            total += 1
            if abjad.inspect(plt_1.head).has_indicator(not_yet_string):
                continue
            if abjad.inspect(plt_2.head).has_indicator(not_yet_string):
                continue
            pitch_class_1 = plt_1.head.written_pitch.pitch_class
            pitch_class_2 = plt_2.head.written_pitch.pitch_class
            if not pitch_class_1 == pitch_class_2:
                continue
            string = 'repeat pitch allowed'
            if (abjad.inspect(plt_1.head).has_indicator(string) and
                abjad.inspect(plt_2.head).has_indicator(string)):
                continue
            violators.append(plt_2)
        total += 1
        return violators, total

    def is_well_formed(self, argument=None):
        r'''Is true when `argument` is well-formed.

        ..  container:: example

            Is well-formed:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> manager = baca.WellformednessManager()
                >>> manager.is_well_formed(staff)
                True

        ..  container:: example

            Repeat pitches are not well-formed:

            ::

                >>> staff = abjad.Staff("c'4 c' d' d'")
                >>> manager = baca.WellformednessManager()
                >>> manager.is_well_formed(staff)
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

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> manager = baca.WellformednessManager()
                >>> string = manager.tabulate_wellformedness(staff)
                >>> print(string)
                0 /	4 repeat pitch classes

        ..  container:: example

            Repeat pitches are not well-formed:

            ::

                >>> staff = abjad.Staff("c'4 c' d' d'")
                >>> manager = baca.WellformednessManager()
                >>> string = manager.tabulate_wellformedness(staff)
                >>> print(string)
                2 /	4 repeat pitch classes

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

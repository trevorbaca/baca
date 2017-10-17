import abjad
import baca
from .Command import Command


class HairpinCommand(Command):
    r'''Hairpin command.

    ..  container:: example

        Attaches hairpin to each PLT run:

        ::

            >>> command = baca.HairpinCommand(
            ...     hairpin_tokens=['f > niente', 'niente < f'],
            ...     target=baca.select().plt_runs(),
            ...     )
            >>> string = "c'4 ~ c' ~ c' r4 d'4 ~ d' ~ d' r4"
            >>> staff = abjad.Staff(string)
            >>> command(staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \once \override Hairpin.circled-tip = ##t
                c'4 ~ \> \f
                c'4 ~
                c'4 \!
                r4
                \once \override Hairpin.circled-tip = ##t
                d'4 ~ \<
                d'4 ~
                d'4 \f
                r4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_flare',
        '_hairpin_tokens',
        '_include_rests',
        '_omit_lone_note_dynamic',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        flare=None,
        hairpin_tokens=None,
        include_rests=None,
        omit_lone_note_dynamic=None,
        selector=None,
        target='baca.select().leaves_in_trimmed_run()',
        ):
        Command.__init__(self, selector=selector, target=target)
        self._flare = flare
        hairpin_tokens = hairpin_tokens or []
        prototype = (list, tuple, abjad.CyclicTuple, abjad.Sequence,)
        assert isinstance(hairpin_tokens, prototype), repr(hairpin_tokens)
        tokens = []
        for element in hairpin_tokens:
            if isinstance(element, str):
                element = tuple(element.split())
                if not abjad.Hairpin._is_hairpin_token(element):
                    raise Exception(f'hairpin token only: {element!r}.')
            tokens.append(element)
        hairpin_tokens = tokens
        hairpin_tokens = abjad.CyclicTuple(hairpin_tokens)
        self._hairpin_tokens = hairpin_tokens
        if include_rests is not None:
            include_rests = bool(include_rests)
        self._include_rests = include_rests
        if omit_lone_note_dynamic is not None:
            omit_lone_note_dynamic = bool(omit_lone_note_dynamic)
        self._omit_lone_note_dynamic = omit_lone_note_dynamic

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if not argument:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.target is not None:
            argument = self.target(argument)
        selections = self._to_selection_list(argument)
        if False:
            print(format(selector))
            print()
            print(argument)
            print()
            print(selections)
            print()
        if not self.hairpin_tokens:
            return
        for i, selection in enumerate(selections):
            leaves = abjad.select(selection).by_leaf()
            if len(leaves) == 1:
                if self.omit_lone_note_dynamic:
                    continue
                else:
                    hairpin_token = self.hairpin_tokens[i]
                    start_dynamic = hairpin_token[0]
                    if start_dynamic == 'niente':
                        message = 'can not attach niente dynamics.'
                        raise Exception(message)
                    dynamic = abjad.Dynamic(start_dynamic)
                    abjad.attach(dynamic, leaves[0])
                    continue
            hairpin_token = self.hairpin_tokens[i]
            if hairpin_token is None:
                continue
            if isinstance(hairpin_token, tuple):
                descriptor = ' '.join([_ for _ in hairpin_token if _])
                hairpin = abjad.Hairpin(
                    descriptor=descriptor,
                    include_rests=self.include_rests,
                    )
                abjad.attach(hairpin, leaves)
            # hook to allow callable custom classes like SwellCommand
            else:
                hairpin_token(leaves)
            if self.flare:
                assert isinstance(leaves[0], abjad.Note), repr(leaves[0])
                stencil = abjad.Scheme('flared-hairpin')
                abjad.override(leaves[0]).hairpin.stencil = stencil

    ### PUBLIC PROPERTIES ###

    @property
    def flare(self):
        r'''Is true when hairpins are flared. Otherwise false.

        ..  container:: example

            Does not flare hairpins:

            ::

                >>> command = baca.HairpinCommand(
                ...     hairpin_tokens=['f > p', 'p < f'],
                ...     target=baca.select().plt_runs(),
                ...     )
                >>> string = "c'4 ~ c' ~ c' r4 d'4 ~ d' ~ d' r4"
                >>> staff = abjad.Staff(string)
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \> \f
                    c'4 ~
                    c'4 \p
                    r4
                    d'4 ~ \< \p
                    d'4 ~
                    d'4 \f
                    r4
                }

        ..  container:: example

            Does flare hairpins:

            ::

                >>> command = baca.HairpinCommand(
                ...     flare=True,
                ...     hairpin_tokens=['f > p', 'p < f'],
                ...     target=baca.select().plt_runs(),
                ...     )
                >>> string = "c'4 ~ c' ~ c' r4 d'4 ~ d' ~ d' r4"
                >>> staff = abjad.Staff(string)
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \once \override Hairpin.stencil = #flared-hairpin
                    c'4 ~ \> \f
                    c'4 ~
                    c'4 \p
                    r4
                    \once \override Hairpin.stencil = #flared-hairpin
                    d'4 ~ \< \p
                    d'4 ~
                    d'4 \f
                    r4
                }

            Note that a LilyPond bug currently prevents flared hairpins from
            working correctly with circled-tip hairpins.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._flare

    @property
    def hairpin_tokens(self):
        r'''Gets hairpin tokens of command.

        Hairpin token defined equal to triple like ``('f', '>', 'p')``,
        string like ``'f > p'`` or none.

        Set to haipin token, list of hairpin tokens or none.

        Returns cyclic tuple.
        '''
        return self._hairpin_tokens

    @property
    def include_rests(self):
        r'''Is true when hairpin includes rests.

        Returns true, false or none.
        '''
        return self._include_rests

    @property
    def omit_lone_note_dynamic(self):
        r'''Is true when start dynamic of hairpin does not attach to lone
        notes. Otherwise false.

        ..  container:: example

            Does not omit lone note dynamic:

            ::

                >>> command = baca.HairpinCommand(
                ...     hairpin_tokens=['ppp < p'],
                ...     target=baca.select().leaves_in_each_plt(),
                ...     )
                >>> string = "c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4"
                >>> staff = abjad.Staff(string)
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4 \ppp
                    g'4 \ppp
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }

        ..  container:: example

            Omits lone note dynamic:

            ::

                >>> command = baca.HairpinCommand(
                ...     hairpin_tokens=['ppp < p'],
                ...     omit_lone_note_dynamic=True,
                ...     target=baca.select().leaves_in_each_plt(),
                ...     )
                >>> string = "c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4"
                >>> staff = abjad.Staff(string)
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4
                    g'4
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._omit_lone_note_dynamic

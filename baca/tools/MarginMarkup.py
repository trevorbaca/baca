import abjad


class MarginMarkup(abjad.AbjadValueObject):
    r'''Margin markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> margin_markup = baca.MarginMarkup(
        ...     markup=abjad.Markup('Cello'),
        ...     short_markup=abjad.Markup('Vc.')
        ...     )
        >>> abjad.attach(margin_markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Cello }
                \set Staff.shortInstrumentName = \markup { Vc. }
                c'4
                d'4
                e'4
                f'4
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_context',
        '_format_slot',
        '_markup',
        '_short_markup',
        )

    _line_redraw = True

    _persistent = True

    _publish_storage_format = True

    ### INITIALIZER ##

    def __init__(
        self,
        context='Staff',
        format_slot='before',
        markup=None,
        short_markup=None,
        ):
        assert isinstance(context, str), repr(context)
        self._context = context
        assert isinstance(format_slot, str), repr(format_slot)
        self._format_slot = format_slot
        if markup is not None:
            assert isinstance(markup, abjad.Markup), repr(markup)
        self._markup = markup
        if short_markup is not None:
            assert isinstance(short_markup, abjad.Markup), repr(short_markup)
        self._short_markup = short_markup

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is margin markup with context, markup and
        short markup equal to those of this margin markup.

        ..  container:: example

            >>> margin_markup_1 = baca.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_2 = baca.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_3 = baca.MarginMarkup(
            ...     context='Staff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
            ...     )

            >>> margin_markup_1 == margin_markup_1
            True
            >>> margin_markup_1 == margin_markup_2
            True
            >>> margin_markup_1 == margin_markup_3
            False

            >>> margin_markup_2 == margin_markup_1
            True
            >>> margin_markup_2 == margin_markup_2
            True
            >>> margin_markup_2 == margin_markup_3
            False

            >>> margin_markup_3 == margin_markup_1
            False
            >>> margin_markup_3 == margin_markup_2
            False
            >>> margin_markup_3 == margin_markup_3
            True

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            return False
        if (self.context == argument.context and
            self.markup == argument.markup and
            self.short_markup == argument.short_markup):
            return True
        return False

    def __hash__(self):
        r'''Hashes margin markup.

        ..  container::

            >>> margin_markup = baca.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
            ...     )

            >>> hash_ = hash(margin_markup)
            >>> isinstance(hash_, int)
            True

        Returns integer.
        '''
        return super(MarginMarkup, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self, context=None):
        lines = []
        if context is None:
            context = self.context
        elif isinstance(context, abjad.Context):
            context = context.headword
        assert isinstance(context, str), repr(context)
        markup = format(self.markup)
        lines.append(rf'\set {context}.instrumentName = {markup}')
        short_markup = format(self.short_markup)
        lines.append(rf'\set {context}.shortInstrumentName = {short_markup}')
        return lines

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.extend(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of margin markup.

        ..  container:: example

            >>> baca.MarginMarkup().context
            'Staff'

        Returns string.
        '''
        return self._context

    @property
    def format_slot(self):
        r'''Gets format slot.

        ..  container:: example

            >>> baca.MarginMarkup().format_slot
            'before'

        Returns string.
        '''
        return self._format_slot

    @property
    def markup(self):
        r'''Gets (instrument name) markup.

        Returns markup.
        '''
        return self._markup

    @property
    def persistent(self):
        r'''Is true.

        ..  container:: example

            >>> margin_markup = baca.MarginMarkup(
            ...     markup=abjad.Markup('Cello'),
            ...     short_markup=abjad.Markup('Vc.')
            ...     )
            >>> margin_markup.persistent
            True

        Returns true.
        '''
        return self._persistent

    @property
    def short_markup(self):
        r'''Gets short (instrument name) markup.

        Returns markup.
        '''
        return self._short_markup

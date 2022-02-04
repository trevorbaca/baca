"""
Memento.
"""
import dataclasses

import abjad


class Memento:
    """
    Memento.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_context",
        "_edition",
        "_manifest",
        "_prototype",
        "_synthetic_offset",
        "_value",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        context=None,
        edition=None,
        manifest=None,
        prototype=None,
        synthetic_offset=None,
        value=None,
    ):
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        edition_ = None
        if edition is not None:
            edition_ = abjad.Tag(edition)
        self._edition = edition_
        if manifest is not None:
            assert isinstance(manifest, str), repr(manifest)
            assert prototype is None
        self._manifest = manifest
        if prototype is not None:
            assert isinstance(prototype, str), repr(prototype)
            assert manifest is None
        self._prototype = prototype
        if synthetic_offset is not None:
            assert isinstance(synthetic_offset, abjad.Offset), repr(synthetic_offset)
        self._synthetic_offset = synthetic_offset
        if value is not None:
            if not isinstance(value, (int, str, dict)):
                assert type(value).__name__ == "PersistentOverride", repr(value)
        self._value = value

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(context={self.context}, edition={self.edition}, manifest={self.manifest}, prototype={self.prototype}, synthetic_offset={self.synthetic_offset}, value={self.value})"

    ### PRIVATE METHODS###

    def _get_format_specification(self):
        return abjad.FormatSpecification()

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        """
        Gets (name of local) context.
        """
        return self._context

    @property
    def edition(self):
        """
        Gets edition.
        """
        return self._edition

    @property
    def manifest(self):
        """
        Gets manifest.
        """
        return self._manifest

    @property
    def prototype(self):
        """
        Gets prototype.
        """
        return self._prototype

    @property
    def synthetic_offset(self):
        """
        Gets synthetic offset.
        """
        return self._synthetic_offset

    @property
    def value(self):
        """
        Gets value.
        """
        return self._value


@dataclasses.dataclass(slots=True)
class PersistentOverride:
    r"""
    Persistent override.

    ..  container:: example

        >>> override = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="bar_line",
        ...     value=(-2, 0),
        ... )

        >>> override
        PersistentOverride(after=None, attribute='bar_extent', context='Staff', grob='bar_line', hide=None, value=(-2, 0))

    ..  container:: example

        >>> override_1 = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="bar_line",
        ...     value=(-2, 0),
        ... )
        >>> override_2 = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="bar_line",
        ...     value=(-2, 0),
        ... )
        >>> override_3 = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Score",
        ...     grob="bar_line",
        ...     value=(-2, 0),
        ... )

        >>> override_1 == override_1
        True
        >>> override_1 == override_2
        True
        >>> override_1 == override_3
        False

        >>> override_2 == override_1
        True
        >>> override_2 == override_2
        True
        >>> override_2 == override_3
        False

        >>> override_3 == override_1
        False
        >>> override_3 == override_2
        False
        >>> override_3 == override_3
        True

    ..  container:: example

        Formats override before leaf:

        >>> override = baca.PersistentOverride(
        ...     attribute="color",
        ...     grob="note_head",
        ...     value="red",
        ... )

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(override, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \override NoteHead.color = #red
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Formats override after leaf:

        >>> override = baca.PersistentOverride(
        ...     after=True,
        ...     attribute="color",
        ...     grob="note_head",
        ...     value="red",
        ... )

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(override, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \override NoteHead.color = #red
                d'4
                e'4
                f'4
            }

    """

    after: bool | None = None
    attribute: str | None = None
    context: str | None = None
    grob: str | None = None
    hide: bool | None = None
    value: str | None = None

    persistent = True

    def __post_init__(self):
        if self.after is not None:
            self.after = bool(self.after)
        if self.attribute is not None:
            assert isinstance(self.attribute, str), repr(self.attribute)
        if self.context is not None:
            assert isinstance(self.context, str), repr(self.context)
        if self.grob is not None:
            assert isinstance(self.grob, str), repr(self.grob)
        if self.hide is not None:
            self.hide = bool(self.hide)

    def _get_format_specification(self):
        return abjad.FormatSpecification()

    def _get_lilypond_format(self, context=None):
        if isinstance(context, abjad.Context):
            assert isinstance(context.lilypond_type, str), repr(context)
            lilypond_type = context.lilypond_type
        else:
            lilypond_type = self.context
        string = abjad.overrides.make_lilypond_override_string(
            self.grob,
            self.attribute,
            self.value,
            context=lilypond_type,
            once=False,
        )
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.hide:
            return bundle
        strings = [self._get_lilypond_format()]
        if self.after:
            bundle.after.commands.extend(strings)
        else:
            bundle.before.commands.extend(strings)
        return bundle

import abjad
import collections


class RestAffixSpecifier(abjad.AbjadValueObject):
    r'''Rest affix specifier.

    ..  container:: example

        Works together with negative-valued talea:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.RestAffixSpecifier(
        ...         prefix=[2],
        ...         suffix=[3],
        ...         ),
        ...     counts=[1, -1],
        ...     time_treatments=[1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> staff = lilypond_file[abjad.Staff]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff \with {
                \override TupletBracket.staff-padding = #4
            } <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/8 {
                            r8
                            c'16
                            r16
                            d'16
                            r16
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/10 {
                            fs''16
                            r16
                            e''16
                            r16
                            ef''16
                            r16
                            af''16
                            r16
                            g''16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5 {
                            a'16
                            r16
                            r8.
                        }
                    }
                }
            >>

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.RestAffixSpecifier(
        ...         prefix=[2],
        ...         suffix=[3],
        ...         ),
        ...     counts=[-1, 1],
        ...     time_treatments=[1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> staff = lilypond_file[abjad.Staff]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff \with {
                \override TupletBracket.staff-padding = #4
            } <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/8 {
                            r8
                            r16
                            c'16
                            r16
                            d'16
                            r16
                            bf'16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/10 {
                            r16
                            fs''16
                            r16
                            e''16
                            r16
                            ef''16
                            r16
                            af''16
                            r16
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5 {
                            r16
                            a'16
                            r8.
                        }
                    }
                }
            >>

    ..  container:: example

        >>> baca.RestAffixSpecifier()
        RestAffixSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(3) Specifiers'

    __slots__ = (
        '_pattern',
        '_prefix',
        '_skips_instead_of_rests',
        '_suffix',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        prefix=None,
        skips_instead_of_rests=None,
        suffix=None,
        ):
        if (pattern is not None and
            not isinstance(pattern, abjad.Pattern)):
            raise TypeError(f'pattern or none: {pattern!r}.')
        self._pattern = pattern
        if prefix is not None:
            assert isinstance(prefix, collections.Iterable), repr(prefix)
        self._prefix = prefix
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        if suffix is not None:
            assert isinstance(suffix, collections.Iterable), repr(suffix)
        self._suffix = suffix

    ### SPECIAL METHODS ###

    def __call__(self, collection_index=None, total_collections=None):
        r'''Calls command on `collection_index` and `total_collections`.

        ..  container:: example

            With time treatments:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(prefix=[1], suffix=[1]),
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 3/4 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 4/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            {
                                a'16
                                r16
                            }
                        }
                    }
                >>

        Returns prefix, suffix pair.
        '''
        if self.pattern is None:
            if collection_index == 0 and collection_index == total_collections - 1:
                return self.prefix, self.suffix
            if collection_index == 0:
                return self.prefix, None
            if collection_index == total_collections - 1:
                return None, self.suffix
        elif self.pattern.matches_index(collection_index, total_collections):
            return self.prefix, self.suffix
        return None, None

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            Treats entire figure when pattern is none:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 5/4 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                a'16
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats entire figure (of only one segment) when pattern is none:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[18, 16, 15, 20, 19]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/8 {
                                r16
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats first segment and last segment in figure:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/6 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                                r8
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 5/4 {
                                r16
                                a'16
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats every segment in figure:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         pattern=abjad.index_all(),
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/6 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                                r8
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/8 {
                                r16
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                                r8
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 5/4 {
                                r16
                                a'16
                                r8
                            }
                        }
                    }
                >>

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def prefix(self):
        r'''Gets prefix.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(prefix=[3]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8.
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        Set to list of positive integers or none.

        Defaults to none.

        Returns list of positive integers or none.
        '''
        return self._prefix

    @property
    def skips_instead_of_rests(self):
        r'''Is true when command makes skips instead of rests.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._skips_instead_of_rests

    @property
    def suffix(self):
        r'''Gets suffix.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(suffix=[3]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            {
                                a'16
                                r8.
                            }
                        }
                    }
                >>

        Set to list of positive integers or none.

        Defaults to none.

        Returns list of positive integers or none.
        '''
        return self._suffix

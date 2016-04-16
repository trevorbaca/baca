# -*- coding: utf-8 -*-
import copy
from abjad.tools import abctools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach


class SwellSpecifier(abctools.AbjadObject):
    r'''Swell specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** 

        ::


            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4'),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         handlertools.HairpinHandler(
            ...             hairpin_tokens=[
            ...                 baca.tools.SwellSpecifier(
            ...                     start_count=2,
            ...                     start_token='niente < p',
            ...                     stop_count=2,
            ...                     stop_token='p > niente',
            ...                     ),
            ...                 ],
            ...             span=[4, 3],
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \< [
                                e'8 \p
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \> \p
                                e'8 \! ]
                            }
                            {
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \< [
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \p \> \p
                                e'8 \! ]
                            }
                            {
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \< [
                                e'8 \p
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \> \p
                                e'8 \! ]
                            }
                            {
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \< [
                                \once \override Hairpin #'circled-tip = ##t
                                e'8 \p \> \p
                                e'8 \! ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_start_count',
        '_start_token',
        '_stop_count',
        '_stop_token',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_count=None,
        start_token=None,
        stop_count=None,
        stop_token=None,
        ):
        assert 0 < start_count, repr(start_count)
        assert isinstance(start_token, str), repr(start_token)
        assert 0 < stop_count, repr(stop_count)
        assert isinstance(stop_token, str), repr(stop_token)
        self._start_count = start_count
        self._start_token = start_token
        self._stop_count = stop_count
        self._stop_token = stop_token

    ### SPECIAL METHODS ###

    def __call__(self, leaves):
        r'''Calls swell specifier.

        Returns none.
        '''
        start_hairpin = spannertools.Hairpin(
            self.start_token,
            include_rests=True,
            )
        if len(leaves) < self.minimum_leaf_count:
            #message = 'specifier requires at least {} leaves: {!r}.'
            #message = message.format(self.minimum_leaf_count, leaves)
            #raise Exception(message)
            if len(leaves) == 0:
                return
            for leaf in leaves:
                if isinstance(leaf, (scoretools.Note, scoretools.Chord)):
                    lone_dynamic = start_hairpin.stop_dynamic
                    lone_dynamic = copy.copy(lone_dynamic)
                    attach(lone_dynamic, leaf)
                    break
            return
        start_leaves = leaves[:self.start_count]
        attach(start_hairpin, start_leaves)
        stop_hairpin = spannertools.Hairpin(
            self.stop_token,
            include_rests=True,
            )
        stop_leaves = leaves[-self.stop_count:]
        attach(stop_hairpin, stop_leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def minimum_leaf_count(self):
        r'''Gets minimum leaf count.

        Defined equal to start count + stop count - 1.

        Returns positive integer.
        '''
        return self.start_count + self.stop_count - 1

    @property
    def start_count(self):
        r'''Gets start count.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._start_count

    @property
    def start_token(self):
        r'''Gets start token.

        Set to string or none.

        Returns string or none.
        '''
        return self._start_token

    @property
    def stop_count(self):
        r'''Gets stop count.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._stop_count

    @property
    def stop_token(self):
        r'''Gets stop token.

        Set to string or none.

        Returns string or none.
        '''
        return self._stop_token
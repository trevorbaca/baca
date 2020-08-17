import collections
import numbers
import typing

import abjad

from . import classes, const, pitchclasses, scoping, typings

### CLASSES ###


class AccidentalAdjustmentCommand(scoping.Command):
    r"""
    Accidental adjustment command.

    ..  container:: example

        >>> baca.AccidentalAdjustmentCommand()
        AccidentalAdjustmentCommand(selector=baca.pleaf(0), tags=[])

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.force_accidental(selector=baca.pleaves()[:2]),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'!2                                                                     %! baca.make_notes()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f'!4.                                                                    %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f'4.                                                                     %! baca.make_notes()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_cautionary", "_forced", "_parenthesized")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        cautionary: bool = None,
        forced: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        parenthesized: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = classes.select().pleaf(0),
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
        )
        if cautionary is not None:
            cautionary = bool(cautionary)
        self._cautionary = cautionary
        if forced is not None:
            forced = bool(forced)
        self._forced = forced
        if parenthesized is not None:
            parenthesized = bool(parenthesized)
        self._parenthesized = parenthesized

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.tag:
            if not self.tag.only_edition() and not self.tag.not_editions():
                raise Exception(f"tag must have edition: {self.tag!r}.")
            tag = abjad.Tag("baca.AccidentalAdjustmentCommand._call()")
            alternative_tag = self.tag.append(tag)
            primary_tag = alternative_tag.invert_edition_tags()
        pleaves = classes.Selection(argument).pleaves()
        assert isinstance(pleaves, classes.Selection)
        for pleaf in pleaves:
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                assert isinstance(pleaf, abjad.Chord)
                note_heads = pleaf.note_heads
            for note_head in note_heads:
                assert note_head is not None
                if not self.tag:
                    if self.cautionary:
                        note_head.is_cautionary = True
                    if self.forced:
                        note_head.is_forced = True
                    if self.parenthesized:
                        note_head.is_parenthesized = True
                else:
                    alternative = abjad.new(note_head)
                    if self.cautionary:
                        alternative.is_cautionary = True
                    if self.forced:
                        alternative.is_forced = True
                    if self.parenthesized:
                        alternative.is_parenthesized = True
                    note_head.alternative = (
                        alternative,
                        str(alternative_tag),
                        str(primary_tag),
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def cautionary(self) -> typing.Optional[bool]:
        """
        Is true when command makes accidentals cautionary.
        """
        return self._cautionary

    @property
    def forced(self) -> typing.Optional[bool]:
        """
        Is true when command forces accidentals.
        """
        return self._forced

    @property
    def parenthesized(self) -> typing.Optional[bool]:
        """
        Is true when command parenthesizes accidentals.
        """
        return self._parenthesized


class ClusterCommand(scoping.Command):
    r"""
    Cluster command.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clusters([3, 4]),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 9/16
                    s1 * 9/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <c' e' g'>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <d' f' a' c''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <bf' d'' f''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <fs'' a'' c''' e'''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <e'' g'' b''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <ef'' g'' b'' d'''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <af'' c''' e'''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <g'' b'' d''' f'''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        }
                        <a' c'' e''>16
                        ^ \markup {
                            \center-align
                                \concat
                                    {
                                        \natural
                                        \flat
                                    }
                            }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ##

    __slots__ = ("_hide_flat_markup", "_start_pitch", "_widths")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        hide_flat_markup=None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=classes.select().plts(),
        start_pitch=None,
        widths=None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        assert isinstance(hide_flat_markup, (bool, type(None)))
        self._hide_flat_markup = hide_flat_markup
        if start_pitch is not None:
            start_pitch = abjad.NamedPitch(start_pitch)
        self._start_pitch = start_pitch
        assert abjad.mathx.all_are_nonnegative_integers(widths)
        widths = abjad.CyclicTuple(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = classes.Selection(argument).leaf(0)
        root = abjad.get.parentage(leaf).root
        with abjad.ForbidUpdate(component=root):
            for i, plt in enumerate(classes.Selection(argument).plts()):
                width = self.widths[i]
                self._make_cluster(plt, width)

    ### PRIVATE METHODS ###

    def _make_cluster(self, plt, width):
        assert plt.is_pitched, repr(plt)
        if not width:
            return
        if self.start_pitch is not None:
            start_pitch = self.start_pitch
        else:
            start_pitch = plt.head.written_pitch
        pitches = self._make_pitches(start_pitch, width)
        key_cluster = abjad.KeyCluster(include_black_keys=not self.hide_flat_markup)
        for pleaf in plt:
            chord = abjad.Chord(pitches, pleaf.written_duration)
            indicators = abjad.detach(object, pleaf)
            for indicator in indicators:
                abjad.attach(indicator, chord)
            abjad.mutate.replace(pleaf, chord)
            abjad.attach(key_cluster, chord)
            abjad.attach(const.ALLOW_REPEAT_PITCH, chord)
            abjad.detach(const.NOT_YET_PITCHED, chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width - 1):
            pitch = pitches[-1] + abjad.NamedInterval("M3")
            pitch = abjad.NamedPitch(pitch, accidental="natural")
            assert pitch.accidental == abjad.Accidental("natural")
            pitches.append(pitch)
        return pitches

    def _mutates_score(self):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def hide_flat_markup(self) -> typing.Optional[bool]:
        r"""
        Is true when cluster hides flat markup.

        ..  container:: example

            Hides flat markup:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.pitch('E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.natural_clusters(widths=[3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                        {                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                            \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                            \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                            s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                            \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                            \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                    <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                            {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \natural
                                    }
                                - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                ^ \markup {
                                    \center-align
                                        \natural
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \natural
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                ^ \markup {
                                    \center-align
                                        \natural
                                    }
                                <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
                <BLANKLINE>
                                <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                        % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        """
        return self._hide_flat_markup

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Selects PLTs.

        ..  container:: example

            >>> baca.clusters([3, 4]).selector
            baca.plts(exclude='HIDDEN')

        """
        return self._selector

    @property
    def start_pitch(self) -> typing.Optional[abjad.NamedPitch]:
        r"""
        Gets start pitch.

        ..  container:: example

            Takes start pitch from input notes:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitches('C4 D4 E4 F4'),
            ...     baca.clusters([3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                        {                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                            \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                            \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                            s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                            \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                            \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                    <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                            {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <c' e' g'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <d' f' a'>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <f' a' c''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
                <BLANKLINE>
                                <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                        % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        ..  container:: example

            Sets start pitch explicitly:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.clusters([3], start_pitch='G4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                        {                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                            \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                            \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                            s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                            \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                            \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                    <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                            {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
                <BLANKLINE>
                                <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                        % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        """
        return self._start_pitch

    @property
    def widths(self) -> typing.Optional[typing.Sequence[int]]:
        r"""
        Gets widths.

        ..  container:: example

            Increasing widths:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.clusters([1, 2, 3, 4], start_pitch='E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                        {                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                            \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                            \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                            s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                            \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                            \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                    <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                            {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g'>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b' d''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
                <BLANKLINE>
                                <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                        % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        ..  container:: example

            Patterned widths:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.clusters([1, 3], start_pitch='E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                        {                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                            \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                            \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                            s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                            \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                            \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                    <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                            {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                                <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
                <BLANKLINE>
                                <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                        % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        ..  container:: example

            Leaves notes and chords unchanged:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitch('E4'),
            ...     baca.clusters([]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                        {                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                            \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                            \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                            s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                            \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                            \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                    <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                            {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                e'2                                                                      %! baca.make_notes()
                                - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                e'4.                                                                     %! baca.make_notes()
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                e'2                                                                      %! baca.make_notes()
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                e'4.                                                                     %! baca.make_notes()
                                <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
                <BLANKLINE>
                                <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                        % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
                <BLANKLINE>
                                    }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                <BLANKLINE>
                                >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.
        """
        return self._widths


class ColorFingeringCommand(scoping.Command):
    r"""
    Color fingering command.

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitch('E4'),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'2                                                                      %! baca.make_notes()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'4.                                                                     %! baca.make_notes()
                            ^ \markup {
                                \override
                                    #'(circle-padding . 0.25)
                                    \circle
                                        \finger
                                            1
                                }
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'2                                                                      %! baca.make_notes()
                            ^ \markup {
                                \override
                                    #'(circle-padding . 0.25)
                                    \circle
                                        \finger
                                            2
                                }
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'4.                                                                     %! baca.make_notes()
                            ^ \markup {
                                \override
                                    #'(circle-padding . 0.25)
                                    \circle
                                        \finger
                                            1
                                }
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """

    ### CLASS VARIABLES ##

    __slots__ = ("_numbers", "_tweaks")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        numbers=None,
        scope: scoping.ScopeTyping = None,
        selector=classes.select().pheads(),
        tweaks: abjad.IndexedTweakManagers = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if numbers is not None:
            assert abjad.mathx.all_are_nonnegative_integers(numbers)
            numbers = abjad.CyclicTuple(numbers)
        self._numbers = numbers
        self._validate_indexed_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        pheads = classes.Selection(argument).pheads()
        total = len(pheads)
        for i, phead in enumerate(pheads):
            number = self.numbers[i]
            if number != 0:
                fingering = abjad.ColorFingering(number)
                self._apply_tweaks(fingering, self.tweaks, i=i, total=total)
                abjad.attach(fingering, phead)

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self):
        """
        Gets numbers.

        ..  container:: example

            >>> command = baca.ColorFingeringCommand(numbers=[0, 1, 2, 1])
            >>> command.numbers
            CyclicTuple([0, 1, 2, 1])

        Set to nonnegative integers.
        """
        return self._numbers

    @property
    def tweaks(self) -> typing.Optional[abjad.IndexedTweakManagers]:
        r"""
        Gets tweaks.
        """
        return self._tweaks


class DiatonicClusterCommand(scoping.Command):
    r"""
    Diatonic cluster command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> command = baca.diatonic_clusters([4, 6])
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ("_widths",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        widths,
        selector=classes.select().plts(),
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        assert abjad.mathx.all_are_nonnegative_integers(widths)
        widths = abjad.CyclicTuple(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, plt in enumerate(classes.Selection(argument).plts()):
            width = self.widths[i]
            start = self._get_lowest_diatonic_pitch_number(plt)
            numbers = range(start, start + width)
            module = abjad.pitch.constants
            change = module._diatonic_pc_number_to_pitch_class_number
            numbers_ = [(12 * (x // 7)) + change[x % 7] for x in numbers]
            pitches = [abjad.NamedPitch(_) for _ in numbers_]
            for pleaf in plt:
                chord = abjad.Chord(pleaf)
                chord.note_heads[:] = pitches
                abjad.mutate.replace(pleaf, chord)

    ### PRIVATE METHODS ###

    def _get_lowest_diatonic_pitch_number(self, plt):
        if isinstance(plt.head, abjad.Note):
            pitch = plt.head.written_pitch
        elif isinstance(plt.head, abjad.Chord):
            pitch = plt.head.written_pitches[0]
        else:
            raise TypeError(plt)
        return pitch._get_diatonic_pitch_number()

    def _mutates_score(self):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def widths(self) -> typing.Optional[typing.Sequence[int]]:
        """
        Gets widths.
        """
        return self._widths


class Loop(abjad.CyclicTuple):
    """
    Loop.

    ..  container:: example

        >>> loop = baca.Loop([0, 2, 4], intervals=[1])
        >>> abjad.f(loop, strict=89)
        baca.Loop(
            [
                abjad.NamedPitch("c'"),
                abjad.NamedPitch("d'"),
                abjad.NamedPitch("e'"),
                ],
            intervals=abjad.CyclicTuple(
                [1]
                ),
            )

        >>> for i in range(12):
        ...     loop[i]
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("cs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("fs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("g'")

        >>> isinstance(loop, abjad.CyclicTuple)
        True

    ..  container:: example

        >>> command = baca.loop([0, 2, 4], [1])
        >>> abjad.f(command, strict=89)
        baca.PitchCommand(
            cyclic=True,
            pitches=baca.Loop(
                [
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("e'"),
                    ],
                intervals=abjad.CyclicTuple(
                    [1]
                    ),
                ),
            selector=baca.plts(exclude='HIDDEN'),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_intervals", "_items")

    ### INITIALIZER ###

    def __init__(self, items=None, *, intervals=None):
        if items is not None:
            assert isinstance(items, collections.abc.Iterable), repr(items)
            items = [abjad.NamedPitch(_) for _ in items]
            items = abjad.CyclicTuple(items)
        abjad.CyclicTuple.__init__(self, items=items)
        if intervals is not None:
            assert isinstance(items, collections.abc.Iterable), repr(items)
            intervals = abjad.CyclicTuple(intervals)
        self._intervals = intervals

    ### SPECIAL METHODS ###

    def __getitem__(self, i) -> abjad.Pitch:
        """
        Gets pitch ``i`` cyclically with intervals.
        """
        if isinstance(i, slice):
            raise NotImplementedError
        iteration = i // len(self)
        if self.intervals is None:
            transposition = 0
        else:
            transposition = sum(self.intervals[:iteration])
        pitch_ = abjad.CyclicTuple(list(self))[i]
        pitch = type(pitch_)(pitch_.number + transposition)
        return pitch

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[list(self.items)],
            storage_format_keyword_names=["intervals"],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def intervals(self):
        """
        Gets intervals.
        """
        return self._intervals

    @property
    def items(self):
        """
        Gets items.
        """
        return self._items


class MicrotoneDeviationCommand(scoping.Command):
    r"""
    Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches('E4'),
        ...     baca.make_even_divisions(),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            eqs'!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            eqf'!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            eqs'!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            eqf'!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            eqs'!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            eqf'!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            eqs'!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """

    ### CLASS VARIABLES ##

    __slots__ = ("_deviations",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deviations=None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=classes.select().plts(),
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if deviations is not None:
            assert isinstance(deviations, collections.abc.Iterable)
            assert all(isinstance(_, numbers.Number) for _ in deviations)
        self._deviations = abjad.CyclicTuple(deviations)

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Cyclically applies deviations to plts in ``argument``.
        """
        if argument is None:
            return
        if not self.deviations:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(classes.Selection(argument).plts()):
            deviation = self.deviations[i]
            self._adjust_pitch(plt, deviation)

    ### PRIVATE METHODS ###

    def _adjust_pitch(self, plt, deviation):
        assert deviation in (0.5, 0, -0.5)
        if deviation == 0:
            return
        for pleaf in plt:
            pitch = pleaf.written_pitch
            accidental = pitch.accidental.semitones + deviation
            pitch = abjad.NamedPitch(pitch, accidental=accidental)
            pleaf.written_pitch = pitch
            annotation = {"color microtone": True}
            abjad.attach(annotation, pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def deviations(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets deviations.

        ..  container:: example

            >>> command = baca.deviation([0, -0.5, 0, 0.5])
            >>> command.deviations
            CyclicTuple([0, -0.5, 0, 0.5])

        Set to iterable of items (each -0.5, 0 or 0.5).
        """
        return self._deviations


class OctaveDisplacementCommand(scoping.Command):
    r"""
    Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.suite(
        ...         baca.pitch('G4'),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            g8                                                                       %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g8                                                                       %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            g'''8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            g'''8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """

    ### CLASS VARIABLES ##

    __slots__ = ("_displacements",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        displacements=None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=classes.select().plts(),
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if displacements is not None:
            displacements = tuple(displacements)
            assert self._is_octave_displacement_vector(displacements)
            displacements = abjad.CyclicTuple(displacements)
        self._displacements = displacements

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.displacements is None:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(classes.Selection(argument).plts()):
            displacement = self.displacements[i]
            interval = abjad.NumberedInterval(12 * displacement)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitch += interval
                    pleaf.written_pitch = pitch
                elif isinstance(pleaf, abjad.Chord):
                    pitches = abjad.PitchSegment(
                        [_ + interval for _ in pleaf.written_pitches]
                    )
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)

    ### PRIVATE METHODS ###

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, (tuple, list)):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def displacements(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets displacements.

        ..  container:: example

            >>> command = baca.displacement(
            ...     [0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2],
            ...     )
            >>> command.displacements
            CyclicTuple([0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2])

        """
        return self._displacements


class PitchCommand(scoping.Command):
    r"""
    Pitch command.

    ..  container:: example

        With pitch numbers:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            b''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            cs''!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            b''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        With pitch numbers:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('C4 F4 F#4 <B4 C#5> D5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            fs'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            <b' cs''!>8
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            fs'!8                                                                    %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            <b' cs''!>8
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            fs'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            <b' cs''!>8
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Large chord:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('<C4 D4 E4 F4 G4 A4 B4 C4>', allow_repeats=True)
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Works with Abjad container:

        >>> command = baca.PitchCommand(
        ...     cyclic=True,
        ...     pitches=[19, 13, 15, 16, 17, 23],
        ...     )

        >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                g''8
                cs''8
                ef''8
                e''8
                f''8
                b''8
                g''8
                cs''8
            }


    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_allow_octaves",
        "_allow_out_of_range",
        "_allow_repeats",
        "_allow_repitch",
        "_mock",
        "_cyclic",
        "_do_not_transpose",
        "_ignore_incomplete",
        "_mutated_score",
        "_persist",
        "_pitches",
        "_state",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allow_octaves: bool = None,
        allow_out_of_range: bool = None,
        allow_repeats: bool = None,
        allow_repitch: bool = None,
        mock: bool = None,
        cyclic: bool = None,
        do_not_transpose: bool = None,
        ignore_incomplete: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        persist: str = None,
        pitches: typing.Union[typing.Sequence, Loop] = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if allow_octaves is not None:
            allow_octaves = bool(allow_octaves)
        self._allow_octaves = allow_octaves
        if allow_out_of_range is not None:
            allow_out_of_range = bool(allow_out_of_range)
        self._allow_out_of_range = allow_out_of_range
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats
        if allow_repitch is not None:
            allow_repitch = bool(allow_repitch)
        self._allow_repitch = allow_repitch
        if mock is not None:
            mock = bool(mock)
        self._mock = mock
        if cyclic is not None:
            cyclic = bool(cyclic)
        self._cyclic = cyclic
        if do_not_transpose is not None:
            do_not_transpose = bool(do_not_transpose)
        self._do_not_transpose = do_not_transpose
        if ignore_incomplete is not None:
            ignore_incomplete = bool(ignore_incomplete)
        self._ignore_incomplete = ignore_incomplete
        self._mutated_score = False
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        if pitches is not None:
            pitches = self._coerce_pitches(pitches)
        self._pitches = pitches
        self._state: abjad.OrderedDict = abjad.OrderedDict()

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.pitches:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        plts = []
        for pleaf in classes.Selection(argument).pleaves():
            plt = abjad.get.logical_tie(pleaf)
            if plt.head is pleaf:
                plts.append(plt)
        self._check_length(plts)
        pitches = self.pitches
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        previous_pitches_consumed = self._previous_pitches_consumed()
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        pitches_consumed = 0
        for i, plt in enumerate(plts):
            pitch = pitches[i + previous_pitches_consumed]
            new_plt = self._set_lt_pitch(
                plt, pitch, allow_repitch=self.allow_repitch, mock=self.mock
            )
            if new_plt is not None:
                self._mutated_score = True
                plt = new_plt
            if self.allow_octaves:
                for pleaf in plt:
                    abjad.attach(const.ALLOW_OCTAVE, pleaf)
            if self.allow_out_of_range:
                for pleaf in plt:
                    abjad.attach(const.ALLOW_OUT_OF_RANGE, pleaf)
            if self.allow_repeats:
                for pleaf in plt:
                    abjad.attach(const.ALLOW_REPEAT_PITCH, pleaf)
            if self.do_not_transpose is True:
                for pleaf in plt:
                    abjad.attach(const.DO_NOT_TRANSPOSE, pleaf)
            pitches_consumed += 1
        self._state = abjad.OrderedDict()
        pitches_consumed += previous_pitches_consumed
        self.state["pitches_consumed"] = pitches_consumed

    ### PRIVATE METHODS ###

    def _check_length(self, plts):
        if self.cyclic:
            return
        if len(self.pitches) < len(plts):
            message = f"only {len(self.pitches)} pitches"
            message += f" for {len(plts)} logical ties:\n\n"
            message += f"{self!r} and {plts!r}."
            raise Exception(message)

    @staticmethod
    def _coerce_pitches(pitches):
        if isinstance(pitches, str):
            pitches = PitchCommand._parse_string(pitches)
        items = []
        for item in pitches:
            if isinstance(item, str) and "<" in item and ">" in item:
                item = item.strip("<")
                item = item.strip(">")
                item = abjad.PitchSet(item, abjad.NamedPitch)
            elif isinstance(item, str):
                item = abjad.NamedPitch(item)
            elif isinstance(item, collections.abc.Iterable):
                item = abjad.PitchSet(item, abjad.NamedPitch)
            else:
                item = abjad.NamedPitch(item)
            items.append(item)
        if isinstance(pitches, Loop):
            pitches = type(pitches)(items=items, intervals=pitches.intervals)
        else:
            pitches = abjad.CyclicTuple(items)
        return pitches

    def _mutates_score(self):
        pitches = self.pitches or []
        if any(isinstance(_, collections.abc.Iterable) for _ in pitches):
            return True
        return self._mutated_score

    @staticmethod
    def _parse_string(string):
        items, current_chord = [], []
        for part in string.split():
            if "<" in part:
                assert not current_chord
                current_chord.append(part)
            elif ">" in part:
                assert current_chord
                current_chord.append(part)
                item = " ".join(current_chord)
                items.append(item)
                current_chord = []
            elif current_chord:
                current_chord.append(part)
            else:
                items.append(part)
        assert not current_chord, repr(current_chord)
        return items

    def _previous_pitches_consumed(self):
        dictionary = self.runtime.get("previous_segment_voice_metadata", None)
        if not dictionary:
            return 0
        dictionary = dictionary.get(const.PITCH, None)
        if not dictionary:
            return 0
        if dictionary.get("name") != self.persist:
            return 0
        pitches_consumed = dictionary.get("pitches_consumed", None)
        if not pitches_consumed:
            return 0
        assert 1 <= pitches_consumed
        if self.ignore_incomplete:
            return pitches_consumed
        dictionary = self.runtime["previous_segment_voice_metadata"]
        dictionary = dictionary.get(const.RHYTHM, None)
        if dictionary:
            if dictionary.get("incomplete_final_note", False):
                pitches_consumed -= 1
        return pitches_consumed

    @staticmethod
    def _set_lt_pitch(
        lt, pitch, *, allow_repitch=False, mock=False, set_chord_pitches_equal=False,
    ):
        new_lt = None
        already_pitched = const.ALREADY_PITCHED
        for leaf in lt:
            abjad.detach(const.NOT_YET_PITCHED, leaf)
            if mock is True:
                abjad.attach(const.MOCK, leaf)
            if allow_repitch:
                continue
            if abjad.get.has_indicator(leaf, already_pitched):
                voice = abjad.get.parentage(leaf).get(abjad.Voice)
                if voice is None:
                    name = "no voice"
                else:
                    name = voice.name
                message = f"already pitched {repr(leaf)} in {name}."
                raise Exception(message)
            abjad.attach(already_pitched, leaf)
        if pitch is None:
            if not lt.is_pitched:
                pass
            else:
                for leaf in lt:
                    rest = abjad.Rest(leaf.written_duration, multiplier=leaf.multiplier)
                    abjad.mutate.replace(leaf, rest, wrappers=True)
                new_lt = abjad.get.logical_tie(rest)
        elif isinstance(pitch, collections.abc.Iterable):
            if isinstance(lt.head, abjad.Chord):
                for chord in lt:
                    chord.written_pitches = pitch
            else:
                assert isinstance(lt.head, (abjad.Note, abjad.Rest))
                for leaf in lt:
                    chord = abjad.Chord(
                        pitch, leaf.written_duration, multiplier=leaf.multiplier,
                    )
                    abjad.mutate.replace(leaf, chord, wrappers=True)
                new_lt = abjad.get.logical_tie(chord)
        else:
            if isinstance(lt.head, abjad.Note):
                for note in lt:
                    note.written_pitch = pitch
            elif set_chord_pitches_equal is True and isinstance(lt.head, abjad.Chord):
                for chord in lt:
                    for note_head in chord.note_heads:
                        note_head.written_pitch = pitch
            else:
                assert isinstance(lt.head, (abjad.Chord, abjad.Rest))
                for leaf in lt:
                    note = abjad.Note(
                        pitch, leaf.written_duration, multiplier=leaf.multiplier,
                    )
                    abjad.mutate.replace(leaf, note, wrappers=True)
                new_lt = abjad.get.logical_tie(note)
        return new_lt

    ### PUBLIC PROPERTIES ###

    @property
    def allow_octaves(self) -> typing.Optional[bool]:
        """
        Is true when command allows octaves.
        """
        return self._allow_octaves

    @property
    def allow_out_of_range(self) -> typing.Optional[bool]:
        """
        Is true when command allows out-of-range pitches.
        """
        return self._allow_out_of_range

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        """
        Is true when command allows repeat pitches.
        """
        return self._allow_repeats

    @property
    def allow_repitch(self) -> typing.Optional[bool]:
        """
        Is true when command allows repitch.
        """
        return self._allow_repitch

    @property
    def cyclic(self) -> typing.Optional[bool]:
        """
        Is true when command reads pitches cyclically.
        """
        return self._cyclic

    @property
    def do_not_transpose(self) -> typing.Optional[bool]:
        """
        Is true when pitch escapes transposition.
        """
        return self._do_not_transpose

    @property
    def ignore_incomplete(self) -> typing.Optional[bool]:
        """
        Is true when persistent pitch command ignores previous segment
        incomplete last note.
        """
        return self._ignore_incomplete

    @property
    def mock(self) -> typing.Optional[bool]:
        """
        Is true when command tags leaves as mock.
        """
        return self._mock

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.PitchCommand().parameter
            'PITCH'

        """
        return const.PITCH

    @property
    def persist(self) -> typing.Optional[str]:
        """
        Gets persist name.
        """
        return self._persist

    @property
    def pitches(self):
        """
        Gets pitches.

        ..  container:: example

            Gets pitches:

            >>> command = baca.PitchCommand(
            ...     pitches=[19, 13, 15, 16, 17, 23],
            ...     )

            >>> for pitch in command.pitches:
            ...     pitch
            NamedPitch("g''")
            NamedPitch("cs''")
            NamedPitch("ef''")
            NamedPitch("e''")
            NamedPitch("f''")
            NamedPitch("b''")

        """
        return self._pitches

    @property
    def state(self) -> abjad.OrderedDict:
        """
        Gets state dictionary.
        """
        return self._state


class RegisterCommand(scoping.Command):
    r"""
    Register command.

    ..  container:: example

        With music-maker:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 15)],
        ...             ),
        ...         ),
        ... )
        >>> selection = stack([[10, 12, 14], [10, 12, 14], [10, 12, 14]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 9/16
                    s1 * 9/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches('G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4'),
        ...     baca.make_even_divisions(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 15)],
        ...             ),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            gqs''!8                                                                  %! baca.make_even_divisions()
            <BLANKLINE>
                            gs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            gtqs''!8                                                                 %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            aqf''!8                                                                  %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            af''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            atqf''!8                                                                 %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            gqs''!8                                                                  %! baca.make_even_divisions()
            <BLANKLINE>
                            gs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            gtqs''!8                                                                 %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            aqf''!8                                                                  %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            af''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            atqf''!8                                                                 %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Works with chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([('[A0, C8]', -6)]),
        ...         ),
        ... )
        >>> selection = stack([{10, 12, 14}])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 1/16
                    s1 * 1/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        <bf c' d'>16
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_registration",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        registration=None,
        scope: scoping.ScopeTyping = None,
        selector=classes.select().plts(),
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if registration is not None:
            prototype = pitchclasses.Registration
            assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.registration is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = classes.Selection(argument).plts()
        assert isinstance(plts, classes.Selection)
        for plt in plts:
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitches = self.registration([pitch])
                    pleaf.written_pitch = pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    pitches = pleaf.written_pitches
                    pitches = self.registration(pitches)
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(const.NOT_YET_REGISTERED, pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def registration(self) -> typing.Optional[pitchclasses.Registration]:
        """
        Gets registration.

        ..  container:: example

            >>> command = baca.RegisterCommand(
            ...     registration=baca.Registration(
            ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
            ...         ),
            ...     )

            >>> abjad.f(command.registration, strict=89)
            baca.Registration(
                components=[
                    baca.RegistrationComponent(
                        source_pitch_range=abjad.PitchRange('[A0, C4)'),
                        target_octave_start_pitch=abjad.NumberedPitch(15),
                        ),
                    baca.RegistrationComponent(
                        source_pitch_range=abjad.PitchRange('[C4, C8)'),
                        target_octave_start_pitch=abjad.NumberedPitch(27),
                        ),
                    ],
                )

        """
        return self._registration


class RegisterInterpolationCommand(scoping.Command):
    r"""
    Register interpolation command.

    :param selector: command selector.

    :param start_pitch: interpolation start pitch.

    :param stop_pitch: interpolation stop pitch.

    ..  container:: example

        With music-maker:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/2
                    s1 * 3/2
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c''16
                        b'16
                        af'16
                        g''16
                        cs''16
                        d''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''16
                        [
                        e''16
                        ef''16
                        f''16
                        a''16
                        bf''16
                        c'''16
                        b''16
                        af''16
                        g'''16
                        cs'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = [
        ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
        ...     ]
        >>> collections = [set(_) for _ in collections]
        >>> selection = stack(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/8
                    s1 * 3/8
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        <e' fs'>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <f' ef''>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <a' bf'>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <c'' b''>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <g'' af''>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <cs''' d'''>16
                    }
                }
            >>

    ..  container:: example

        Holds register constant:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, 12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 9]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            fs''!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            a''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            bf''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            c''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            b''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            af''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            fs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            ef''!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            a''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            bf''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            b''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            af''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            fs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 9]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 9]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to 0:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, 0),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 9]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            fs''!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            a''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            bf'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            c''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            b'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            af'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            g''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            fs'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            ef''!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            a'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            bf'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            af'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            d'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            fs'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            ef'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 9]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 9]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Octave-transposes to a target interpolated from 0 up to 12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(0, 12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 9]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            fs'!8                                                                    %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            ef'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            a'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            bf'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            c''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            b'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            af'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            fs'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            ef''!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            a'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            bf'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            af'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            fs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 9]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 9]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to -12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, -12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 9]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            fs''!8                                                                   %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            a'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            bf'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            c''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            b'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            af'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            fs'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            ef'!8                                                                    %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            a'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            bf!8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            b8                                                                       %! baca.make_even_divisions()
            <BLANKLINE>
                            af!8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g8                                                                       %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            cs'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            d'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            fs!8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e8                                                                       %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            ef!8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            f8                                                                       %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 9]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 9]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Octave-transposes to a target interpolated from -12 up to 12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(-12, 12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 9]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            fs!8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            e8                                                                       %! baca.make_even_divisions()
            <BLANKLINE>
                            ef!8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            f8                                                                       %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            a8                                                                       %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            bf!8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            b8                                                                       %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            af!8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            cs'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            fs'!8                                                                    %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            ef'!8                                                                    %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            a'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            bf'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            af'!8                                                                    %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            cs''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            fs''!8                                                                   %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            ef''!8                                                                   %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 9]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 9]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_start_pitch", "_stop_pitch")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = classes.select().plts(),
        start_pitch: typing.Union[abjad.Number, abjad.NumberedPitch] = 0,
        stop_pitch: typing.Union[abjad.Number, abjad.NumberedPitch] = 0,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        start_pitch = abjad.NumberedPitch(start_pitch)
        self._start_pitch: abjad.NumberedPitch = start_pitch
        stop_pitch = abjad.NumberedPitch(stop_pitch)
        self._stop_pitch: abjad.NumberedPitch = stop_pitch

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = classes.Selection(argument).plts()
        length = len(plts)
        for i, plt in enumerate(plts):
            registration = self._get_registration(i, length)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    written_pitches = registration([pleaf.written_pitch])
                    pleaf.written_pitch = written_pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    written_pitches = registration(pleaf.written_pitches)
                    pleaf.written_pitches = written_pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(const.NOT_YET_REGISTERED, pleaf)

    ### PRIVATE METHODS ###

    def _get_registration(self, i, length):
        start_pitch = self.start_pitch.number
        stop_pitch = self.stop_pitch.number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(i, length)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        return pitchclasses.Registration([("[A0, C8]", current_pitch)])

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets selector.

        ..  container:: example

            Selects tuplet 0:

            >>> stack = baca.stack(
            ...     baca.figure([1], 16),
            ...     rmakers.beam(),
            ...     baca.color(baca.tuplet(0)),
            ...     baca.register(0, 24, selector=baca.tuplet(0)),
            ... )

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> selection = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            fs'16
                            [
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            ef''16
                            \abjad-color-music #'green
                            f''16
                            \abjad-color-music #'green
                            a'16
                            \abjad-color-music #'green
                            bf'16
                            \abjad-color-music #'green
                            c''16
                            \abjad-color-music #'green
                            b''16
                            \abjad-color-music #'green
                            af''16
                            \abjad-color-music #'green
                            g''16
                            \abjad-color-music #'green
                            cs'''16
                            \abjad-color-music #'green
                            d'''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs'16
                            [
                            e'16
                            ef'16
                            f'16
                            a'16
                            bf'16
                            c'16
                            b'16
                            af'16
                            g'16
                            cs'16
                            d'16
                            ]
                        }
                    }
                >>

        ..  container:: example

            Selects tuplet -1:

            >>> stack = baca.stack(
            ...     baca.figure([1], 16),
            ...     rmakers.beam(),
            ...     baca.color(baca.tuplet(-1)),
            ...     baca.register(0, 24, selector=baca.tuplet(-1)),
            ... )

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> selection = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            fs'16
                            [
                            e'16
                            ef'16
                            f'16
                            a'16
                            bf'16
                            c'16
                            b'16
                            af'16
                            g'16
                            cs'16
                            d'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            fs'16
                            [
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            ef''16
                            \abjad-color-music #'green
                            f''16
                            \abjad-color-music #'green
                            a'16
                            \abjad-color-music #'green
                            bf'16
                            \abjad-color-music #'green
                            c''16
                            \abjad-color-music #'green
                            b''16
                            \abjad-color-music #'green
                            af''16
                            \abjad-color-music #'green
                            g''16
                            \abjad-color-music #'green
                            cs'''16
                            \abjad-color-music #'green
                            d'''16
                            ]
                        }
                    }
                >>

        ..  container:: example

            Maps to tuplets:

            >>> stack = baca.stack(
            ...     baca.figure([1], 16),
            ...     rmakers.beam(),
            ...     baca.color(baca.tuplets()),
            ...     baca.new(
            ...         baca.register(0, 24),
            ...         map=baca.tuplets(),
            ...         ),
            ... )

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> selection = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            fs'16
                            [
                            \abjad-color-music #'red
                            e'16
                            \abjad-color-music #'red
                            ef''16
                            \abjad-color-music #'red
                            f''16
                            \abjad-color-music #'red
                            a'16
                            \abjad-color-music #'red
                            bf'16
                            \abjad-color-music #'red
                            c''16
                            \abjad-color-music #'red
                            b''16
                            \abjad-color-music #'red
                            af''16
                            \abjad-color-music #'red
                            g''16
                            \abjad-color-music #'red
                            cs'''16
                            \abjad-color-music #'red
                            d'''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            fs'16
                            [
                            \abjad-color-music #'blue
                            e'16
                            \abjad-color-music #'blue
                            ef''16
                            \abjad-color-music #'blue
                            f''16
                            \abjad-color-music #'blue
                            a'16
                            \abjad-color-music #'blue
                            bf'16
                            \abjad-color-music #'blue
                            c''16
                            \abjad-color-music #'blue
                            b''16
                            \abjad-color-music #'blue
                            af''16
                            \abjad-color-music #'blue
                            g''16
                            \abjad-color-music #'blue
                            cs'''16
                            \abjad-color-music #'blue
                            d'''16
                            ]
                        }
                    }
                >>

        """
        return self._selector

    @property
    def start_pitch(self) -> abjad.NumberedPitch:
        """
        Gets start pitch.
        """
        return self._start_pitch

    @property
    def stop_pitch(self) -> abjad.NumberedPitch:
        """
        Gets stop pitch.
        """
        return self._stop_pitch


class RegisterToOctaveCommand(scoping.Command):
    r"""
    Register-to-octave command.

    ..  container:: example

        Chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([{0, 14, 28}])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 1/16
                    s1 * 1/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        <c' d'' e'''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([{0, 14, 28}])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 1/16
                    s1 * 1/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        <c d' e''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([{0, 14, 28}])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 1/16
                    s1 * 1/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        <c, d e'>16
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([[0, 14, 28]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/16
                    s1 * 3/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d''16
                        e'''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([[0, 14, 28]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/16
                    s1 * 3/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        c16
                        [
                        d'16
                        e''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([[0, 14, 28]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/16
                    s1 * 3/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        c,16
                        [
                        d16
                        e'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([[10, 12, 14]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/16
                    s1 * 3/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        bf'16
                        [
                        c''16
                        d''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([[10, 12, 14]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/16
                    s1 * 3/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...         ),
        ... )

        >>> selection = stack([[10, 12, 14]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/16
                    s1 * 3/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        >>> baca.RegisterToOctaveCommand()
        RegisterToOctaveCommand(selector=baca.plts())

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_anchor", "_octave_number")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        anchor=None,
        octave_number=None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=classes.select().plts(),
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if anchor is not None:
            prototype = (abjad.Center, abjad.Down, abjad.Up)
            assert anchor in prototype, repr(anchor)
        self._anchor = anchor
        if octave_number is not None:
            assert isinstance(octave_number, int), repr(octave_number)
        self._octave_number = octave_number

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.octave_number is None:
            return
        if self.selector:
            argument = self.selector(argument)
        target_octave_number = self.octave_number or 4
        current_octave_number = self._get_anchor_octave_number(argument)
        octave_adjustment = target_octave_number - current_octave_number
        transposition = abjad.Transposition(n=12 * octave_adjustment)
        pleaves = classes.Selection(argument).pleaves()
        assert isinstance(pleaves, classes.Selection)
        for pleaf in pleaves:
            self._set_pitch(pleaf, transposition)

    ### PRIVATE METHODS ###

    def _get_anchor_octave_number(self, argument):
        pitches = []
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            if isinstance(leaf, abjad.Note):
                pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                pitches.extend(leaf.written_pitches)
            else:
                raise TypeError(leaf)
        pitches = list(set(pitches))
        pitches.sort()
        anchor = self.anchor or abjad.Down
        if anchor == abjad.Down:
            pitch = pitches[0]
        elif anchor == abjad.Up:
            pitch = pitches[-1]
        elif anchor == abjad.Center:
            pitch = self._get_centroid(pitches)
        else:
            raise ValueError(anchor)
        return pitch.octave.number

    @staticmethod
    def _get_centroid(pitches):
        soprano = max(pitches)
        bass = min(pitches)
        centroid = (soprano.number + bass.number) / 2.0
        return abjad.NumberedPitch(centroid)

    def _set_pitch(self, leaf, transposition):
        if isinstance(leaf, abjad.Note):
            pitch = transposition(leaf.written_pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            pitches = [transposition(_) for _ in leaf.written_pitches]
            leaf.written_pitches = pitches
        abjad.detach(const.NOT_YET_REGISTERED, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def anchor(self) -> typing.Optional[abjad.enums.VerticalAlignment]:
        """
        Gets anchor.

        ..  container:: example

            Bass anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Down,
            ...     octave_number=5,
            ...     )
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c'' d''' e''''>1

        ..  container:: example

            Center anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Center,
            ...     octave_number=5,
            ...     )
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c' d'' e'''>1

        ..  container:: example

            Soprano anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Up,
            ...     octave_number=5,
            ...     )
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c d' e''>1

        """
        return self._anchor

    @property
    def octave_number(self) -> int:
        r"""
        Gets octave number.

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c, d e'>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=1)
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c,, d, e>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=2)
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c, d e'>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=3)
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c d' e''>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=4)
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c' d'' e'''>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=5)
            >>> command(chord)

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c'' d''' e''''>1

        """
        return self._octave_number


class StaffPositionCommand(scoping.Command):
    r"""
    Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                \clef "treble"
                b'4
                d''4
                b'4
                d''4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef('percussion'), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_allow_out_of_range",
        "_allow_repeats",
        "_allow_repitch",
        "_mock",
        "_exact",
        "_mutated_score",
        "_numbers",
        "_set_chord_pitches_equal",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        numbers,
        *,
        allow_out_of_range: bool = None,
        allow_repeats: bool = None,
        allow_repitch: bool = None,
        exact: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        mock: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = classes.select().plts(),
        set_chord_pitches_equal: bool = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        prototype = (int, list, abjad.StaffPosition)
        assert all(isinstance(_, prototype) for _ in numbers), repr(numbers)
        numbers = abjad.CyclicTuple(numbers)
        self._numbers = numbers
        if allow_out_of_range is not None:
            allow_out_of_range = bool(allow_out_of_range)
        self._allow_out_of_range = allow_out_of_range
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats
        if allow_repitch is not None:
            allow_repitch = bool(allow_repitch)
        self._allow_repitch = allow_repitch
        if mock is not None:
            mock = bool(mock)
        self._mock = mock
        if exact is not None:
            exact = bool(exact)
        self._exact = exact
        self._mutated_score = False
        if set_chord_pitches_equal is not None:
            set_chord_pitches_equal = bool(set_chord_pitches_equal)
        self._set_chord_pitches_equal = set_chord_pitches_equal

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        plt_count = 0
        for i, plt in enumerate(classes.Selection(argument).plts()):
            clef = abjad.get.effective(
                plt.head, abjad.Clef, default=abjad.Clef("treble"),
            )
            number = self.numbers[i]
            if isinstance(number, list):
                positions = [abjad.StaffPosition(_) for _ in number]
                pitches = [_.to_pitch(clef) for _ in positions]
                new_lt = PitchCommand._set_lt_pitch(
                    plt,
                    pitches,
                    allow_repitch=self.allow_repitch,
                    mock=self.mock,
                    set_chord_pitches_equal=self.set_chord_pitches_equal,
                )
                if new_lt is not None:
                    self._mutated_score = True
                    plt = new_lt
            else:
                position = abjad.StaffPosition(number)
                pitch = position.to_pitch(clef)
                new_lt = PitchCommand._set_lt_pitch(
                    plt,
                    pitch,
                    allow_repitch=self.allow_repitch,
                    mock=self.mock,
                    set_chord_pitches_equal=self.set_chord_pitches_equal,
                )
                if new_lt is not None:
                    self._mutated_score = True
                    plt = new_lt
            plt_count += 1
            for pleaf in plt:
                abjad.attach(const.STAFF_POSITION, pleaf)
                if self.allow_out_of_range:
                    abjad.attach(const.ALLOW_OUT_OF_RANGE, pleaf)
                if self.allow_repeats:
                    abjad.attach(const.ALLOW_REPEAT_PITCH, pleaf)
                    abjad.attach(const.DO_NOT_TRANSPOSE, pleaf)
        if self.exact and plt_count != len(self.numbers):
            message = f"PLT count ({plt_count}) does not match"
            message += f" staff position count ({len(self.numbers)})."
            raise Exception(message)

    ### PRIVATE METHODS ###

    def _mutates_score(self):
        numbers = self.numbers or []
        if any(isinstance(_, collections.abc.Iterable) for _ in numbers):
            return True
        return self._mutated_score

    ### PUBLIC PROPERTIES ###

    @property
    def allow_out_of_range(self) -> typing.Optional[bool]:
        """
        Is true when out-of-range staff positions are allowed.
        """
        return self._allow_out_of_range

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        """
        Is true when repeat staff positions are allowed.
        """
        return self._allow_repeats

    @property
    def allow_repitch(self) -> typing.Optional[bool]:
        """
        Is true when command allows repitch.
        """
        return self._allow_repitch

    @property
    def exact(self) -> typing.Optional[bool]:
        """
        Is true when number of staff positions must match number of leaves
        exactly.
        """
        return self._exact

    @property
    def mock(self) -> typing.Optional[bool]:
        """
        Is true when command tags leaves as mock.
        """
        return self._mock

    @property
    def numbers(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets numbers.
        """
        return self._numbers

    @property
    def set_chord_pitches_equal(self) -> typing.Optional[bool]:
        """
        Is true when command sets chord pitches equal.
        """
        return self._set_chord_pitches_equal


class StaffPositionInterpolationCommand(scoping.Command):
    r"""
    Staff position interpolation command.

    :param selector: selector.

    :param start: start pitch or start staff position.

    :param stop: stop pitch or stop staff position.


    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_mock",
        "_pitches_instead_of_staff_positions",
        "_start",
        "_stop",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        start: typing.Union[int, str, abjad.NamedPitch, abjad.StaffPosition],
        stop: typing.Union[int, str, abjad.NamedPitch, abjad.StaffPosition],
        *,
        mock: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        pitches_instead_of_staff_positions: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = classes.select().plts(),
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        prototype = (abjad.NamedPitch, abjad.StaffPosition)
        if isinstance(start, str):
            start = abjad.NamedPitch(start)
        elif isinstance(start, int):
            start = abjad.StaffPosition(start)
        assert isinstance(start, prototype), repr(start)
        self._start = start
        if isinstance(stop, str):
            stop = abjad.NamedPitch(stop)
        elif isinstance(stop, int):
            stop = abjad.StaffPosition(stop)
        assert isinstance(stop, prototype), repr(stop)
        self._stop = stop
        if mock is not None:
            mock = bool(mock)
        self._mock = mock
        if pitches_instead_of_staff_positions is not None:
            pitches_instead_of_staff_positions = bool(
                pitches_instead_of_staff_positions
            )
        self._pitches_instead_of_staff_positions = pitches_instead_of_staff_positions

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = classes.Selection(argument).plts()
        if not plts:
            return
        count = len(plts)
        if isinstance(self.start, abjad.StaffPosition):
            start_staff_position = self.start
        else:
            start_phead = plts[0].head
            clef = abjad.get.effective(start_phead, abjad.Clef)
            start_staff_position = abjad.StaffPosition.from_pitch_and_clef(
                self.start, clef,
            )
        if isinstance(self.stop, abjad.StaffPosition):
            stop_staff_position = self.stop
        else:
            stop_phead = plts[-1].head
            clef = abjad.get.effective(
                stop_phead, abjad.Clef, default=abjad.Clef("treble"),
            )
            stop_staff_position = abjad.StaffPosition.from_pitch_and_clef(
                self.stop, clef,
            )
        unit_distance = abjad.Fraction(
            stop_staff_position.number - start_staff_position.number, count - 1
        )
        for i, plt in enumerate(plts):
            staff_position = unit_distance * i + start_staff_position.number
            staff_position = round(staff_position)
            staff_position = abjad.StaffPosition(staff_position)
            clef = abjad.get.effective(
                plt.head, abjad.Clef, default=abjad.Clef("treble"),
            )
            pitch = staff_position.to_pitch(clef)
            new_lt = PitchCommand._set_lt_pitch(
                plt, pitch, allow_repitch=True, mock=self.mock
            )
            assert new_lt is None, repr(new_lt)
            for leaf in plt:
                abjad.attach(const.ALLOW_REPEAT_PITCH, leaf)
                if not self.pitches_instead_of_staff_positions:
                    abjad.attach(const.STAFF_POSITION, leaf)
        if isinstance(self.start, abjad.NamedPitch):
            start_pitch = self.start
        else:
            clef = abjad.get.effective(
                plts[0], abjad.Clef, default=abjad.Clef("treble"),
            )
            start_pitch = self.start.to_pitch(clef)
        new_lt = PitchCommand._set_lt_pitch(
            plts[0], start_pitch, allow_repitch=True, mock=self.mock
        )
        assert new_lt is None, repr(new_lt)
        if isinstance(self.stop, abjad.NamedPitch):
            stop_pitch = self.stop
        else:
            clef = abjad.get.effective(
                plts[0], abjad.Clef, default=abjad.Clef("treble"),
            )
            stop_pitch = self.stop.to_pitch(clef=clef)
        new_lt = PitchCommand._set_lt_pitch(
            plts[-1], stop_pitch, allow_repitch=True, mock=self.mock
        )
        assert new_lt is None, repr(new_lt)

    ### PUBLIC PROPERTIES ###

    @property
    def mock(self) -> typing.Optional[bool]:
        """
        Is true command tags leaves as mock.
        """
        return self._mock

    @property
    def pitches_instead_of_staff_positions(self) -> typing.Optional[bool]:
        """
        Is true command interprets ``start`` and ``stop`` as pitches instead of
        staff positions.
        """
        return self._pitches_instead_of_staff_positions

    @property
    def start(self) -> typing.Union[abjad.NamedPitch, abjad.StaffPosition]:
        """
        Gets start.
        """
        return self._start

    @property
    def stop(self) -> typing.Union[abjad.NamedPitch, abjad.StaffPosition]:
        """
        Gets stop.
        """
        return self._stop


### FACTORY FUNCTIONS ###


def bass_to_octave(
    n: int, selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the lowest note in the entire
        selection appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.bass_to_octave(3),
        ...     baca.color(baca.plts().group()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'green
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        f'8
                        ~
                        [
                        \abjad-color-music #'green
                        f'32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <ef' e' fs''>8
                        ~
                        [
                        \abjad-color-music #'green
                        <ef' e' fs''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <g af'>8
                        ~
                        [
                        \abjad-color-music #'green
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        a8
                        ~
                        [
                        \abjad-color-music #'green
                        a32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the lowest pitch in each pitched
        logical tie appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.bass_to_octave(3),
        ...         map=baca.plts(),
        ...         ),
        ...     baca.color(baca.plts()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'blue
                        f8
                        ~
                        [
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        ~
                        [
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'blue
                        <g af'>8
                        ~
                        [
                        \abjad-color-music #'blue
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        a8
                        ~
                        [
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.Down, octave_number=n, selector=selector
    )


def center_to_octave(
    n: int, selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the centroid of all PLTs appears
        in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.center_to_octave(3),
        ...     baca.color(baca.plts().group()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <c, d, bf,>8
                        ~
                        [
                        \abjad-color-music #'green
                        <c, d, bf,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        f8
                        ~
                        [
                        \abjad-color-music #'green
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <ef e fs'>8
                        ~
                        [
                        \abjad-color-music #'green
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <g, af>8
                        ~
                        [
                        \abjad-color-music #'green
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        a,8
                        ~
                        [
                        \abjad-color-music #'green
                        a,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the centroid of each pitched
        logical tie appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.center_to_octave(3),
        ...         map=baca.plts(),
        ...         ),
        ...     baca.color(baca.plts()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'blue
                        f8
                        ~
                        [
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        ~
                        [
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'blue
                        <g, af>8
                        ~
                        [
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        a8
                        ~
                        [
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.Center, octave_number=n, selector=selector
    )


def clusters(
    widths: typing.List[int],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
) -> ClusterCommand:
    """
    Makes clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(selector=selector, start_pitch=start_pitch, widths=widths)


def color_fingerings(
    numbers: typing.List[abjad.Number],
    *tweaks: abjad.IndexedTweakManager,
    selector: abjad.Expression = classes.select().pheads(exclude=const.HIDDEN),
) -> ColorFingeringCommand:
    """
    Adds color fingerings.
    """
    return ColorFingeringCommand(numbers=numbers, selector=selector, tweaks=tweaks)


def deviation(
    deviations: typing.List[abjad.Number],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> MicrotoneDeviationCommand:
    """
    Sets microtone ``deviations``.
    """
    return MicrotoneDeviationCommand(deviations=deviations, selector=selector)


def diatonic_clusters(
    widths: typing.List[int],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> DiatonicClusterCommand:
    """
    Makes diatonic clusters with ``widths``.
    """
    return DiatonicClusterCommand(selector=selector, widths=widths)


def displacement(
    displacements: typing.List[int],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> OctaveDisplacementCommand:
    r"""
    Octave-displaces ``selector`` output.

    ..  container:: example

        Octave-displaces PLTs:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack(3 * [[0, 2, 3]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 27/16
                    s1 * 27/16
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        c16
                        [
                        d''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/12 {
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    ..  container:: example

        Octave-displaces chords:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [4],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ... )
        >>> selection = stack(6 * [{0, 2, 3}])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 15/8
                    s1 * 15/8
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        r8
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c'' d'' ef''>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c'' d'' ef''>4
                        r4
                    }
                }
            >>

    """
    return OctaveDisplacementCommand(displacements=displacements, selector=selector)


def force_accidental(
    selector: abjad.Expression = classes.select().pleaf(0, exclude=const.HIDDEN),
) -> AccidentalAdjustmentCommand:
    r"""
    Forces accidental.

    ..  container:: example

        Inverts edition-specific tags:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.not_parts(baca.force_accidental(selector=baca.pleaves()[:2])),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'2                                                                      %! +PARTS:baca.AccidentalAdjustmentCommand._call()
                        %@% e'!2                                                                     %! -PARTS:baca.AccidentalAdjustmentCommand._call() %! baca.make_notes()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f'4.                                                                     %! +PARTS:baca.AccidentalAdjustmentCommand._call()
                        %@% f'!4.                                                                    %! -PARTS:baca.AccidentalAdjustmentCommand._call() %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            e'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f'4.                                                                     %! baca.make_notes()
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """
    return AccidentalAdjustmentCommand(forced=True, selector=selector)


def interpolate_pitches(
    start: typing.Union[int, str, abjad.NamedPitch],
    stop: typing.Union[int, str, abjad.NamedPitch],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    mock: bool = None,
) -> StaffPositionInterpolationCommand:
    r"""
    Interpolates from staff position of ``start`` pitch to staff
    position of ``stop`` pitch.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble"),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/2
                    s1 * 3/2
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \clef "treble"                                                               %! baca.clef():baca.IndicatorCommand._call()
                        ef'16
                        [
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        fs''16
                        ]
                    }
                }
            >>

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef('treble'),
        ...     baca.interpolate_pitches('Eb4', 'F#5'),
        ...     baca.glissando(
        ...         allow_repeats=True,
        ...         hide_middle_note_heads=True,
        ...         ),
        ...     baca.glissando_thickness(3),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/2
                    s1 * 3/2
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \override Glissando.thickness = #'3                                          %! baca.glissando_thickness():baca.OverrideCommand._call(1)
                        \clef "treble"                                                               %! baca.clef():baca.IndicatorCommand._call()
                        ef'16
                        [
                        \glissando                                                                   %! baca.glissando():abjad.glissando(7)
                        \hide NoteHead                                                               %! baca.glissando():abjad.glissando(1)
                        \override Accidental.stencil = ##f                                           %! baca.glissando():abjad.glissando(1)
                        \override NoteColumn.glissando-skip = ##t                                    %! baca.glissando():abjad.glissando(1)
                        \override NoteHead.no-ledgers = ##t                                          %! baca.glissando():abjad.glissando(1)
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        \revert Accidental.stencil                                                   %! baca.glissando():abjad.glissando(6)
                        \revert NoteColumn.glissando-skip                                            %! baca.glissando():abjad.glissando(6)
                        \revert NoteHead.no-ledgers                                                  %! baca.glissando():abjad.glissando(6)
                        \undo \hide NoteHead                                                         %! baca.glissando():abjad.glissando(6)
                        fs''16
                        ]
                        \revert Glissando.thickness                                                  %! baca.glissando_thickness():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    start_ = abjad.NamedPitch(start)
    stop_ = abjad.NamedPitch(stop)
    return StaffPositionInterpolationCommand(
        start_,
        stop_,
        mock=mock,
        pitches_instead_of_staff_positions=True,
        selector=selector,
    )


def interpolate_staff_positions(
    start: typing.Union[int, abjad.StaffPosition],
    stop: typing.Union[int, abjad.StaffPosition],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    mock: bool = None,
) -> StaffPositionInterpolationCommand:
    r"""
    Interpolates from ``start`` staff position to ``stop`` staff position.
    """
    start_ = abjad.StaffPosition(start)
    stop_ = abjad.StaffPosition(stop)
    return StaffPositionInterpolationCommand(
        start_, stop_, mock=mock, selector=selector
    )


def levine_multiphonic(n: int) -> abjad.Markup:
    """
    Makes Levine multiphonic markup.
    """
    assert isinstance(n, int), repr(n)
    return abjad.Markup(rf'\baca-boxed-markup "L.{n}"', literal=True)


def loop(
    items: typing.Sequence,
    intervals: typing.Sequence,
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> PitchCommand:
    """
    Loops ``items`` at ``intervals``.
    """
    loop = Loop(items=items, intervals=intervals)
    return pitches(loop, selector=selector)


def natural_clusters(
    widths: typing.Sequence[int],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
) -> ClusterCommand:
    """
    Makes natural clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(
        hide_flat_markup=True,
        selector=selector,
        start_pitch=start_pitch,
        widths=widths,
    )


def pitch(
    pitch,
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    allow_out_of_range: bool = None,
    allow_repitch: bool = None,
    mock: bool = None,
    do_not_transpose: bool = None,
    persist: str = None,
) -> PitchCommand:
    r"""
    Makes pitch command.

    ..  container:: example

        REGRESSION. Preserves duration multipliers when leaves cast from one
        type to another (note to chord in this example):

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.rhythm(
        ...         rmakers.note(),
        ...         rmakers.written_duration(1),
        ...     ),
        ...     baca.pitch("<C4 D4 E4>"),
        ... )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"                             %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"                             %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """
    if isinstance(pitch, (list, tuple)) and len(pitch) == 1:
        raise Exception(f"one-note chord {pitch!r}?")
    if allow_out_of_range not in (None, True, False):
        raise Exception(
            f"allow_out_of_range must be boolean (not {allow_out_of_range!r})."
        )
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        cyclic=True,
        do_not_transpose=do_not_transpose,
        mock=mock,
        persist=persist,
        pitches=[pitch],
        selector=selector,
    )


def pitches(
    pitches,
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    allow_octaves: bool = None,
    allow_repeats: bool = None,
    allow_repitch: bool = None,
    mock: bool = None,
    do_not_transpose: bool = None,
    exact: bool = None,
    ignore_incomplete: bool = None,
    persist: str = None,
) -> PitchCommand:
    """
    Makes pitch command.
    """
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception(
            f"ignore_incomplete must be boolean (not {ignore_incomplete!r})."
        )
    if ignore_incomplete is True and not persist:
        raise Exception("ignore_incomplete is ignored when persist is not set.")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        allow_repitch=allow_repitch,
        cyclic=cyclic,
        do_not_transpose=do_not_transpose,
        ignore_incomplete=ignore_incomplete,
        mock=mock,
        persist=persist,
        pitches=pitches,
        selector=selector,
    )


def register(
    start: int,
    stop: int = None,
    *,
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> typing.Union[RegisterCommand, RegisterInterpolationCommand]:
    r"""
    Octave-transposes ``selector`` output.

    ..  container:: example

        Octave-transposes all PLTs to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf4
                        ~
                        bf16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs16
                        [
                        e'16
                        ]
                        ef'4
                        ~
                        ef'16
                        r16
                        af16
                        [
                        g16
                        ]
                    }
                    \times 4/5 {
                        a16
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(baca.tuplet(1)),
        ...     baca.register(-6, selector=baca.tuplet(1)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af16
                        [
                        \abjad-color-music #'green
                        g16
                        ]
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    ..  container:: example

        Octave-transposes all PLTs to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6, 18),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs'16
                        [
                        e'16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5 {
                        a''16
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to an octave interpolated from
        -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(baca.tuplet(1)),
        ...     baca.register(-6, 18, selector=baca.tuplet(1)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af'16
                        [
                        \abjad-color-music #'green
                        g''16
                        ]
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    if stop is None:
        return RegisterCommand(
            registration=pitchclasses.Registration([("[A0, C8]", start)]),
            selector=selector,
        )
    return RegisterInterpolationCommand(
        selector=selector, start_pitch=start, stop_pitch=stop
    )


def soprano_to_octave(
    n: int, selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the highest note in the
        collection of all PLTs appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.color(baca.plts().group()),
        ...     baca.soprano_to_octave(3),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <c,, d,, bf,,>8
                        ~
                        [
                        \abjad-color-music #'green
                        <c,, d,, bf,,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        f,8
                        ~
                        [
                        \abjad-color-music #'green
                        f,32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <ef, e, fs>8
                        ~
                        [
                        \abjad-color-music #'green
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        <g,, af,>8
                        ~
                        [
                        \abjad-color-music #'green
                        <g,, af,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'green
                        a,,8
                        ~
                        [
                        \abjad-color-music #'green
                        a,,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music that such that the highest note in each
        pitched logical tie appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.soprano_to_octave(3),
        ...         map=baca.plts(),
        ...         ),
        ...     baca.color(baca.plts()),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        <c d bf>8
                        ~
                        [
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'blue
                        f8
                        ~
                        [
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        <ef, e, fs>8
                        ~
                        [
                        \abjad-color-music #'red
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'blue
                        <g, af>8
                        ~
                        [
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \abjad-color-music #'red
                        a8
                        ~
                        [
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(anchor=abjad.Up, octave_number=n, selector=selector)


def staff_position(
    argument: typing.Union[int, list, abjad.StaffPosition],
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    allow_out_of_range: bool = None,
    allow_repitch: bool = None,
    mock: bool = None,
    set_chord_pitches_equal: bool = None,
) -> StaffPositionCommand:
    """
    Makes staff position command; allows repeats.
    """
    assert isinstance(argument, (int, list, abjad.StaffPosition)), repr(argument)
    if isinstance(argument, list):
        assert all(isinstance(_, (int, abjad.StaffPosition)) for _ in argument)
    return StaffPositionCommand(
        [argument],
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        mock=mock,
        selector=selector,
        set_chord_pitches_equal=set_chord_pitches_equal,
    )


def staff_positions(
    numbers,
    selector: abjad.Expression = classes.select().plts(exclude=const.HIDDEN),
    *,
    allow_out_of_range: bool = None,
    allow_repeats: bool = None,
    mock: bool = None,
    exact: bool = None,
) -> StaffPositionCommand:
    """
    Makes staff position command; does not allow repeats.
    """
    if allow_repeats is None and len(numbers) == 1:
        allow_repeats = True
    return StaffPositionCommand(
        numbers,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=allow_repeats,
        exact=exact,
        mock=mock,
        selector=selector,
    )

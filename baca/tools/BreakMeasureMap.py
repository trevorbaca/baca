import abjad
import baca
import typing
from .Command import Command
from .LBSD import LBSD


class BreakMeasureMap(abjad.AbjadObject):
    r'''Breaks measure map.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
        ...     breaks=baca.breaks(baca.page([1, 0, (10, 20,)])),
        ...     )

        >>> maker(
        ...     baca.scope('ViolinMusicVoice'),
        ...     baca.make_even_runs(),
        ...     baca.pitch('E4'),
        ...     )
        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \autoPageBreaksOff                                                           %! BMM1:BREAK
                        \noBreak                                                                     %! BMM2:BREAK
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                        #'((Y-offset . 0) (alignment-distances . (10 20)))                           %! IC:BREAK
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        \pageBreak                                                                   %! IC:BREAK
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \noBreak                                                                     %! BMM2:BREAK
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \noBreak                                                                     %! BMM2:BREAK
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \noBreak                                                                     %! BMM2:BREAK
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \noBreak                                                                     %! BMM2:BREAK
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context StringSectionStaffGroup = "String Section Staff Group"
                    <<
                        \tag Violin                                                                  %! ST4
                        \context ViolinMusicStaff = "ViolinMusicStaff"
                        {
                            \context ViolinMusicVoice = "ViolinMusicVoice"
                            {
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 1]                                   %! SM4
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Violin                                                   %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                            %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Vn.                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                            %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \clef "treble"                                                   %! SM8:DEFAULT_CLEF:ST3
                                    \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                    \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                %@% \override ViolinMusicStaff.Clef.color = ##f                      %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                    \set ViolinMusicStaff.forceClef = ##t                            %! SM8:DEFAULT_CLEF:SM33:ST3
                                    e'8
                                    [
                                    ^ \markup {                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        \with-color                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            #(x11-color 'DarkViolet)                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            (Violin)                                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        }                                                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Violin                                                   %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Vn.                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 2]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 3]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 4]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 5]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
            <BLANKLINE>
                                }
                            }
                        }
                        \tag Viola                                                                   %! ST4
                        \context ViolaMusicStaff = "ViolaMusicStaff"
                        {
                            \context ViolaMusicVoice = "ViolaMusicVoice"
                            {
            <BLANKLINE>
                                % [ViolaMusicVoice measure 1]                                        %! SM4
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Viola                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Va.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "alto"                                                         %! SM8:DEFAULT_CLEF:ST3
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolaMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                R1 * 1/2
                                ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Viola)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Viola                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Va.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
            <BLANKLINE>
                                % [ViolaMusicVoice measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [ViolaMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [ViolaMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [ViolaMusicVoice measure 5]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                            }
                        }
                        \tag Cello                                                                   %! ST4
                        \context CelloMusicStaff = "CelloMusicStaff"
                        {
                            \context CelloMusicVoice = "CelloMusicVoice"
                            {
            <BLANKLINE>
                                % [CelloMusicVoice measure 1]                                        %! SM4
                                \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Cello                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Vc.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "bass"                                                         %! SM8:DEFAULT_CLEF:ST3
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set CelloMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                R1 * 1/2
                                ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Cello)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Cello                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Vc.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
            <BLANKLINE>
                                % [CelloMusicVoice measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [CelloMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [CelloMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [CelloMusicVoice measure 5]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_bol_measure_numbers',
        '_commands',
        '_deactivate',
        '_tags',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, commands=None, deactivate=None, tags=None):
        tags = tags or []
        assert baca.Command._are_valid_tags(tags), repr(tags)
        if abjad.tags.BREAK not in tags:
            tags.append(abjad.tags.BREAK)
        self._tags = tags
        self._bol_measure_numbers = []
        self._deactivate = deactivate
        if commands is not None:
            commands_ = abjad.OrderedDict()
            for measure_number, list_ in commands.items():
                commands_[measure_number] = []
                for command in list_:
                    command_ = abjad.new(
                        command,
                        deactivate=self.deactivate,
                        tags=self.tags,
                        )
                    commands_[measure_number].append(command_)
            commands = commands_
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, context=None) -> None:
        r'''Calls map on `context`.
        '''
        if context is None:
            return
        skips = baca.select(context).skips()
        measure_count = len(skips)
        last_measure_number = self.first_measure_number + measure_count - 1
        literal = abjad.LilyPondLiteral(r'\autoPageBreaksOff', 'before')
        abjad.attach(
            literal,
            skips[0],
            deactivate=self.deactivate,
            tag=self.tag.prepend('BMM1'),
            )
        for skip in skips:
            if not abjad.inspect(skip).has_indicator(LBSD):
                literal = abjad.LilyPondLiteral(r'\noBreak', 'before')
                abjad.attach(
                    literal,
                    skip,
                    deactivate=self.deactivate,
                    tag=self.tag.prepend('BMM2'),
                    )
        for measure_number, commands in self.commands.items():
            if last_measure_number < measure_number:
                message = f'score ends at measure {last_measure_number}'
                message += f' (not {measure_number}).'
                raise Exception(message)
            for command in commands:
                command(context)

    ### PUBLIC PROPERTIES ###

    @property
    def bol_measure_numbers(self) -> typing.List[int]:
        r'''Gets beginning-of-line measure numbers.

        Populated during ``baca.breaks()`` initialization.
        '''
        return  self._bol_measure_numbers

    @property
    def commands(self) -> abjad.OrderedDict:
        r'''Gets commands.
        '''
        return self._commands

    @property
    def deactivate(self) -> typing.Optional[bool]:
        r'''Is true when tags should write deactivated.
        '''
        return self._deactivate

    @property
    def first_measure_number(self) -> int:
        r'''Gets first measure number.
        '''
        return self.bol_measure_numbers[0]

    @property
    def tag(self) -> typing.Optional[abjad.Tag]:
        r'''Gets tag.
        '''
        if self.tags:
            return abjad.Tag.from_words(self.tags)
        return None

    @property
    def tags(self) -> typing.List[str]:
        r'''Gets tags.
        '''
        assert Command._are_valid_tags(self._tags), repr(self._tags)
        return self._tags[:]

#(set-global-staff-size 16)

\paper {
    print-first-page-number = ##f
    print-page-number = ##f
    system-system-spacing.minimum-distance = 24
}

\header {
    tagline = ##f
}

\layout {
    \accidentalStyle forget
    indent = 10
    ragged-bottom = ##t
    ragged-last = ##t
    ragged-right = ##t
}

%%% CONTEXTS %%%

\layout {

    % GLOBAL SKIPS
    \context {
        \name GlobalSkips
        \type Engraver_group
        \consists Staff_symbol_engraver
        \consists Script_engraver
        \consists Text_engraver
        \consists Text_spanner_engraver
        \override StaffSymbol.stencil = ##f
        %\override TextScript.outside-staff-priority = 600
        %\override TextScript.staff-padding = 3
        %\override TextSpanner.bound-details.right.attach-dir = #LEFT
        %\override TextSpanner.staff-padding = 4
        }

    % GLOBAL RESTS
    \context {
        \name GlobalRests
        \type Engraver_group
        \consists Multi_measure_rest_engraver
        \override MultiMeasureRest.transparent = ##t
        \override MultiMeasureRestText.font-size = 3
        \override MultiMeasureRestText.outside-staff-priority = 0
        \override MultiMeasureRestText.padding = 0
        }

    % GLOBAL CONTEXT
    \context {
        \name GlobalContext
        \type Engraver_group
        \consists Axis_group_engraver
        \consists Mark_engraver
        \consists Metronome_mark_engraver
        \consists Time_signature_engraver
        \accepts GlobalRests
        \accepts GlobalSkips
        %\override MetronomeMark.X-extent = #'(0 . 0)
        %\override MetronomeMark.Y-extent = #'(0 . 0)
        %\override MetronomeMark.break-align-symbols = #'(left-edge)
        %\override MetronomeMark.extra-offset = #'(0 . 4)
        %\override MetronomeMark.font-size = 3
        % in red because custom scores format all metronome marks as markup:
        \override MetronomeMark.color = #red
        \override RehearsalMark.X-extent = #'(0 . 0)
        \override RehearsalMark.Y-offset = -2.25
        \override RehearsalMark.X-offset = 6
        \override RehearsalMark.break-align-symbols = #'(time-signature)
        \override RehearsalMark.break-visibility = #end-of-line-invisible
        \override RehearsalMark.font-name = "Didot"
        \override RehearsalMark.font-size = 10
        \override RehearsalMark.outside-staff-priority = 200
        \override RehearsalMark.self-alignment-X = #center
        \override TimeSignature.X-extent = #'(0 . 0)
        \override TimeSignature.break-align-symbol = #'left-edge
        \override TimeSignature.break-visibility = #end-of-line-invisible
        \override TimeSignature.space-alist.clef = #'(extra-space . 0.5)
        \override TimeSignature.style = #'numbered
        \override VerticalAxisGroup.default-staff-staff-spacing.minimum-distance = 12
        \override VerticalAxisGroup.minimum-Y-extent = #'(-4 . 4)
    }

    % STAFF
    \context {
        \Staff
        \remove Time_signature_engraver
    }

    % MUSIC CONTEXT
    \context {
        \name MusicContext
        \type Engraver_group
        \consists System_start_delimiter_engraver
        \accepts StaffGroup
    }

    % SCORE
    \context {
        \Score
        \accepts GlobalContext
        \accepts MusicContext
        \remove Bar_number_engraver
        \remove Mark_engraver
        \remove Metronome_mark_engraver
        \remove System_start_delimiter_engraver
        \override BarLine.hair-thickness = 0.5
        \override Beam.breakable = ##t
        \override Beam.damping = 99
        \override DynamicLineSpanner.Y-extent = #'(-4 . 4)
        \override DynamicLineSpanner.padding = #1.5
        \override Glissando.breakable = ##t
        \override Glissando.thickness = 3
        \override NoteCollision.merge-differently-dotted = ##t
        \override NoteColumn.ignore-collision = ##t
        \shape #'((-2 . 0) (-1 . 0) (-0.5 . 0) (0 . 0)) RepeatTie                 
        \override RepeatTie.X-extent = ##f
        \override SpacingSpanner.strict-grace-spacing = ##t
        \override SpacingSpanner.strict-note-spacing = ##t
        \override SpacingSpanner.uniform-stretching = ##t
        \override StemTremolo.beam-width = 1.5
        \override StemTremolo.flag-count = 4
        \override StemTremolo.slope = 0.5
        \override TextScript.padding = 1
        \override TextScript.X-extent = ##f
        \override TextScript.Y-extent = #'(-1.5 . 1.5)
        \override TrillSpanner.bound-details.right.padding = 2
        \override TupletBracket.breakable = ##t
        \override TupletBracket.full-length-to-extent = ##f
        \override TupletBracket.padding = 2
        \override TupletNumber.text = #tuplet-number::calc-fraction-text
        autoBeaming = ##f
        markFormatter = #format-mark-box-alphabet
        proportionalNotationDuration = #(ly:make-moment 1 16)
        tupletFullLength = ##t
    }

}
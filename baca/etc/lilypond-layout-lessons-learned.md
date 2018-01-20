LILYPOND LAYOUT LESSONS LEARNED
===============================

1.  WARNING: setting multimeasure rest text PADDING large ...

    \override MultiMeasureRestText.padding = 10

    ... causes LilyPond to go haywire with the Y-offset values
    set explicitly on NonMusicalPaperColumn.line-break-system-details.

    This destroys explicit page layout of systems.

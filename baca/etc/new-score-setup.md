0.  Apply any OS updates with (Apple menu > App Store ... > Updates).

1.  Change to abjad directory.

    Run "pip install -e .".

    Run "ajv api -M; ajv doctest; py.test -rf".

    Change to the experimental directory.

    Run "ajv api -X; ajv doctest; py.test -rf".

    Change to the IDE directory.

    Run "pip install -e .".

    Run "ajv api -I; ajv doctest; py.test -rf".

2.  Decide the title of the score.
    Decide the name of the score package.

3.  Use IDE (new) to create the score package.
    IDE supplies title and year metadata.
    [TODO: include 'composer' metadata automatically score __metadata__py.]

4.  Edit score metadata by hand with (meta).
    For example:
    metadata = abjad.datastructuretools.TypedOrderedDict(
        [
            ('catalog_number', 'AWN-015'),
            ('composer', 'Ba\xc4\x8da'), # TODO: include automatically
            ('forces_tagline', 'for eight players'),
            ('paper_dimensions', '17 x 11 in'), # remove
            ('price', '\\$80 / \\euro 72'), # remove
            ('title', 'Fabergé Investigations'),
            ('year', 2016),
            ]
        )
    [TODO: remove paper dimensions.]
    [TODO: remove price.]
    NOTE: score title will note yet appear in IDE main screen output.

5.  Quit the IDE.
    Edit ~/.profile and add score package navigation aliases.
    For example:
        export FABERGE=$SCORES/faberge
        alias fabx="clear; cd $FABERGE/faberge"
        alias fab="fabx; start-abjad-ide fab"
    Quit the terminal.
    Restart the terminal.

6.  Change to score package score directory in all three terminal windows.
    Save terminal windows as a group.
    Use window group when terminal starts.
    Restart the terminal.

7.  Start the IDE at new score. For example: "fab".
    Create new to-do.txt file with (ee > new > to-do.txt).

8.  Create new stages.txt file with (ee > new > stages.txt).

9.  Edit stages.txt and define score stages verbally.
    Commit with (ci): "Started new score."
    [TODO: does full score title appear in IDE after commit?]

9.5 TODO: update abjad/.../example_score/tools/ScoreTemplate.py.
    Remove 'from abjad import Score, Staff, Voice'.
    Remove 'from abjad.tools import abctools'.
    Use 'import abjad' instead.

9.6 TODO: update abjad/.../example_score/tools/SegmentMaker.py.
    Remove 'from abjad.tools import abctools'.
    Remove 'from abjad.tools import lilypondfiletools'.
    Use 'import abjad' instead.

10. Copy an existing score template with (oo > cp).
    Edit ScoreTemplate.py by hand.
    Define instruments in score order.
    Make only one (master) score template per score.
    Run (dt).

11. Copy an existing instruments package with (mm > cp).
    Edit instruments/definition.py by hand.
    Define instruments in score order.
    Run (dfk).
    Eventually run (pdfm).

12. Copy an existing tempi package with (mm > cp).
    Edit tempi/definition.py by hand.
    Define tempi alphabetically by tempo name.
    Run (dfk).
    Eventually run (pdfm).

13. If required copy an existing time signatures package with (mm > cp).
    Edit time_signatures/definition.py by hand.
    Run (dfk).
    Eventually run (pdfm).

14. Change to the stylesheets directory with (yy).
    Leave IDE-generated nonfirst-segment.ily as is.

15. Copy an existing default-instrument-names.ily with (yy > cp).
    Edit default-instrument-names.ily by hand.
    Define default instrument names in score order.
    Insert blank lines between pairs of definitions.
    Define only one default instrument name per player; ignore doublings.
    (No method exists to check LilyPond stylesheet edits.)
    (Probably IDE can create default-instrument-names.ily automatically.)

16. Replace IDE-generated stylesheet.ily with existing stylesheet.ily.
    Copy existing stylesheet.ily with (yy > cp).
    Edit stylesheet.ily by hand.
    Define generic contexts first; then define score contexts in score order.
    Make sure stylesheet includes ...
        \override TextScript.font-name = #"Palatino"
    ... in the Score context to stop LaTeX's pdfpages fl ligature problems.
    (No method exists to check LilyPond stylesheet edits.)
    (Eventually create much of stylesheet.ily from ScoreTemplate.py.)

17. If parts will be produced:
    Copy existing parts.ily with (yy > cp).
    Edit parts.ily by hand.
    Probably no editing will be required.

18. Copy existing abbreviations file with (mm > cp).
    Edit __abbreviations__.py by hand.
    Define voices in score order.
    Run (!python __abbreviations__.py).
    Run (dt).
    Run (pt).
    Commit changes to score package:
    "Defined score template, instruments and stylesheet."

19. Create all segments with yet-to-be-implemented (gg > setup).
    To define 'name' by hand:
        metadata = collections.OrderedDict([
            ('name', 'K'),
            ])
    To create segments by hand:
    (gg > new > segment__introduction > meta > define 'name' by hand)
    (gg > new > segment_a > meta > define 'name' by hand)
    ...
    (gg > new > segment_q > meta > define 'name' by hand)
    NOTE: change 'segment_introduction' to 'segment__introduction', if needed.

20. Define stub version of first segment.
    Go to (%introduction).
    Copy an existing definition.py with (cp).
    Edit introduction/definition.py by hand.
    Define figure infrastructure if figure-oriented.
    Define segment-maker.
    If time signature-originated, define no music.
    If figure-originated, define only one figure.
    Run (pdfm) repeatedly until PDF renders successfully.
    Check title typography.
    Edit stylesheet.ily with (@sty).
    Check instrument names and short instrument names.
    Edit materials/instruments/definition.py with (@instr).
    Check (lpg) to make sure no errors or warnings appear in LilyPong log.
    
21. Define stub version of nonfirst segment.
    Go to (%A).
    Copy an existing definition.py with (cp).
    Edit introduction/definition.py by hand.
    Define segment-maker.
    Do not define time or color.
    Supply enough time signatures to create two (or more) pages of music.
    This will allow stylesheet footer-checking when stub score is built.
    Run (pdfm) repeatedly until PDF renders successfully.
    Footers will not appear in the output PDF.
    But footers will appear when stub score is built.
    Make sure that no blue-colored default instrument names appear.
    Check (lpg) to make sure no errors or warnings appear in LilyPong log.

22. Build stub version of score with yet-to-be-implemented (bb > setup).
    (Until then: 
        !trash assets
        !trash segments
        !trash parts.ily
        !trash segments.ily
        lyc > rf
        fcg > pg > mg > bcg > sg
        Edit music.ly by hand; comment-out not-yet-created segments
        fci > pi > mi > bci > si
        )
    Run (lyc > mi > si). Debug as necessary.
    Call (score.pdf) to inspect stub score.
    Check footers on pages two and greater; edit (@sty) as necessary.

23. Go to score directory with (ss).
    Run (dt).
    Run (pt).
    Use (ci) to commit changes to score package: "Built stub segments."
    Quit the IDE.

24. In the terminal, change to baca package with (cdb).
    Run 'ajv doctest; py.test -rf'.
    Commit changes to baca package.

25. Change to _docs package with (cds > cd _docs).
    Run build_scores_api.py.
    Commit changes to _docs package: "Rebuilt docs."

26. Change to the abjad directory.
    Run "ajv api -M; ajv doctest; py.test -rf".
    Change to the experimental directory.
    Run "ajv api -X; ajv doctest; py.test -rf".
    Change to the IDE directory.
    Run "ajv api -I; ajv doctest; py.test -rf".

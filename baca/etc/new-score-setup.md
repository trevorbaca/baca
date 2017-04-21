1.  Apply OS updates:

        Apple menu > App Store ... > Updates

2.  Check status:

        pull_all

        (st*)

        (up*)

3.  Run tests under Python 3:

        workon abjad3

    Change to the abjad directory:

        abjad api -M; ajv doctest; py.test -rf; git st
        
    Change to the experimental directory:

        abjad api -M; ajv doctest; py.test -rf; git st

    Change to the IDE diretory:

        abjad api -M; ajv doctest; py.test -rf; git st

    Change to the Bača directory:

        make_baca_api.py; ajv doctest; py.test -rf; git st

4.  Run tests under Python 2:

        workon abjad2

    Change to the abjad directory:

        abjad api -M; ajv doctest; py.test -rf; git st
        
    Change to the experimental directory:

        abjad api -M; ajv doctest; py.test -rf; git st

    Change to the IDE diretory:

        abjad api -M; ajv doctest; py.test -rf; git st

    Change to the Bača directory:

        make_baca_api.py; ajv doctest; py.test -rf; git st

5.  Change back to Python 3:

        workon abjad3

6.  Update Abjad.

    Change back to the Abjad directory:

        pip install -e .

        ajv api -M; ajv doctest; py.test -rf; git st

    Change to the experimental directory:

        ajv api -X; ajv doctest; py.test -rf; git st

7.  Update the IDE.

    Change back to the IDE directory:

        pip install -e .

        ajv api -I; ajv doctest; py.test -rf; git st

8.  Update Bača.

    Change to Bača directory:

        git pull

        make_baca_api.py; ajv doctest; py.test -rf; git st

9.  Test all scores:

    Start IDE. For every score:

        (gg > pdfm*)

        (tests)

10. Decide the title of the score.

    Decide the name of the score package.

11. Go to www.github.com.

    Click "New Repository".

    Name the repository.

    Add description:

        Stirrings Still (2017) for narrator and string quartet

    Allow repository to be public.

    Check "Initialze this repository with a README".

    Do not add a .gitignore.

    Do not add license.

    Click "Create Repository".

12. Click "Clone or download".

    Copy repository URL with clipboard icon.

13. Return to terminal and clone repository:

        https://github.com/trevorbaca/stirrings.git

14. Use IDE `(new)` to create the score package.

    TODO: teach IDE to prompt for newly created repository.

15. IDE includes composer, title and year metadata automatically.

    Add catalog number and forces tagline metadata with `(meta)`:

        metadata = abjad.datastructuretools.TypedOrderedDict(
            [
                ('catalog_number', 'AWN-018'),
                ('composer', 'Bača'),
                ('forces_tagline', 'for narrator \& string quartet'),
                ('title', 'Stirrings Still'),
                ('year', 2017),
                ]
            )

16. Change to the outer directory with `(ww)`.

    Copy Git ignore file from existing score.

17. Quit the IDE and list score packages.

    Rename newly created score package if necessary.

    Change outer directory and inner directory.

    Change score package __init__.py:

        from stirrings_still import tools
        from stirrings_still import materials
        from stirrings_still import segments

    To:

        from stirrings import tools
        from stirrings import materials
        from stirrings import segments

    TODO: teach IDE to execute last step automatically.

18. Quit the IDE. Edit `~/.profile` and add score package navigation aliases:

        export STIRRINGS=$SCORES/stirrings
        alias stix="clear; cd $STIRRINGS/stirrings"
        alias sti="stix; start-abjad-ide sti"

    Quit and restart the terminal.

19. Change to score package score directory in all three terminal windows.

    Save terminal windows as a group:

        Window > Save Windows as Group ...

    Use window group when terminal starts.

    Quit and restart the terminal.

    Start the IDE at new score.

20. Make etc files:

    Make to-do.md file with `(ee > new > to-do.md)`. 

    Make stages.md file with `(ee > new > stages.md)`.

    Commit.

21. Copy an existing score template with (oo > cp).

    Edit ScoreTemplate.py by hand.

    Define instruments in score order.

    Make only one (master) score template per score.

    Run (dt).

22. Copy an existing instruments package with (mm > cp).

    Edit instruments/definition.py by hand.

    Define instruments in score order.

    Run (dfk).

    Eventually run (pdfm).

23. Copy an existing tempi package with (mm > cp).

    Edit tempi/definition.py by hand.

    Define tempi alphabetically by tempo name.

    Run (dfk).

    Eventually run (pdfm).

24. If required copy an existing time signatures package with (mm > cp).

    Edit time_signatures/definition.py by hand.

    Run (dfk).

    Eventually run (pdfm).

25. Change to the stylesheets directory with (yy).

    Leave IDE-generated nonfirst-segment.ily as is.

26. Copy an existing default-instrument-names.ily with (yy > cp).

    Edit default-instrument-names.ily by hand.

    Define default instrument names in score order.

    Insert blank lines between pairs of definitions.

    Define only one default instrument name per player; ignore doublings.

    (No method exists to check LilyPond stylesheet edits.)

    (Probably IDE can create default-instrument-names.ily automatically.)

27. Replace IDE-generated stylesheet.ily with existing stylesheet.ily.

    Copy existing stylesheet.ily with (yy > cp).

    Edit stylesheet.ily by hand.

    Define generic contexts first; then define score contexts in score order.

    Make sure stylesheet includes ...

        \override TextScript.font-name = #"Palatino"

    ... in the Score context to stop LaTeX's pdfpages fl ligature problems.

    (No method exists to check LilyPond stylesheet edits.)

    (Eventually create much of stylesheet.ily from ScoreTemplate.py.)

28. If parts will be produced:

        Copy existing parts.ily with (yy > cp).
        Edit parts.ily by hand.

    Probably no editing will be required.

29. Test and commit:

    Run (dt).

    Run (pt).

    Commit changes to score package:

    "Defined score template, instruments and stylesheet."

30. Edit stages.txt and define score stages verbally.

31. Create all segments with yet-to-be-implemented (gg > setup).

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

32. Define stub version of first segment.

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
    
33. Define stub version of nonfirst segment.

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

34. Build stub version of score with yet-to-be-implemented (bb > setup).

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

35. Go to score directory with (ss).

    Run (dt).

    Run (pt).

    Use (ci) to commit changes to score package: "Built stub segments."

    Quit the IDE.

36. In the terminal, change to baca package with (cdb).

    Run 'ajv doctest; py.test -rf'.

    Commit changes to baca package.

37. Change to _docs package with (cds > cd _docs).

    Run build_scores_api.py.

    Commit changes to _docs package: "Rebuilt docs."

38. Change to the abjad directory.

    Run "ajv api -M; ajv doctest; py.test -rf".

    Change to the experimental directory.

    Run "ajv api -X; ajv doctest; py.test -rf".

    Change to the IDE directory.

    Run "ajv api -I; ajv doctest; py.test -rf".

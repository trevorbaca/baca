NEW SCORE SETUP
===============

Revise this document during use.

Pull respositories
------------------

1.  Pull repositories:

    pull_all

2.  Test everything:

    cdj; py.test -rf

    cdb; py.test -rf

    cdi; py.test -rf
        
3.  Rebuild scores:

    ss
    >> gg ipn
    >> gg ipn
    ...

4.  Rebuild docs:

    apim

    apib

    apii

    apis

Apply software updates
----------------------

5.  Update LilyPond, TeXShop, macOS:

    lilypond.org > Unstable release.

    TeXShop > Check for updates.

    Apple menu > App Store ... > Updates.

    Sanity-check LilyPond with \new Staff { c'4 }.

6.  Test everything:

    cdj; py.test -rf

    cdb; py.test -rf

    cdi; py.test -rf

7.  Rebuild scores:

    ss
    >> gg ipn
    >> gg ipn
    ...

8.  Rebuild docs:

    apim

    apib

    apii

    apis

9.  Repeat steps above for secondary devices.

Package unpushed trevor/dev commits
-----------------------------------

10. Package unpushed trevor/dev commits:

    Follow feature management in Git workflow instructions.

    Make sure trevor/dev is empty.

11. Update Abjad:

    cd ~/abjad

    pip install -e .

    py.test -rf; apim; git st

12. Update the IDE:

    cd ~/ide

    pip install -e .

    Remove ~/.virtualenvs/abjad3/bin/start-abjad-ide

    Quit and restart the terminal.
    
    Sanity-check IDE with restart.

    py.test -rf; apii; git st

13. Update Bača:

    cd ~/baca

    git pull

    py.test -rf; apib.

14. Rebuild scores:

    ss
    >> gg ipn
    >> gg ipn
    ...

15. Rebuild docs:

    apim

    apib

    apii

    apis

Make new score package
----------------------

16. Determine repository metadata:

    Select score title.

    Select score package name.

17. Create new GitHub repository:

    Go to www.github.com.

    Click "New Repository".

    Name the repository.

    Add description: "Stirrings Still (2017) for narrator and string quartet."

    Make repository public.

    Do not initialize with README.

    Do not add .gitignore.

    Do not add license.

    Click "Create Repository."

18. Make new score package with IDE:

    (new)

    Stop IDE and respell directory names if necessary.

    nahte/nahte -> naehte/naehte

    [TODO: teach IDE to search (and prompt) for newly created repository.]

19. Add catalog number and forces tagline metadata by hand:

    metadata = abjad.OrderedDict(
        [
            ('catalog_number', 'AWN-019'),
            ('composer', 'Bača'),
            ('forces_tagline', 'for narrator \& string quartet'),
            ('title', 'Stirrings Still'),
            ('year', 2017),
            ]
        )

    IDE includes composer, title, year metadata automatically.

20. Move score package to Desktop.

    mv [score] ~/Desktop

21. Clone Github repository:

    Return to GitHub.

    Click "Clone or download."

    Copy repository URL with clipboard icon.

    Return to terminal.

    cd ~/Scores

    git clone https://github.com/trevorbaca/stirrings.git

22. Move score package contents into GitHub clone:

    (ci "Configured Python package.")
    
23. Configure wrapper directory:

    Symlink .gitignore:

        (ww)

        (!trash .gitignore)

        (!ln -s ~/baca/dotfiles/gitignore ~/Scores/my_score/.gitignore)

    Get existing .travis.yml:

        rm .travis.yml

        (ww get [score] .travis.yml)

        Edit .travis.yml by hand.

    Get existing README.md:

        rm README.md

        (ww get [score] README.md)

        Edit README.md by hand.

    Check IDE-generated wrapper files by hand:

        No requirements.txt file is necessary.

        No setup.cfg file is necessary.

        Check setup.py.

    (ci "Configured wrapper directory.")

24. Compare subpackage initializers to existing score:

    (ci "Configured package initializers.")

25. Configure score for continuous integration:

    https://travis-ci.org.

    Click "+" (next to "My Repositories) in upper left corner.

    Leads to https://travis-ci.org/profile/trevorbaca.

    Click "Sync account."

    Refresh page.

    Toggle "trevorbaca/<score>." 

    Click "settings."

    Cron jobs > interval > "daily" > add.

    Settings > "trigger custom build."

26. Verify continuous integration setup:

    Return to IDE.

    Make test commit.

    (ci "Configured contiguous integration.")

    Return to https://travis-ci.org.

    Make sure Travis lists score.

    Make sure all tests pass.

27. Add score to IDE aliases:

    (al)

28. Add score to ~/.profile:

    export STIRRINGS_STILL=$SCORES/stirrings_still
    alias stix="clear; cd $STIRRINGS_STILL/stirrings_still"
    alias sti="stix; start-abjad-ide sti"

    export PYTHONPATH=$STIRRINGS_STILL:$PYTHONPATH

    Quit and restart terminal.

29. Add repository to ~/baca/scr/restart-travis-build-set-n script.

30. Add repository to clone scores script:
    
    ~/micellaneous/config/clone_scores.py

31. Add terminal window group:

    Change to score package in three terminal windows.

    Window > Save Windows as Group ...

    Use window group when terminal starts.

    Quit and restart terminal.

32. Move sketches into etc directory:

    Restart IDE.

    Move files by hand.

    (ci "Added materials PDF, map PDF.")

33. Make etc files:

    (ee new to-do.md)

    (ee new stages.md)

    (ci "Added etc files.")

34. Set up stylesheets directory:

    Leave IDE-generated nonfirst-segment.ily as is.

    Get existing contexts.ily.

    (yy get [score] contexts.ily)

    Edit contexts.ily by hand.

    Define global contexts.
    
    Define score contexts in score order.

    (No method exists to check LilyPond stylesheet edits.)

    (Eventually create much of contexts.ily from ScoreTemplate.py.)

    Remove IDE-generated stylesheet.ily and get existing stylesheet.

    (yy rm stylesheet.ily)

    (yy get [score] stylesheet.ily).

    Edit stylesheet.ily by hand.

    Remove IDE-generated parts.ily.

    (yy rm parts.ily)

    (Eventually teach IDE more about part production.)

    (ci "Added stylesheets.")

35. Compare initializers against existing score:

    cc __init__.py

    mm __init__.py

    gg __init__.py

    oo __init__.py

36. Get existing instruments:

    (mm)

    (!trash __init__.py)

    ([source score] mm !cp __init__.py ~/Desktop)
    
    ([target score] mm !mv ~/Desktop/__init__.py .)

    Edit materials __init__.py by hand.

    (mm get [score] instruments)

    Edit materials/instruments/definition.py by hand.

    Define instruments in score order.

    (dpc)

    Add instruments to materials/__init__.py by hand.

    (ci "Added instruments.")

37. Remove IDE-generated ScoreTemplate.py:

    (oo rm ScoreTemplate.py)

    Remove IDE-generated SegmentMaker.py.

    (oo rm SegmentMaker.py)

    Get existing ScoreTemplate.py.

    (oo get [score] ScoreTemplate.py)

    Edit ScoreTemplate.py by hand.

    Replace existing package name with new package name.

    Define instruments in score order.

    Make only one master score template per score.

    (^^)

    (!apis)

    Visually inspect scores API.

    (ci "Added score template.")

    (cdsx; git add .; git commit "Rebuilt API.")

38. Get existing metronome marks:

    (mm get [score] metronome_marks)

    Edit metronome_marks/definition.py by hand.

    Define metronome marks alphabetically by metronome mark name.

    Edit materials/__init__.py by hand.

    (dpc)

    (ci "Added metronome marks.")

39. Get existing time signatures (if time-signature-oriented):

    (mm get [score] time_signatures) 

    Edit time_signatures/definition.py by hand.

    Edit materials/__init__.py by hand.

    (dpc)

    (ci "Added time signatures.")

40. Define stub version of first segment:

    (gg new A)

    (A rm definition.py get [score] definition.py)

    Edit A/definition.py by hand.

    Define figure infrastructure if figure-oriented.

    Define segment-maker.

    Define no music if time-signature-oriented.

    Define one figure if figure-oriented.

    Render PDF (ipn).

    Check title typography.

    Check instrument names.
    
    Check short instrument names.

    Check (ipn) messaging for metadata handling.

    Check (le) for LilyPond warnings.
    
41. Define stub version of second segment:

    (gg new B)

    (B rm definition.py get [score] definition.py)

    Edit definition.py by hand.

    Define segment-maker.

    Supply time signatures for two (or more) pages of music.

    This will allow stylesheet footer-checking when stub score is built.

    Render PDF.

    Footers will not appear in the output PDF.

    But footers will appear when stub score is built.

    Check short instrument names.

    Check (ipn) messaging for metadata handling.

    Check (lp) for LilyPond warnings.

    (ci "Segments A, B.")

42. Build stub version of score if ensemble piece:

    (bb new ledger) 

    (ledger)

    (lyc* mg)

    Get existing front cover.

    (rm front-cover.tex get [score] front-cover.tex)

    Check front-cover.tex by hand.

    (fci)

    Check preface.tex by hand.

    (pi)

    Check stylesheet.ily by hand.

    Check music.ly by hand.

    (mi)

    Check back-cover.tex by hand.

    (bci)

    Check score.tex by hand.

    (si)

    Check footers on pages two and greater.
    
    TODO: Teach IDE more about builds.

    (cc ^^ ++ ci "Added ledger build.")

43. Test everything:

    cdj; py.test -rf

    cdb; py.test -rf

    cdi; py.test -rf

44. Rebuild scores:

    ss
    >> gg ipn
    >> gg ipn
    ...

45. Rebuild docs:

    apim

    apib

    apii

    apis

46. Commit changes to this document:

    (ci "Updated new score setup instructions.")

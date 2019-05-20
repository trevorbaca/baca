NEW SCORE SETUP
===============

Revise this document during use.

Pull respositories
------------------

1.  Pull repositories:

    pull_all

2.  Test everything:

    (cdj .. !py.test -rf)

    (cdb .. !py.test -rf)

    (cdi .. !py.test -rf)
        
3.  Rebuild scores:

    (ss)

    (>> gg ipn)

    (>> gg ipn)

    ...

4.  Rebuild docs:

    apim

    apib

    apii

    apis

Apply software updates
----------------------

5.  Update macOS, LilyPond, TeXShop:

    Apple menu > App Store ... > Updates.

    lilypond.org > Unstable release.

        Sanity-check LilyPond with \new Staff { c'4 }.

    TeXShop > Check for updates.

6.  Test everything:

    (cdj .. !py.test -rf)

    (cdb .. !py.test -rf)

    (cdi .. !py.test -rf)

7.  Rebuild scores:

    (ss)

    (>> gg ipn)

    (>> gg ipn)

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

11. Update pip:

    pip install --upgrade pip

12. Update Sphinx and Sphinx's RTD theme:

    pip install --upgrade sphinx

    pip install --upgrade sphinx-rtd-theme

13. Update Abjad:

    cd ~/abjad

    pip install -e .

    py.test -rf; apim; git st

14. Update the IDE:

    cd ~/ide

    pip install -e .

    Remove ~/.virtualenvs/abjad3/bin/start-abjad-ide

    Quit and restart the terminal.
    
    Sanity-check IDE with restart.

    py.test -rf; apii; git st

15. Update Bača:

    cd ~/baca

    git pull

    py.test -rf; apib; git st

16. Rebuild scores:

    (ss)

    (>> gg ipn)

    (>> gg ipn)

    ...

17. Rebuild docs:

    apim

    apib

    apii

    apis

Make new score package
----------------------

18. Select score metadata:

    Determine score title.

    Determine score package name.

19. Make new score package with IDE:

    (new)

    Stop IDE and respell directory names if necessary.

    nahte/nahte -> naehte/naehte

20. Add catalog number and forces tagline metadata by hand:

    metadata = abjad.OrderedDict(
        [
            ('catalog_number', 'AWN-020'),
            ('composer', 'Bača'),
            ('forces_tagline', 'for narrator \& nine players'),
            ('title', '(HARMONY)'),
            ('year', 2019),
            ]
        )

    IDE includes composer, title, year metadata automatically.

21. Create new GitHub repository:

    Go to www.github.com.

    Click "New Repository".

    Name the repository.

    Add description: "(HARMONY) (2019) for narrator and nine players."

    Make repository public.

    Do not initialize with README.

    Do not add .gitignore.

    Do not add license.

    Click "Create Repository."

22. Initialize IDE-created directory as GitHub repository:

    cd ~/Scores/harmony

    git init

    git add .
    
    git commit

    git remote add origin https://github.com/trevorbaca/harmony.git

    git push -u origin master

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

    Check IDE-generated wrapper files by hand.

        No requirements.txt file is necessary.

        No setup.cfg file is necessary.

        Check setup.py in comparison to existing score package.

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "Configured wrapper directory.")

24. Compare subpackage initializers to existing score:

    cc __init__.py

    mm __init__.py

    gg __init__.py

    oo __init__.py

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "Configured package initializers.")

25. Remove IDE-generated segment-maker:

    (oo)

    (rm SegmentMaker.py)

26. Run mypy:

    (ww)

    (!mypy harmony)

27. Configure score for continuous integration:

    https://travis-ci.org.

    Click "+" (next to "My Repositories) in upper left corner.

    Leads to https://travis-ci.org/profile/trevorbaca.

    Click "Sync account."

    Refresh page.

    Toggle "trevorbaca/<score>." 

    Click "settings."

    Cron jobs > interval > "daily" > add.

    More options > "Trigger build".

28. Verify continuous integration setup:

    Return to IDE.

    Make test commit.

    (ci "Configured contiguous integration.")

    Return to https://travis-ci.org.

    Make sure Travis lists score.

    Make sure all tests pass.

29. Add score to IDE aliases:

    (al)

30. Add score to ~/.profile:

    export harmony=$SCORES/harmony
    alias stix="clear; cd $harmony/harmony"
    alias sti="stix; start-abjad-ide sti"

    export PYTHONPATH=$harmony:$PYTHONPATH

    Quit and restart terminal.

31. Add repository to ~/baca/scr/restart-travis-build-set-n script.

    cdb

    (..)

    (ci)
    
    "Taught Travis restart scripts about (HARMONY)."

32. Add repository to clone scores script:
    
    ~/micellaneous/config/clone_scores.py

    cdm

    ci "Taught score clone scripts about (HARMONY)."

33. Add test submodule:

    (cc)

    (!trash test)

    (ci "Removed test submodule.")

    (!git submodule add https://github.com/trevorbaca/test.git)

    Make sure .gitmodules file appears in wrapper directory.

    (ww)

    (!ls -a)

    (ci "Added test submodule.")

34. Move sketches into etc directory:

    Restart IDE.

    Move files by hand.

    (ci "Added materials PDF, map PDF.")

35. Make etc files:

    (ee new to-do.md)

    (ee new stages.md)

    (ci "Added etc files.")

36. Set up stylesheets directory:

    (yy)

    Leave IDE-generated nonfirst-segment.ily as is.

    Remove IDE-generated contexts.ily and get existing contexts.ily.

        (yy rm contexts.ily remove)
        
        (yy get [score] contexts.ily)

        Edit contexts.ily by hand.

            Define global contexts.
            
            Define score contexts in score order.

            (No method exists to check LilyPond stylesheet edits.)

            (Eventually check against ScoreTemplate.py programmatically.)

    Remove IDE-generated stylesheet.ily and get existing stylesheet.

        (yy rm stylesheet.ily remove)

        (yy get [score] stylesheet.ily).

        Edit stylesheet.ily by hand.

    (ci "Added contexts and stylesheets.")

37. Get existing instruments:

    (mm get [score] instruments y)

    Check materials __init__.py.

        from .instruments.definition import instruments

    Check contents __init__.py.

        from harmony.materials.instruments.definition import instruments

    Edit materials/instruments/definition.py by hand.

        Define instruments in score order.

    (dpc)

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "Added instruments.")

38. Get existing margin markups:

    (mm get [score] margin_markups y)

    Check margin_markups __init__.py.

        from .margin_markups.definition import margin_markups

    Check contents __init__.py.

        from harmony.materials.margin_markups.definition import margin_markups

    Edit materials/margin_markups/definition.py by hand.

        Define margin markups in score order.

        (dpc)

    Define LilyPond margin markups.

        (yy markups.ily)

        Define margin markups in score order.

    Get existing margin_markup() function.

        (oo get [score] margin_markup.py y)

        Edit tools/margin_markup.py by hand.

        Edit tools/__init__.py by hand.

            from .margin_markup import margin_markup

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "Added margin markups.")

39. Remove IDE-generated ScoreTemplate.py:

        (oo rm ScoreTemplate.py)

    (Check to make sure IDE-generated SegmentMaker.py already removed.)

    Get existing ScoreTemplate.py.

        (oo get [score] ScoreTemplate.py)

    Edit ScoreTemplate.py by hand.

        Replace existing package name with new package name.

        Define parts in score order.

        Make only one master score template per score.

        (^^)

        (!apis)

        Visually inspect scores API to make sure score template appears.

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "Added score template.")

    (cdsx; git add .; git commit "Rebuilt API.")

40. Get existing metronome marks:

        (mm get [score] metronome_marks)

    Edit metronome_marks/definition.py by hand.

        Define metronome marks alphabetically by metronome mark name.

        Edit materials/__init__.py by hand.

        (dpc)

    Check contents __init__.py.

        from harmony.materials.metronome_marks.definition import metronome_marks

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "Added metronome marks.")

41. Get existing time signatures (if time-signature-oriented):

        (mm get [score] time_signatures) 

    Edit time_signatures/definition.py by hand.

        Edit materials/__init__.py by hand.

        (dpc)

    Check contents __init__.py.

        from harmony.materials.time_signatures.definition import time_signatures

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "Added time signatures.")

42. Define stub version of first segment:

    Make package:

        (gg new A)

        (A rm definition.py remove)
        
        (A get [score] definition.py)

        Edit A/definition.py by hand.

            Define figure infrastructure if figure-oriented.

            Define segment-maker.

            Define no music if time-signature-oriented.

            Define one figure if figure-oriented.

            Set start markup and margin markup for each part.

    Define stub layout of first segment:

        (A rm layout.py remove)

        (A get [score] layout.py)

        Edit A/layout.py by hand.

    Render PDF (ipn).

        Check (ipn) messaging for metadata handling.

        Check (le) for LilyPond warnings.

        Check title typography.

        Check instrument names.
        
        Check short instrument names.

        Check start instrument markup.

        Check margin markup.

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "A.")
    
43. Define stub version of second segment:

    Make package:

        (gg new B)

        (B rm definition.py get [score] definition.py)

    Edit definition.py by hand:

        Define segment-maker.

        Supply time signatures for two (or more) pages of music.

        This allows stylesheet footer-checking when stub score is built.

    Render PDF.

        Footers will not appear in the output PDF.

        But footers will appear when stub score is built.

        Check short instrument names.

        Check (ipn) messaging for metadata handling.

        Check (lp) for LilyPond warnings.

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony

    (ci "A, B.")

44. Build stub version of score if ensemble piece:

    (bb new score ledger-score ledger) 

    ($89 / \\euro 89)
    
    (LED y)

    (ledger-score)

    (lyc* mg)

    Make front cover:

        (rm front-cover.tex get [score] front-cover.tex)

        (fcte)

        (fcti)

    Make preface:

        (rm preface.tex get [score] preface.tex)

        (pfte)

        (pfti)

    Make layout.ly:

        (rm layout.py remove)

        (get [score] layout.py)

        (lpe)

        (llm)

    Make music.pdf:

        Check stylesheet.ily by hand:

            (sty)

        Check music.ly by hand:

            (mle)

        Interpret music.ly:

            (mli)

    Make back-cover.pdf:

        (rm back-cover.tex)

        (get [score] back-cover.tex)

        (bcte)

        (bcti)

    Make blank.pdf:

        (get [score] blank.tex)
        
        (blank.tex)

        (!xpdf blank.tex)

    Make score.pdf and insert blank pages:

        (ste)

        (sti)

        Check footers on pages two and greater.

    Check package wellformedness.

        (^^)

        cd ~

        bkr Scores/harmony

        mypy --ignore-missing-imports Scores/harmony
    
    (cc ^^ ++ ci "Added ledger build.")

45. Test everything:

    (cdj .. !py.test -rf)

    (cdb .. !py.test -rf)

    (cdi .. !py.test -rf)

46. Rebuild scores:

    (ss)

    (>> gg ipn)

    (>> gg ipn)

    ...

47. Rebuild docs:

    apim

    apib

    apii

    apis

48. Commit changes to this document:

    (ci "Updated new score setup instructions.")

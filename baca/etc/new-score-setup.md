NEW SCORE SETUP
===============

Read and revise this document.

Then follow the steps in the four areas below:

    * pull repositories; test

    * apply software updates; test

    * package unpushed trevor/dev commits; test

    * create new score package; test

Pull respositories
------------------

1.  Pull repositories.

    (!pull_all st* pull*)

    TODO: Add IDE (pull_all) command.

2.  Test and rebuild everything.

    (cdj .. !ajv api -M ^^ ++ ci)

    (cdi !ajv api -I ^^ ++ ci)

    (ll !make_baca_api.py ^^ ++ ci)
        
    cd ~/Scores; make_scores_api.py; git st; git commit "Rebuilt API."

3.  Rebuild scores.

    (mm pdfm* gg pdfm* ^^ ++)

4.  Rebuild docs.

    cd ~/abjad/abjad/docs; make clean; ajv api -M 

    cd ~/abjad-ide/ide/docs; make clean; ajv api -I

    cd ~/baca/baca/_docs; make clean; make_baca_api.py

    cd ~/Scores/_docs; make clean; make_scores_api.py

Apply software updates
----------------------

5.  Apply LilyPond, TeXShop and macOS updates.

    lilypond.org > Unstable release.

    TeXShop > Check for updates.

    Apple menu > App Store ... > Updates.

    Sanity-check LilyPond with \new Staff { c'4 }.

6.  Test and rebuild everything.

    (cdj .. !ajv api -M ^^ ++ ci)

    (cdi !ajv api -I ^^ ++ ci)

    (ll !make_baca_api.py ^^ ++ ci)
        
    cd ~/Scores; make_scores_api.py; git st; git commit "Rebuilt API."

7.  Rebuild scores.

    (mm pdfm* gg pdfm* ^^ ++)

8.  Rebuild docs.

    cd ~/abjad/abjad/docs; make clean; ajv api -M 

    cd ~/abjad-ide/ide/docs; make clean; ajv api -I

    cd ~/baca/baca/_docs; make clean; make_baca_api.py

    cd ~/Scores/_docs; make clean; make_scores_api.py

9.  Repeat steps above for secondary devices.

Package unpushed trevor/dev commits
-----------------------------------

10. Package unpushed trevor/dev commits.

    Follow feature management in Git workflow instructions.

    Make sure trevor/dev is empty.

11. Update Abjad.

    cd ~/abjad

    pip install -e .

    ajv api -M; ajv doctest; py.test -rf; git st

12. Update the IDE.

    cd ~/abjad-ide

    pip install -e .

    Remove ~/.virtualenvs/abjad3/bin/start-abjad-ide

    Quit and restart the terminal.
    
    Sanity-check IDE with restart.

    ajv api -I; ajv doctest; py.test -rf; git st

13. Update Bača.

    cd ~/baca

    git pull

    make_baca_api.py; (^^); (++); git st

    make_scores_api.py

14. Rebuild scores.

    (mm pdfm* gg pdfm* ^^ ++)

15. Rebuild docs.

    cd ~/abjad/abjad/docs; make clean; ajv api -M 

    cd ~/abjad-ide/ide/docs; make clean; ajv api -I

    cd ~/baca/baca/_docs; make clean; make_baca_api.py

    cd ~/Scores/_docs; make clean; make_scores_api.py

Make new score package
----------------------

16. Select score title.

    Select score package name.

17. Go to www.github.com.

    Click "New Repository".

    Name the repository.

    Add description: "Stirrings Still (2017) for narrator and string quartet."

    Make repository public.

    Do not initialize with README.

    Do not add .gitignore.

    Do not add license.

    Click "Create Repository."

18. Click "Clone or download."

    Copy repository URL with clipboard icon.

19. Return to terminal and clone repository.

    cd ~/Scores

    git clone https://github.com/trevorbaca/stirrings.git

20. Start IDE and create score package.

    (new)

    TODO: teach IDE to search (and prompt) for newly created repository.

21. IDE includes composer, title, year metadata automatically.

    Add catalog number and forces tagline metadata by hand.
    
        metadata = abjad.TypedOrderedDict(
            [
                ('catalog_number', 'AWN-018'),
                ('composer', 'Bača'),
                ('forces_tagline', 'for narrator \& string quartet'),
                ('title', 'Stirrings Still'),
                ('year', 2017),
                ]
            )

22. Symlink .gitignore:

    (ww)

    (!ln -s ~/baca/baca/dotfiles/gitignore ~/Scores/my_score/.gitignore)

23. Get existing .travis.yml.

    (ww get [score] .travis.yml)

    Edit .travis.yml by hand.

24. Get existing README.md.

    (ww get [score] README.md)

    Edit README.md by hand.

25. Check IDE-generated wrapper files by hand.

    requirements.txt
    setup.cfg
    setup.py

26. Compare package initializer to package initializer of existing score.

27. Commit.

    (ci "Configured Python package.")

    Visit https://github.com/trevorbaca/<score> and confirm changes.

28. Configure score for continuous integration.

    https://travis-ci.org.

    Click "+" (next to "My Repositories) in upper left corner.

    Leads to https://travis-ci.org/profile/trevorbaca.

    Click "Sync account."

    Toggle "trevorbaca/<score>." 

29. Return to IDE.

    Make test commit.

    (ci "Configured contiguous integration.")

    Return to https://travis-ci.org.

    Make sure Travis lists score.

    Make sure all tests pass.

30. Add score alias to IDE aliases.

    (al)

31. Add aliases to ~/.profile.

        export STIRRINGS_STILL=$SCORES/stirrings_still
        alias stix="clear; cd $STIRRINGS_STILL/stirrings_still"
        alias sti="stix; start-abjad-ide sti"

32. Add score package to PYTHONPATH.

    export PYTHONPATH=$STIRRINGS_STILL:$PYTHONPATH

    Quit and restart terminal.

33. Add repository to ~/baca/baca/scr/restart-travis-build-set-n script.

34. Add repository to clone scores script.
    
    .../clone_scores.py

35. Change to score package in three terminal windows.

    Window > Save Windows as Group ...

    Use window group when terminal starts.

    Quit and restart terminal.

36. Restart IDE.

    Move sketches into etc directory.

    (ci "Added materials PDF, map PDF.")

37. Make etc files.

    (ee new to-do.md)

    (ee new stages.md)

    (ci "Added etc files.")

38. Change to stylesheets directory.

    Leave IDE-generated nonfirst-segment.ily as is.

39. Get existing contexts.ily.

    (yy get [score] contexts.ily)

    Edit contexts.ily by hand.

    Define global contexts.
    
    Define score contexts in score order.

    Make sure stylesheet includes ...

        \override TextScript.font-name = #"Palatino"

    ... in the Score context to stop LaTeX's pdfpages fl ligature problems.

    (No method exists to check LilyPond stylesheet edits.)

    (Eventually create much of contexts.ily from ScoreTemplate.py.)

40. Remove IDE-generated stylesheet.ily.

    (yy rm stylesheet.ily)

    Get existing stylesheet.ily.

    (yy get [score] stylesheet.ily).

    Edit stylesheet.ily by hand.

41. Remove IDE-generated parts.ily.

    (yy rm parts.ily)

    (Eventually teach IDE more about part production.)

    (ci "Added stylesheets.")

42. Get existing instruments.

    (mm get [score] instruments)

    Edit instruments/definition.py by hand.

    Define instruments in score order.

    (dfk)

    Eventually run (pdfm).

    (ci "Added instruments.")

43. Remove IDE-generated ScoreTemplate.py.

    (oo rm ScoreTemplate.py)

    Remove IDE-generated SegmentMaker.py.

    (oo rm SegmentMaker.py)

    Get existing ScoreTemplate.py.

    (oo get [score] ScoreTemplate.py)

    Edit ScoreTemplate.py by hand.

    Replace existing package name with new package name.

    Define instruments in score order.

    Make only one master score template per score.

    (^^ !make_scores_api.py)

    Visually inspect scores API.

    (ci "Added score template.")

44. Get existing metronome marks.

    (mm get [score] metronome_marks)

    Edit metronome_marks/definition.py by hand.

    Define metronome marks alphabetically by metronome mark name.

    (dfk)

    (pdfm)

    (ci "Added metronome marks.")

45. Get existing time signatures (if time-signature-oriented).

    (mm get [score] time_signatures) 

    Edit time_signatures/definition.py by hand.

    (dfk)

    (ci "Added time signatures.")

46. Define stub version of first segment.

    (gg new _)

    (_ rm definition.py get [score] definition.py)

    Edit _/definition.py by hand.

    Define figure infrastructure if figure-oriented.

    Define segment-maker.

    Define no music if time-signature-oriented.

    Define one figure if figure-oriented.

    Render PDF.

    Check title typography.

    Check instrument names.
    
    Check short instrument names.

    Check (pdfm) messaging for metadata handling.

    Check (lp) for LilyPond warnings.
    
47. Define stub version of second segment.

    (gg new A)

    (A rm definition.py get [score] definition.py)

    Edit definition.py by hand.

    Define segment-maker.

    Supply time signatures for two (or more) pages of music.

    This will allow stylesheet footer-checking when stub score is built.

    Render PDF.

    Footers will not appear in the output PDF.

    But footers will appear when stub score is built.

    Check short instrument names.

    Check (pdfm) messaging for metadata handling.

    Check (lp) for LilyPond warnings.

    (ci "Segments _, A.")

48. Build stub version of score.

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

49. Test and rebuild everything.

    (cdj .. !ajv api -M ^^ ++ ci)

    (cdi !ajv api -I ^^ ++ ci)

    (ll !make_baca_api.py ^^ ++ ci)
        
    cd ~/Scores; make_scores_api.py; git st; git commit "Rebuilt API."

50. Rebuild scores.

    (mm pdfm* gg pdfm* ^^ ++)

51. Rebuild docs.

    cd ~/abjad/abjad/docs; make clean; ajv api -M 

    cd ~/abjad-ide/ide/docs; make clean; ajv api -I

    cd ~/baca/baca/_docs; make clean; make_baca_api.py

    cd ~/Scores/_docs; make clean; make_scores_api.py

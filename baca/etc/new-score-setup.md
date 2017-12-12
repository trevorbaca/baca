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

    (!pull_all)

    (st*)

    (up*)

    TODO: Add IDE (pull_all) command.

2.  Test and rebuild everything.

    (cdj .. !ajv api -M ^^ ++ ci)

    (cdi !ajv api -I ^^ ++ ci)

    (ll !make_baca_api.py ^^ ++ ci)
        
    cd ~/Scores; make_scores_api.py; git st; git commit "Rebuilt API."

3.  Rebuild scores.

    (mm > pdfm*)

    (gg > pdfm*)

    (^^)

    (++)

4.  Rebuild docs make clean.

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

    (cdj ..)

    (!ajv api -M)

    (^^ ++ ci)

    (cdi)

    (!ajv api -I)

    (^^ ++ ci)

    (ll make_baca_api.py)

    (^^ ++ ci)
        
    (q)

    cd ~/Scores; make_scores_api.py; git st; git commit "Rebuilt API."

7.  Rebuild scores.

    (mm > pdfm*)

    (gg > pdfm*)

    (^^)

    (++)

8.  Rebuild docs make clean.

    cd ~/abjad/abjad/docs; make clean; ajv api -M 

    cd ~/abjad-ide/ide/docs; make clean; ajv api -I

    cd ~/baca/baca/_docs; make clean; make_baca_api.py

    cd ~/Scores/_docs; make clean; make_scores_api.py

9.  Repeat steps above for secondary devices.

Package unpushed trevor/dev commits
-----------------------------------

10. Package unpushed trevor/dev commits.

    Follow feature management in Git workflow instructions.
    ... 

    Make sure trevor/dev is empty.

11. Update Abjad.

    cd ~/abjad

    pip install -e .

    ajv api -M; ajv doctest; py.test -rf; git st

12. Update the IDE.

    cd ~/abjad-ide

    pip install -e .

    ajv api -I; ajv doctest; py.test -rf; git st

13. Update Bača.

    cd ~/baca

    git pull

    make_baca_api.py; (^^); (++); git st

    make_scores_api.py

15. Rebuild scores.

    (mm > pdfm*)

    (gg > pdfm*)

    (^^)

    (++)

16. Rebuild docs make clean.

    cd ~/abjad/abjad/docs; make clean; ajv api -M 

    cd ~/abjad-ide/ide/docs; make clean; ajv api -I

    cd ~/baca/baca/_docs; make clean; make_baca_api.py

    cd ~/Scores/_docs; make clean; make_scores_api.py

Make new score package
----------------------

17. Select score title.

    Select score package name.

18. Go to www.github.com.

    Click "New Repository".

    Name the repository.

    Add description: "Stirrings Still (2017) for narrator and string quartet."

    Make repository public.

    Check "Initialze this repository with a README."

    Do not add .gitignore.

    Do not add license.

    Click "Create Repository."

19. Click "Clone or download."

    Copy repository URL with clipboard icon.

20. Return to terminal and clone repository.

    https://github.com/trevorbaca/stirrings.git

21. Start IDE and create score package.

    (new)

    TODO: teach IDE to prompt for newly created repository.

22. IDE includes composer, title and year metadata automatically.

    Add catalog number and forces tagline metadata by hand.
    
    (meta).

    metadata = abjad.TypedOrderedDict(
        [
            ('catalog_number', 'AWN-018'),
            ('composer', 'Bača'),
            ('forces_tagline', 'for narrator \& string quartet'),
            ('title', 'Stirrings Still'),
            ('year', 2017),
            ]
        )

23. Copy .gitignore from existing score.

    (ww)

    (get > .gitignore)

24. Quit IDE and list score packages.

    (ren) to rename score package if necessary.

25. Quit IDE again.

    Add aliases to ~/.profile.

    export STIRRINGS=$SCORES/stirrings
    alias stix="clear; cd $STIRRINGS/stirrings"
    alias sti="stix; start-abjad-ide sti"

    Quit terminal.

    Restart terminal.

26. Change to score package in three terminal windows.

    Window > Save Windows as Group ...

    Use window group when terminal starts.

    Quit and restart terminal.

    Restart IDE.

27. Make etc files.

    (ee > new > to-do.md)

    (ee > new > stages.md)

    (ci > "Added stages.")

28. Copy ScoreTemplate.py from existing score package.

    (oo > get > ScoreTemplate.py)

    Edit ScoreTemplate.py by hand.

    Define instruments in score order.

    Make only one (master) score template per score.

    (^^)

29. Copy instruments from existing score package.

    (mm > get > instruments)

    Edit instruments/definition.py by hand.

    Define instruments in score order.

    (dfk)

    Eventually run (pdfm).

30. Copy metronome marks package from existing score package.

    (mm > get > metronome_marks)

    Edit metronome_marks/definition.py by hand.

    Define metronome marks alphabetically by metronome mark name.

    (dfk)

    Eventually run (pdfm).

31. Copy time signatures package from existing score package, if requred.

    (mm > get > time_signatures) 

    Edit time_signatures/definition.py by hand.

    (dfk)

    Eventually run (pdfm).

32. Change to stylesheets directory.

    (yy)

    Leave IDE-generated nonfirst-segment.ily as is.

33. Copy contexts.ily from existing score package.

    (yy > get > contexts.ily)

    Edit contexts.ily by hand.

    Define global contexts first.
    
    Define score contexts in score order.

    Make sure stylesheet includes ...

        \override TextScript.font-name = #"Palatino"

    ... in the Score context to stop LaTeX's pdfpages fl ligature problems.

    (No method exists to check LilyPond stylesheet edits.)

    (Eventually create much of contexts.ily from ScoreTemplate.py.)

34. Replace IDE-generated stylesheet.ily with stylesheet.ily from existing
    score package.

    (yy > get > stylesheet.ily).

    Edit stylesheet.ily by hand.

35. Copy parts.ily from existing score packge if score requires parts.

    (yy > get > parts.ily)

    Edit parts.ily by hand.

    (Probably no editing will be required.)

    (No method exists to check LilyPond stylesheet edits.)

    (Eventually teach IDE more about part production.)

36. Test and commit.

    (^^)

    (++)

    (ci > "Defined score template, instruments and stylesheet.")

37. Edit stages.txt.

    Detail score stages verbally.

38. Create all segments with yet-to-be-implemented (gg > setup).

    To define 'name' by hand:

        metadata = collections.OrderedDict([
            ('name', 'K'),
            ])

    To create segments by hand:

        (gg > new > _ > meta > define 'name' by hand)
        (gg > new > A > meta > define 'name' by hand)
        ...
        (gg > new > Q > meta > define 'name' by hand)

39. Define stub version of first segment.

    (gg > new > _)

    (%_)

    (get > definition.py)

    Edit _/definition.py by hand.

    Define figure infrastructure if figure-oriented.

    Define segment-maker.

    Define no music if time-signature-oriented.

    Define one figure if figure-oriented.

    Render PDF.

    Check title typography.

    Check instrument names.
    
    Check short instrument names.

    (pdfm) to render PDF.

    (@sty) to edit stylesheet.ily.

    (@instr) to edit materials/instruments/definition.py.

    (lp) to make sure no errors or warnings appear in LilyPong log.
    
40. Define stub version of nonfirst segment.

    (gg > new > A)

    (%A)

    (get > definition.py)

    Edit A/definition.py by hand.

    Define segment-maker.

    Supply time signatures for two (or more) pages of music.

    This will allow stylesheet footer-checking when stub score is built.

    Render PDF.

    Footers will not appear in the output PDF.

    But footers will appear when stub score is built.

    Check short instrument names.

    (lp) to make sure no errors or warnings appear in LilyPong log.

41. Build stub version of score.

    (bb > new > ledger) 

    (%led)

    (!trash assets)

    (!trash segments)

    (!trash parts.ily)

    (!trash segments.ily)

    (lyc*)

    (fcg pg mg bcg sg)

    Edit music.ly by hand.
    
    Comment-out not-yet-created segments.

    (fci pi mi bci si)

    (mi)

    (si)

    Check footers on pages two and greater.
    
    (@sty) to edit stylesheet.ily.

    TODO: Teach IDE more about builds.

42. Test and commit.

    (ss)

    (^^)

    (++)

    (ci > "Built stub segments.")

43. Test and rebuild everything.

    (cdj ..)

    (!ajv api -M)

    (^^ ++ ci)

    (cdi)

    (!ajv api -I)

    (^^ ++ ci)

    (ll make_baca_api.py)

    (^^ ++ ci)
        
    (q)

    cd ~/Scores; make_scores_api.py; git st; git commit "Rebuilt API."

44. Rebuild scores.

    (mm > pdfm*)

    (gg > pdfm*)

    (^^)

    (++)

45. Rebuild docs make clean.

    cd ~/abjad/abjad/docs; make clean; ajv api -M 

    cd ~/abjad-ide/ide/docs; make clean; ajv api -I

    cd ~/baca/baca/_docs; make clean; make_baca_api.py

    cd ~/Scores/_docs; make clean; make_scores_api.py

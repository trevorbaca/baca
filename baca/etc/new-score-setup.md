NEW SCORE SETUP
===============

1.  Read and revise this document.

2.  Apply OS updates.

    Apple menu > App Store ... > Updates.

3.  Install TeXShop updates.

    TeXShop > Install updates.

    TeXShopw > Check for updates.

4.  Apply LilyPond updates.

    lilypond.org > Unstable release.

5.  Pull scores.

    pull_all

    (st*)

    (up*)

6.  (cdj ..)

    (!ajv api -M)

    (^^ ++ ci)

    (cdi)

    (!ajv api -I)

    (^^ ++ ci)

    (ll make_baca_api.py)

    (^^ ++ ci)
        
    (q)

    cd ~/Scores; make_scores_api.py; git st; git commit "Rebuilt API."

7.  Package unpshed trevor/dev commits and push into Abjad.

    cd ~/abjad/abjad

    git checkout trevor/dev
    
    ...

8.  Update Abjad.

    cd ~/abjad

    pip install -e .

    ajv api -M; ajv doctest; py.test -rf; git st

9.  Update the IDE.

    cd ~/abjad-ide

    pip install -e .

    ajv api -I; ajv doctest; py.test -rf; git st

10. Update Bača.

    cd ~/baca

    git pull

    make_baca_api.py; (^^); (++); git st

11. Rebuild scores.

    (mm > pdfm*)

    (gg > pdfm*)

    (^^)

    (++)

12. Select score title.

    Select score package name.

13. Go to www.github.com.

    Click "New Repository".

    Name the repository.

    Add description: "Stirrings Still (2017) for narrator and string quartet."

    Make repository public.

    Check "Initialze this repository with a README."

    Do not add .gitignore.

    Do not add license.

    Click "Create Repository."

14. Click "Clone or download."

    Copy repository URL with clipboard icon.

15. Return to terminal and clone repository.

    https://github.com/trevorbaca/stirrings.git

16. Start IDE and create score package.

    (new)

    TODO: teach IDE to prompt for newly created repository.

17. IDE includes composer, title and year metadata automatically.

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

18. Copy .gitignore from existing score.

    (ww)

    (get > .gitignore)

19. Quit IDE and list score packages.

    (ren) to rename score package if necessary.

20. Quit IDE again.

    Add aliases to ~/.profile.

    export STIRRINGS=$SCORES/stirrings
    alias stix="clear; cd $STIRRINGS/stirrings"
    alias sti="stix; start-abjad-ide sti"

    Quit terminal.

    Restart terminal.

21. Change to score package in three terminal windows.

    Window > Save Windows as Group ...

    Use window group when terminal starts.

    Quit and restart terminal.

    Restart IDE.

22. Make etc files.

    (ee > new > to-do.md)

    (ee > new > stages.md)

    (ci > "Added stages.")

23. Copy ScoreTemplate.py from existing score package.

    (oo > get > ScoreTemplate.py)

    Edit ScoreTemplate.py by hand.

    Define instruments in score order.

    Make only one (master) score template per score.

    (^^)

24. Copy instruments from existing score package.

    (mm > get > instruments)

    Edit instruments/definition.py by hand.

    Define instruments in score order.

    (dfk)

    Eventually run (pdfm).

25. Copy metronome marks package from existing score package.

    (mm > get > metronome_marks)

    Edit metronome_marks/definition.py by hand.

    Define metronome marks alphabetically by metronome mark name.

    (dfk)

    Eventually run (pdfm).

26. Copy time signatures package from existing score package, if requred.

    (mm > get > time_signatures) 

    Edit time_signatures/definition.py by hand.

    (dfk)

    Eventually run (pdfm).

27. Change to stylesheets directory.

    (yy)

    Leave IDE-generated nonfirst-segment.ily as is.

28. Copy contexts.ily from existing score package.

    (yy > get > contexts.ily)

    Edit contexts.ily by hand.

    Define global contexts first.
    
    Define score contexts in score order.

    Make sure stylesheet includes ...

        \override TextScript.font-name = #"Palatino"

    ... in the Score context to stop LaTeX's pdfpages fl ligature problems.

    (No method exists to check LilyPond stylesheet edits.)

    (Eventually create much of contexts.ily from ScoreTemplate.py.)

29. Replace IDE-generated stylesheet.ily with stylesheet.ily from existing
    score package.

    (yy > get > stylesheet.ily).

    Edit stylesheet.ily by hand.

30. Copy parts.ily from existing score packge if score requires parts.

    (yy > get > parts.ily)

    Edit parts.ily by hand.

    (Probably no editing will be required.)

    (No method exists to check LilyPond stylesheet edits.)

    (Eventually teach IDE more about part production.)

31. Test and commit.

    (^^)

    (++)

    (ci > "Defined score template, instruments and stylesheet.")

32. Edit stages.txt.

    Detail score stages verbally.

33. Create all segments with yet-to-be-implemented (gg > setup).

    To define 'name' by hand:

        metadata = collections.OrderedDict([
            ('name', 'K'),
            ])

    To create segments by hand:

        (gg > new > _ > meta > define 'name' by hand)
        (gg > new > A > meta > define 'name' by hand)
        ...
        (gg > new > Q > meta > define 'name' by hand)

34. Define stub version of first segment.

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
    
35. Define stub version of nonfirst segment.

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

36. Build stub version of score.

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

37. Test and commit.

    (ss)

    (^^)

    (++)

    (ci > "Built stub segments.")

38. Run tests.

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

39. Read and revise this document.

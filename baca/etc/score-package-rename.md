Score package rename
====================

OBJECTIVE: rename a (relatively recently created) score package:

    1. Rename GitHub repository.

    2. Rename Abjad score package.

STEPS:

    1.  Navigate to GitHub repository page:

        Example https://github.com/trevorbaca/stirrings;
        
        Click "Settings";

        Enter new name in the "Repository name" textbox;
        
        Click the "Rename" button.

    2.  Start IDE and use (ren) at main menu.

    3.  Navigate to renamed score package.

    4.  (ss > meta) to adjust title metadata (if necessary).

    5.  (ww > travis) to change PACKAGE environment variable.

        TODO: Teach IDE to handle this step during package rename.

    6.  (ww > read) to change build status Travis paths in README file.

        TODO: Teach IDE to handle this step during package rename.

    7.  (ci) to commit.

    8.  (als) to change score alias.

    9.  (vipf) to change score package environment variable.

    10. (vipf) to change PYTHONPATH environment variable.

    11. Quit and restart terminal.

    12. Reestablish window group in terminal (if necessary).

    13. (tests) to rerun tests.

    14. make_baca_api.py to rebuild API.

    15. Edit baca/scr/restart-all-travis-builds.

    16. Resync Travis: 
        
        Navigate to https://travis-ci.org/;

        Click on username link in upper right corner;

        Click "Accounts";

        Click "Sync account";

        Return to https://travis-ci.org/ and refresh page;

        Click tab for renamed package;

        Click "Restart build".

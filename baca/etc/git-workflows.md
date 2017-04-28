Abjad Git workflows
===================

This document describes the primary Git-based development workflow recommended
for Abjad core developers. The process was engineered primarily by Josiah and
transcribed here by Trevor. To use the procedures described here you will need
the Git client installed on your local machine and you will sometimes need to
visit the Abjad project pages hosted on GitHub. Run `git --version` to check
that the Git client is installed on your machine. The Abjad GitHub pages are
hosted at https://github.com/Abjad/abjad.

CONTENTS:

    * Command index
    * Rebasing on master
    * Single-commit workflow (changes already made)
    * Single-commit workflow (changes not yet made)
    * Setting up a development branch
    * Cherry-picking from development to feature branches

Command index
=============

Git commands used in these workflows:

    git branch
    git branch -d <branch-name>
    git checkout <branch-name>
    git checkout -b <branch-name>
    git cherry-pick
    git clone <URL>
    git lg
    git push
    git push --set-upstream origin <branch-name>
    git st

Add the following aliases to your `~/.gitconfig` file before you begin:

    lg = log --graph --abbrev-commit --pretty=oneline --decorate --color
    st = status

Rebasing on master
==================

Assume you have a persistent development branch (like trevor/dev) or a feature
branch (like trevor/implement-pitchtools-set-class) checked out on your local
machine. Also assume you've made some commits in your branch. Further assume
that master at origin (mainline hosted on GitHub's servers) has some relatively
new commits that your branch doesn't have. Finally assume that you want the
mainline commits in your branch. How best to add mainline commits to your
branch? One approach is to rebase your branch on master.

1. Check out master:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        08:43 $ git checkout master
        Switched to branch 'master'
        Your branch is behind 'origin/master' by 4 commits, and can be fast-forwarded.
        (use "git pull" to update your local branch)

2. Fetch from master:

        08:43 $ git fetch
        (abjad3) ✔ ~/abjad/abjad [master ↓·4|✔] 

    Nothing seems to happen. So perhaps this step is unncessary.

3. (Maybe) pull from master:

        (abjad3) ✔ ~/abjad/abjad [master ↓·4|✔] 
        08:49 $ git pull
        Updating 8336f29..16b7f68
        Fast-forward
        abjad/tools/lilypondparsertools/GuileProxy.py      |  2 +-
        .../LilyPondLexicalDefinition.py                   | 56 +++++++---------------
        abjad/tools/lilypondparsertools/LilyPondParser.py  | 12 +++--
        .../LilyPondSyntacticalDefinition.py               |  4 +-
        abjad/tools/systemtools/Configuration.py           |  3 +-
        5 files changed, 30 insertions(+), 47 deletions(-)

    Is this step necessary? Or is fetching sufficient?

4. Check out your development branch:

        (abjad3) ✔ ~/abjad/abjad [master|✔] 
        08:52 $ git checkout trevor/dev
        Switched to branch 'trevor/dev'
        Your branch is up-to-date with 'origin/trevor/dev'.

5. **Interactively** rebase your development branch on master:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        08:53 $ git rebase -i master

    Git will open a file in Vim:

        pick b14b9aa Added SetClass class to pitchtools.
        pick 6308a61 Pulled in vimrc updates..
        pick 2f62a57 Removed pitchtools.instantiate_pitch_and_interval_test_collection().
        < snip >
        pick 576a5ca Updated boilerplate score __metadata__.py file.
        pick 80c2842 Added empty __init__.py to example_score/test/ directory.
        pick 8ad1ebc Removed empty __init__ from example_score/test/ directory.
        pick 7462c5d Repeated NamedPitch, NumberedPitch __sub__() change.

        # Rebase 16b7f68..7462c5d onto 16b7f68 (48 command(s))
        #
        # Commands:
        # p, pick = use commit
        # r, reword = use commit, but edit the commit message
        # e, edit = use commit, but stop for amending
        # s, squash = use commit, but meld into previous commit
        # f, fixup = like "squash", but discard this commit's log message
        # x, exec = run command (the rest of the line) using shell
        # d, drop = remove commit
        #
        # These lines can be re-ordered; they are executed from top to bottom.
        #
        # If you remove a line here THAT COMMIT WILL BE LOST.
        #
        # However, if you remove everything, the rebase will be aborted.
        #
        # Note that empty commits are commented out

    Change pick commands to other commands, as needed.

    Step-by-step instructions are impossible here.

    Write and quit Vim.

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        08:53 $ git rebase -i master
        [detached HEAD 4b22a04] Pulled in vimrc updates.
        Date: Sat Oct 22 13:03:14 2016 -0500
        1 file changed, 1 insertion(+), 1 deletion(-)
        Successfully rebased and updated refs/heads/trevor/dev.

6. Force-push:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·48↑·52|✔] 
        08:55 $ git push -f
        Counting objects: 398, done.
        Delta compression using up to 4 threads.
        Compressing objects: 100% (397/397), done.
        Writing objects: 100% (398/398), 58.98 KiB | 0 bytes/s, done.
        Total 398 (delta 339), reused 0 (delta 0)
        remote: Resolving deltas: 100% (339/339), completed with 73 local objects.
        To https://github.com/Abjad/abjad.git
        + 7462c5d...c86ad9e trevor/dev -> trevor/dev (forced update)

7. Done:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        08:57 $ git st
        On branch trevor/dev
        Your branch is up-to-date with 'origin/trevor/dev'.
        nothing to commit, working tree clean


Single-commit workflow (changes not already made)
=================================================

Use this workflow for the thinnest of all possible interactions with the
codebase: a single commit. The understanding here will be that your single
commit will be equivalent to a (very small) feature.

1. Visit the Abjad GitHub pages at https://github.com/Abjad or the Abjad IDE
GitHub pages at https://github.com/Abjad/ide. Click on "issues". Open an issue.
For example "Rerender test artifacts for LilyPond 2.19.49". Make a note of the
issue number GitHub assigns. (Issue #146, for example).

2. Create an eponymous feature branch on your local machine:

        git checkout -b trevor/rerender-test-artifacts-for-lilypond-2-19-49

3. Make your changes, add, commit and push to origin. Include the string
"closes #146" (or equivalent) in your commit message to signal to GitHub that
the commit should close issue #146 automatically:

        git add .
        git commit "Rerendered for LilyPond 2.19.49. This closes #146."
        git push --set-upstream origin trevor/rerender-test-artifacts-for-lilypond-2-19-49

4. Return to https://github.com/Abjad or https://github.com/Abjad/ide. You will
likely be prompted to create a pull request with a green button labeled
"compare & pull request". Click this button. GitHub will take you to a PR
creation page titled "Open a pull request."

5. On the PR creation page you will find a green button labeled "Create pull
request." Click this button. GitHub will take you to a PR info page titled
something like "Rerendered test artifacts for LilyPond 2.19.49. #147." Notice
that the PR ID (#147) is incrementally greater than the corresponding issue ID
(#146).

6. On the PR info page you will see an array of information detailing the PR
you just created. Wait until all Travis tests have finished running. Go back
and fix any Travis tests that fail. After all Travis tests pass you will see a
green button labeled "Merge pull request." Click this button. You will see a
new green button labeled "Confirm merge." Click this button. If everything goes
right GitHub will present an in-page message that says "Pull request
successully merged and closed." You will see a gray button labeled "Delete
branch." Click this button.

7. Return to https://github.com/Abjad or https://github.com/Abjad/ide. Confirm
that GitHub's "branches" page no longer includes the feature branch you created
during this workflow.

8. Note that a copy of the feature branch persists on your local machine:

        (abjad3) ✔ ~/abjad-ide [trevor/rerender-test-artifacts-for-lilypond-2-19-49|✔] 
        12:10 $ git branch
        master
        * trevor/rerender-test-artifacts-for-lilypond-2-19-49

9. Check out master:

        12:23 $ git checkout master
        Switched to branch 'master'
        Your branch is behind 'origin/master' by 2 commits, and can be fast-forwarded.
        (use "git pull" to update your local branch)
        (abjad3) ✔ ~/abjad-ide [master ↓·2|✔] 

10. Pull from origin into your local copy of master:

        12:24 $ git pull
        Updating da848d5..67d238c
        Fast-forward
        .travis.yml                                         |   4 ++--
        .../build/letter-portrait/music.pdf                 | Bin 39687 -> 39687 bytes
        .../build/letter-portrait/score.pdf                 | Bin 78993 -> 78992 bytes
        .../materials/magic_numbers/illustration.pdf        | Bin 19337 -> 19336 bytes
        .../pitch_ranges/illustration.pdf          | Bin 10592 -> 10592 bytes
        .../materials/tempos/illustration.pdf      | Bin 24265 -> 24265 bytes
        .../segments/segment_01/illustration.pdf            | Bin 35806 -> 35806 bytes
        .../segments/segment_02/illustration.pdf            | Bin 34607 -> 34607 bytes
        .../segments/segment_03/illustration.pdf            | Bin 34658 -> 34658 bytes
        9 files changed, 2 insertions(+), 2 deletions(-)
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Note that the pink and green [master|✔] indicator shows that your copy of
    master is now up to date.

11. Prune unused branches:

        12:25 $ git remote prune origin
        Pruning origin
        URL: https://github.com/Abjad/ide.git
        * [pruned] origin/issue-122-skip-two-tests
        * [pruned] origin/spiel-der-dornen-cleanup
        * [pruned] origin/trevor/rerender-test-artifacts-for-lilypond-2-19-49
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Prune removes the local copy of your feature branch. Prune may also remove
    other unused branches on your local machine (as shown above).

12. Display local branches again:

        12:27 $ git branch
        * master
        trevor/rerender-test-artifacts-for-lilypond-2-19-49
        (abjad3) ✔ ~/abjad-ide [master|✔] 

13. Delete the local copy of your feature branch if the local copy of your
feature branch persists:

        12:28 $ git branch -d trevor/rerender-test-artifacts-for-lilypond-2-19-49
        Deleted branch trevor/rerender-test-artifacts-for-lilypond-2-19-49 (was cf2bb92).
        (abjad3) ✔ ~/abjad-ide [master|✔] 

14. Display local branches again:

        12:29 $ git branch
        * master
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Confirm that the local copy of your feature branch no longer appears.

15. Prune again:

        12:30 $ git remote prune origin
        * master
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Confirm that prune has no effect.


Single-commit workflow (changes already made)
=============================================

Use this workflow as an equivalent for the one above *if* you've already made
some local changes while (for example) debugging.

1. Make changes, test, realize you need to create a PR and commit.

2. Visit the Abjad GitHub pages at https://github.com/Abjad or the Abjad IDE
GitHub pages at https://github.com/Abjad/ide. Click on "issues". Open an issue.
For example "Port aliases to Python 3". Make a note of the ID that GitHub
creates. (GitHub ID #149, for example).

3. Create an eponymous feature branch on your local machine:

        git checkout -b trevor/port-aliases-to-python-3

    You can use `git st` immediately after branch creation to confirm that your
    local changes are still present. (And note that if you `checkout master; git
    st` you will find that your local changes are still present in master, too.)

4. Add, commit and push to origin. Include the string "closes #149" (or
equivalent) in your commit message to signal to GitHub that the commit should
close #149 automatically:

        git add .
        git commit "Ported alises to Python 3. This closes #149."
        git push --set-upstream origin trevor/port-aliases-to-python-3

    Git will respond with something telling you that your newly created feature
    branch now "tracks" a remote branch:

        15:32 $ git push --set-upstream origin trevor/port-aliases-to-python-3
        Counting objects: 6, done.
        Delta compression using up to 4 threads.
        Compressing objects: 100% (6/6), done.
        Writing objects: 100% (6/6), 595 bytes | 0 bytes/s, done.
        Total 6 (delta 4), reused 0 (delta 0)
        remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
        To https://github.com/Abjad/ide.git
        * [new branch]      trevor/port-aliases-to-python-3 -> trevor/port-aliases-to-python-3
        Branch trevor/port-aliases-to-python-3 set up to track remote branch trevor/port-aliases-to-python-3 from origin.

    And `git st` will tell you that your feature branch is up-to-date with the
    remote branch in question:

        15:34 $ git st
        On branch trevor/port-aliases-to-python-3
        Your branch is up-to-date with 'origin/trevor/port-aliases-to-python-3'.
        nothing to commit, working tree clean

5. Return to https://github.com/Abjad or https://github.com/Abjad/ide. You will
likely be prompted to create a pull request with a green button labeled
"compare & pull request". Click this button. GitHub will take you to a PR
creation page titled "Open a pull request."

6. On the PR creation page you will find a green button labeled "Create pull
request." Click this button. GitHub will take you to a PR info page titled
something like "Ported aliases to Python 3. #150." We can call this page a PR
info page. Notice that the PR ID (#150) is incrementally greater than the
corresponding issue ID (#149).

7. On the PR info page you will see several sections of information detailing
the PR you just created. Wait until all Travis tests have finished running.

    What happens if any Travis tests fail? Go to travis-ci.org and click on
    Abjad/abjad or Abjad/ide. Visually locate the job that failed. Click on the
    job that failed. Scroll down and read the logs of the job that failed. Then
    return to terminal and make local changes to fix the problem. Then add,
    commit, push. Then return to the PR info page. Notice that the PR info page
    will dynamically update to reflect the fact that Travis tests are
    rerunning. 

    After all Travis tests pass you will see a green button labeled "Merge pull
    request." Click this button. You will see a new green button labeled
    "Confirm merge." Click this button. If everything goes right GitHub will
    present an in-page message that says "Pull request successully merged and
    closed." You will see a gray button labeled "Delete branch." Click this
    button.

8. Return to https://github.com/Abjad or https://github.com/Abjad/ide. Confirm
that GitHub's "branches" page no longer includes the feature branch you created
during this workflow.

9. Note that a copy of the feature branch persists on your local machine:

        (abjad3) ✔ ~/abjad-ide [trevor/rerender-test-artifacts-for-lilypond-2-19-49|✔] 
        12:10 $ git branch
        master
        * trevor/rerender-test-artifacts-for-lilypond-2-19-49

10. Check out master:

        12:23 $ git checkout master
        Switched to branch 'master'
        Your branch is behind 'origin/master' by 2 commits, and can be fast-forwarded.
        (use "git pull" to update your local branch)
        (abjad3) ✔ ~/abjad-ide [master ↓·2|✔] 

11. Pull from origin into your local copy of master:

        12:24 $ git pull
        Updating da848d5..67d238c
        Fast-forward
        .travis.yml                                         |   4 ++--
        .../build/letter-portrait/music.pdf                 | Bin 39687 -> 39687 bytes
        .../build/letter-portrait/score.pdf                 | Bin 78993 -> 78992 bytes
        .../materials/magic_numbers/illustration.pdf        | Bin 19337 -> 19336 bytes
        .../pitch_ranges/illustration.pdf                   | Bin 10592 -> 10592 bytes
        .../materials/tempos/illustration.pdf               | Bin 24265 -> 24265 bytes
        .../segments/segment_01/illustration.pdf            | Bin 35806 -> 35806 bytes
        .../segments/segment_02/illustration.pdf            | Bin 34607 -> 34607 bytes
        .../segments/segment_03/illustration.pdf            | Bin 34658 -> 34658 bytes
        9 files changed, 2 insertions(+), 2 deletions(-)
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Note that the pink and green [master|✔] indicator shows that your copy of
    master is now up to date.

12. Prune unused branches:

        12:25 $ git remote prune origin
        Pruning origin
        URL: https://github.com/Abjad/ide.git
        * [pruned] origin/issue-122-skip-two-tests
        * [pruned] origin/spiel-der-dornen-cleanup
        * [pruned] origin/trevor/rerender-test-artifacts-for-lilypond-2-19-49
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Prune removes the local copy of your feature branch. Prune may also remove
    other unused branches on your local machine (as shown above).

13. Display local branches again:

        12:27 $ git branch
        * master
        trevor/rerender-test-artifacts-for-lilypond-2-19-49
        (abjad3) ✔ ~/abjad-ide [master|✔] 

14. Delete the local copy of your feature branch if the local copy of your
feature branch persists:

        12:28 $ git branch -d trevor/rerender-test-artifacts-for-lilypond-2-19-49
        Deleted branch trevor/rerender-test-artifacts-for-lilypond-2-19-49 (was cf2bb92).
        (abjad3) ✔ ~/abjad-ide [master|✔] 

15. Display local branches again:

        12:29 $ git branch
        * master
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Confirm that the local copy of your feature branch no longer appears.

16. Prune again:

        12:30 $ git remote prune origin
        * master
        (abjad3) ✔ ~/abjad-ide [master|✔] 

    Confirm that prune has no effect.


Setting up a development branch
===============================

Are you going to be contributing a lot of code to Abjad? Then consider setting
up a personal development branch as a customizable staging area for your work.

1. This workflow revolves around three branches on your local machine:

    1. master
    2. a development branch
    3. one (or more) feature branches

    The master and development branches will persist on your machine
    indefinitely. You will create and remove feature branches on an as-needed
    basis, as described below.

2. Clone a local copy of the Abjad repository to your local machine. (If you
have a local copy of the Abjad repository you can skip this step.)

        git clone https://github.com/Abjad/abjad.git

3. Visit the Abjad GitHub pages at https://github.com/Abjad. Information about
commit counts, branches, releases, contributors, issues, pull requests and the
structure of the Abjad repository itself are all available here. Note in
particular the "branches" link. Click this link. GitHub serves the 
https://github.com/Abjad/abjad/branches page. Take a look at the page. Nine or
ten branches are usually visible. The branches that you will make as part of
this workflow will appear here. We'll refer to this page as the "GitHub
branches page". It's worth bookmarking the page in your browser for easy
access.

4. Return to the terminal and change into your local copy of the Abjad
repository. Then run `git branch`:

        $ git branch
        * master

    Your local copy of the Abjad repository contains a branch called "master".

5. Create your PDB with `git checkout -b <branch-name>`:

        $ git checkout -b trevor/dev
        Switched to a new branch 'trevor/dev'

    You can name your PDB anything you like, with the example above being
    typical. Note that slashes are allowed in branch names (even though most
    other pieces of punctuation are not). You can use slahses (as shown above,
    for example) to provide a type of handmade namespacing; neither Git nor
    GitHub interpret slashes specially. Note, too, that you use `git checkout
    -b <branch-name>` to create a branch: you do not use `git branch` to create
    a branch.

6. Run `git branch` again:

        (abjad) ✔ ~/abjad/abjad [trevor/dev L|✔] 
        $ git branch
        master
        * trevor/dev

    Your PDB appears in the output of `git branch` preceded by an asterisk. The
    asterisk indicates the "present working branch" (that is, the branch you
    are currently "in" or working on). Note, too, that the "branch status
    indicator" [is this the best term?] displays the name of the present
    working branch together with an "L" and a check mark. We'll return to the
    meaning of the "L" and the check mark later.

7. You can use `git checkout` to move back and forth between branches:

        (abjad) ✔ ~/abjad/abjad [trevor/dev L|✔] 
        $ git checkout master
        Switched to branch 'master'
        Your branch is up-to-date with 'origin/master'.

        (abjad) ✔ ~/abjad/abjad [master|✔] 
        $ git checkout trevor/dev
        Switched to branch 'trevor/dev'

    Note that you use `git checkout <branch-name>` to move between branches.
    There is no `git switch <branch-name>` or the like.
    
8. What do you do if you want to rename the branch you just created? The
process involves three steps: switch to master, delete your PDB and then
recreate your PDB with a different name:

        (abjad) ✔ ~/abjad/abjad [trevor/dev L|✔] 
        $ git checkout master
        Switched to branch 'master'
        Your branch is up-to-date with 'origin/master'.

        (abjad) ✔ ~/abjad/abjad [master|✔] 
        $ git branch -d trevor/dev
        Deleted branch trevor/dev (was a94bf0d).

        (abjad) ✔ ~/abjad/abjad [master|✔] 
        $ git checkout -b trevor/dev
        Switched to a new branch 'trevor/dev'
    
    The important thing to note here is that you can not delete the present
    working branch. Switch to another branch (like master) first.

9. Pause to consider the asymmetry between the Git commands required to create
a branch, delete a branch, move between branches and list branches:

    * create a branch: `git checkout -b <branch-name>`
    * delete a branch: `git branch -d <branch-name>`
    * move between branches: `git checkout <branch-name>`
    * list branches: `git branch`

    Two of these commands are variants of `git branch` while the other two are
    versions of `git checkout`. Best to commit the asymmetry to memory.

10. Return to GitHub's Abjad branches page:

    https://github.com/Abjad/abjad/branches

    Notice that your PDB does not yet appear.

11. Switch back to your PDB. Make a trivial change to a file. Save the file.
Notice that the check mark previously included in the branch status indicator
has changed to "...1":

        (abjad) ✔ ~/abjad/abjad [trevor/dev L|…1] 
        $

    The `...1` shows that a file has changed in your local copy.

12. Add the file:

        $ git add .
        (abjad) ✔ ~/abjad/abjad [trevor/dev L|●1] 

    The branch status indicator (BSI) has changed to show a single file added
    but not yet committed.

13. Commit the file:

        (abjad) ✔ ~/abjad/abjad [trevor/dev L|●1] 
        $ git commit
        [trevor/dev dfa36c6] Added ForteNumber class to pitchtools.
        1 file changed, 76 insertions(+)
        create mode 100644 abjad/tools/pitchtools/ForteNumber.py

    Note that BSI has changed back to a check mark:

        (abjad) ✔ ~/abjad/abjad [trevor/dev L|✔] 
        $

14. Attempt to push your commit:

        (abjad) ✔ ~/abjad/abjad [trevor/dev L|✔] 
        $ git push
        fatal: The current branch trevor/dev has no upstream branch.

    Use the following to push the current branch and set the remote as
    upstream:

        git push --set-upstream origin trevor/dev
        (abjad) ✘-128 ~/abjad/abjad [trevor/dev L|✔] 

    Git complains that your PDB has no "upstream branch".

    Use `git push --set-upstream <remote> <branch-name>` the way Git suggests:

        (abjad) ✘-128 ~/abjad/abjad [trevor/dev L|✔] 
        $ git push --set-upstream origin trevor/dev
        Counting objects: 6, done.
        Delta compression using up to 4 threads.
        Compressing objects: 100% (6/6), done.
        Writing objects: 100% (6/6), 1.03 KiB | 0 bytes/s, done.
        Total 6 (delta 4), reused 0 (delta 0)
        remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
        To https://github.com/Abjad/abjad.git
        * [new branch]      trevor/dev -> trevor/dev
        Branch trevor/dev set up to track remote branch trevor/dev from origin.

    Consider the last line of Git's output: "Branch trevor/dev set up to track
    remote branch trevor/dev from origin." What does this mean? This means that
    the PDB you have created in your local copy of the Abjad repository is now
    set up to "track" a remote branch (also called trevor/dev) on origin. The
    statement introduces several new phenomena at one time. First, consider
    that your PDB is now to be thought of as "local" (ie, on your machine) and
    that this contrasts with a "remote" branch (ie, in the Abjad repository
    hosted by GitHub). The second thing is that calling "git push
    --set-upstream" (in the way shown above) functions to create the remote
    version of your PDB. The next steps confirms that this is the case.

15. Visit GitHub's Abjad branches page again:

    https://github.com/Abjad/abjad/branches

    Voila! Assuming the previous step worked correctly, you will now see a
    section of GitHub's Abjad branches page entitled "your branches". The
    remote version of your PDB will be listed there.

    Take a minute to study GitHub's web-based presentation of (the remote copy
    of) your PDB. An icon of a trash can (to delete the branch) and a "new pull
    request" button appear. You won't need the trash can icon because your PDB
    is designed to be persistent. (Though later in this workflow you'll delete
    other, transient branches.) And pull requests (PRs) can also be safely
    ignored at this point (though described later in this workflow). But take a
    moment and study the (unlabeled) two-part indicator that probably looks
    something like "0|1". Call this the "commit status indicator" (CSI). The
    left part of the CSI gives the number of commits sitting in "remote master"
    that do not yet exist in your remote PDB. What is "remote master"? The
    remote master branch is the version of the master branch (ie, mainline) of
    the Abjad repository hosted on GitHub's servers. So the 0 in this CSI's
    "0|1" means that there are zero commits sitting in remote master that do
    not yet exist in the remote copy of your PDB. The right part of the CSI
    gives the number of commits sitting in the remote version of your PDB that
    do not (yet) exist in remote master. Note the symmetry between the left and
    right parts of the CSI: the left part gives a count of commits in remote
    master not yet in remote PDB; the right part gives a count of commits in
    remote PDB not yet in remote master. The left and right parts of the CSI
    are something of a type of inverse of each other. As a whole, the CSI gives
    some sense of the degree of out-of-synch-ness of any branch in the
    repository in comparison to master.

    The way that commits migrate from your PDB into master is the subject of
    pull requests and merges. We will initiate PRs (and manage merges) later in
    this workflow. For now, both topics can be safely ignored.

16. Return to the terminal, do more work, make more commits. Your work here
should feel familiar. Use `git add .` and `git push` in the usual ways. You
won't have to use `git push --set-upstream` any more, for example. You'll
probably be on this step for a couple of days or weeks, commiting code bit by
bit, effectively moving code the local copy of your PDB up to the remote
version of your PDB hosted on GitHub's servers. When you've created enough
commits to constitute some sort of user-relevant feature, move on to the next
steps.


Cherry-picking (from development to feature branches)
=====================================================

What to do after you development branch starts to accumulate commits? Every so
often you'll want to collect commits in your development branch and make
them into a feature that can be added into the Abjad mainline. You do this by
cherry-picking commits from your development branch into a feature branch that
you'll create specifically for this purpose.

1. Check out master:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:11 $ git checkout master
        Switched to branch 'master'
        Your branch is up-to-date with 'origin/master'.

2. Pull master:

        (abjad3) ✔ ~/abjad/abjad [master|✔] 
        10:21 $ git pull
        Already up-to-date.

3. Check out your development branch:

        (abjad3) ✔ ~/abjad/abjad [master|✔] 
        12:11 $ git checkout trevor/dev
        Switched to branch 'trevor/dev'
        Your branch is up-to-date with 'origin/trevor/dev'.

4. Pull your development branch:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:12 $ git pull
        Already up-to-date.

5. Decide which DB commits you want to gather together into a feature.

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:14 $ git lg

    Note hash suffixes to use in the next step.

6. Switch back to master (IMPORTANT):

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:06 $ git checkout master
        Switched to branch 'master'
        Your branch is up-to-date with 'origin/master'.

    Why is it so important to switch back to master? Because the branch
    creation that happens in the following step will be based on the status of
    the current branch. And we will want to create a feature branch *based on
    master* (and not based on your development branch).

7. Create a feature branch using Git's checkout command:

        (abjad3) ✔ ~/abjad/abjad [master|✔] 
        12:18 $ git checkout -b trevor-pitchtools-cleanup
        Switched to a new branch 'trevor-pitchtools-cleanup'

    Optionally you can run tests on your feature branch now just to make sure
    everything is ok before populating your feature branch:

        (abjad3) ✔ ~/abjad/abjad [trevor/update-score-metadata-file L|✔] 
        14:47 $ ajv doctest tools/pitchtools
        ...
    
8. Populate your feature branch with cherry-picked commits:

        (abjad3) ✔ ~/abjad/abjad [trevor/update-score-metadata-file L|✔] 
        10:24 $ git cherry-pick c96a20c
        [trevor/update-score-metadata-file b4240a0] CONFIG: Updated vimrc and boilerplate score __metadata__.py file.
        Date: Sat Oct 22 13:03:14 2016 -0500
        2 files changed, 3 insertions(+), 3 deletions(-)

    Call `cherry-pick` as many times as necessary.

    You can run tests between cherry-picks to convince yourself that things are
    ok after each cherry-pick. Calling `git st` between cherry-picks shows
    nothing.

9. Push:

        (abjad3) ✔ ~/abjad/abjad [trevor/update-score-metadata-file L|✔] 
        10:25 $ git push
        fatal: The current branch trevor/update-score-metadata-file has no upstream branch.
        To push the current branch and set the remote as upstream, use

            git push --set-upstream origin trevor/update-score-metadata-file

        (abjad3) ✘-128 ~/abjad/abjad [trevor/update-score-metadata-file L|✔] 
        10:25 $ git push --set-upstream origin trevor/update-score-metadata-file
        Counting objects: 10, done.
        Delta compression using up to 4 threads.
        Compressing objects: 100% (9/9), done.
        Writing objects: 100% (10/10), 1.07 KiB | 0 bytes/s, done.
        Total 10 (delta 7), reused 0 (delta 0)
        remote: Resolving deltas: 100% (7/7), completed with 7 local objects.
        To https://github.com/Abjad/abjad.git
        * [new branch]      trevor/update-score-metadata-file -> trevor/update-score-metadata-file
        Branch trevor/update-score-metadata-file set up to track remote branch trevor/update-score-metadata-file from origin.

10. Visit GitHub at http://github.com/Abjad/abjad:

    - You'll be notified that you can make a PR from the newly pushed branch.
    - Make the PR ("Compare & pull request" > "Create pull request").
    - Wait for tests to pass.
    - Make corrections in your feature branch and push again, if necessary.
    - Merge the branch via the PR page.
    - Delete the branch.

11. Return to the terminal and check out master:

        (abjad3) ✘-128 ~/abjad/abjad [trevor/update-score-metadata-file L|✔] 
        14:21 $ git checkout master
        Switched to branch 'master'
        Your branch is behind 'origin/master' by 2 commits, and can be fast-forwarded.
        (use "git pull" to update your local branch)

12. Pull master:

        (abjad3) ✔ ~/abjad/abjad [master ↓·2|✔] 
        14:23 $ git pull
        Updating 16b7f68..b6253f4
        Fast-forward
        abjad/boilerplate/example_score/example_score/__metadata__.py | 4 ++--
        abjad/etc/editors/vimrc                                       | 2 +-
        2 files changed, 3 insertions(+), 3 deletions(-)

13. Delete the feature branch:

        (abjad3) ✔ ~/abjad/abjad [master|✔] 
        14:21 $ git branch -d trevor/update-score-metadata-file
        Deleted branch trevor/update-score-metadata-file (was b4240a0).

I think that's it. That is, I don't think it's necessary to check out your
development branch and interactively rebase on master.

Abjad Git workflows
===================

This document describes the primary Git-based development workflow recommended
for Abjad core developers. The process was engineered primarily by Josiah and
transcribed here by Trevor. To use the procedures described here you will need
the Git client installed on your local machine and you will sometimes need to
visit the Abjad project pages hosted on GitHub. Run `git --version` to check
that the Git client is installed on your machine. The Abjad GitHub pages are
hosted at https://github.com/Abjad/abjad. Git commands used in this workflow:

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

1. Fetch origin:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        13:01 $ git fetch origin

    Nothing seems to happen. So perhaps this step is unncessary.

2. Rebase on master:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        13:01 $ git rebase origin/master
        First, rewinding head to replay your work on top of it...
        Applying: Added ForteNumber class to pitchtools.
        Applying: Improved ForteNumber initialization.
        Applying: Changed pitchtools.ForteNumber to pitchtools.SetClass.

    Git "rewinds" the head of your branch to the current state of
    origin/master.
    
    Then Git reapplies your commits.

    The local copy of your branch now differs from the remote copy of your
    branch.

    If everything goes well then asking for status will show something like
    this:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·3↑·18|✔] 
        13:02 $ git st
        On branch trevor/dev
        Your branch and 'origin/trevor/dev' have diverged,
        and have 18 and 3 different commits each, respectively.
        (use "git pull" to merge the remote branch into yours)
        nothing to commit, working directory clean

    What if things go differently? It's possible Git might tell you things like
    this:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        11:00 $ git rebase origin/master
        First, rewinding head to replay your work on top of it...
        Applying: Added ForteNumber class to pitchtools.
        Applying: Improved ForteNumber initialization.
        Applying: Changed pitchtools.ForteNumber to pitchtools.SetClass.
        Applying: Added ForteNumber class to pitchtools.
        Applying: Improved ForteNumber initialization.
        Applying: Changed pitchtools.ForteNumber to pitchtools.SetClass.
        Using index info to reconstruct a base tree...
        Falling back to patching base and 3-way merge...
        Applying: Pulled in vimrc updates..
        Applying: Removed pitchtools.instantiate_pitch_and_interval_test_collection().
        Applying: Removed pitchtools.inventory_named_inversion_equivalent_interval_classes().
        Applying: Added IterationAgent.by_pitch_pair().
        Applying: Removed pitchtools.iterate_named_pitch_pairs_in_expr().
        Applying: Renamed pitchtools.list_ordered_pitch_pairs().
        Applying: Removed pitchtools.list_ordered_pitch_pairs().
        Applying: Removed pitchtools.list_unordered_named_pitch_pairs_in_expr().
        Applying: Reoved pitchtools.list_pitch_numbers_in_expr().
        Applying: Deprecated pitchtools.list_numbered_interval_numbers_pairwise().
        Applying: Removed pitchtools.list_numbered_intervals_pairwise().
        Applying: Removed pitchtools.list_numbered_inversion_equivalent_interval_classes_in_expr.
        Applying: Cleaned up pitchtools.list_named_pitches_in_expr().
        Applying: Renamed pitchtools.list_named_pitches_in_expr().
        Applying: Changed pitchtools.list_pitches() return type.
        Applying: Renamed pitchtools.list_pitches().
        Applying: Deprecated pitchtools.iterate_pitches().
        Applying: Removed pitchtools.iterate_pitches(). CHANGE.
        Applying: Removed pitchtools.set_written_pitch_of_pitched_components_in_expr().
        Applying: Removed pitchtools.sort_named_pitch_carriers_in_expr().
        Applying: Replaced pitchtools.yield_all_pitch_class_sets().
        Applying: Replaced pitchtools.transpose_named_pitch_by_numbered_interval_and_respell().
        Applying: Deprecated pitchtools.transpose_pitch_number_by_octave_transposition_mapping().
        Applying: Removed pitchtools.transpose_pitch_number_by_octave_transposition_mapping().
        Applying: Removed pitchtools.transpose_pitch_expr_into_pitch_range().
        Applying: Removed pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor().
        Applying: Added NamedInterval.transpose() and NumberedInterval.transpose().
        Applying: Replaced pitchtools.transpose_pitch_carrier_by_interval(). MILESTONE.
        Using index info to reconstruct a base tree...
        M	abjad/tools/pitchtools/NamedPitch.py
        Falling back to patching base and 3-way merge...
        error: Your local changes to the following files would be overwritten by merge:
            abjad/tools/pitchtools/SetClass.py
        Please commit your changes or stash them before you merge.
        Aborting
        error: Failed to merge in the changes.
        Patch failed at 0034 Replaced pitchtools.transpose_pitch_carrier_by_interval(). MILESTONE.
        The copy of the patch that failed is found in: .git/rebase-apply/patch

        When you have resolved this problem, run "git rebase --continue".
        If you prefer to skip this patch, run "git rebase --skip" instead.
        To check out the original branch and stop rebasing, run "git rebase --abort".

    Asking for status when this happens gives something like this:

        (abjad3) ✔ ~/abjad/abjad [:46943d7|✔] 
        11:13 $ git st
        rebase in progress; onto 8336f29
        You are currently rebasing branch 'trevor/dev' on '8336f29'.
        (all conflicts fixed: run "git rebase --continue")

        nothing to commit, working tree clean

    Aborting the rebase will look like this:

        (abjad3) ✔ ~/abjad/abjad [:46943d7|✔] 
        11:16 $ git rebase --abort

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        11:16 $ git st
        On branch trevor/dev
        Your branch is up-to-date with 'origin/trevor/dev'.
        nothing to commit, working tree clean

    But fixing the rebase is tricky. There were no local changes in the branch
    prior to rebasing. So why does Git complain about local changes during
    rebasing?

    In this case I copy `pitchtools/SetClass.py` to the desktop and try again.
    This time I tell Git to continue rebasing:

        (abjad3) ✘-128 ~/abjad/abjad [:38dac4f|✔] 
        11:18 $ git rebase --continue
        Applying: Replaced pitchtools.transpose_pitch_carrier_by_interval(). MILESTONE.
        No changes - did you forget to use 'git add'?
        If there is nothing left to stage, chances are that something else
        already introduced the same changes; you might want to skip this patch.

        When you have resolved this problem, run "git rebase --continue".
        If you prefer to skip this patch, run "git rebase --skip" instead.
        To check out the original branch and stop rebasing, run "git rebase --abort".

    There is nothing to add:

        (abjad3) ✔ ~/abjad/abjad [:38dac4f|✔] 
        11:20 $ git st
        rebase in progress; onto 8336f29
        You are currently rebasing branch 'trevor/dev' on '8336f29'.
        (all conflicts fixed: run "git rebase --continue")

        nothing to commit, working tree clean

    So I tell Git to skip the next patch to be rebased:

        (abjad3) ✔ ~/abjad/abjad [:38dac4f|✔] 
        11:22 $ git rebase --skip
        Applying: Added 'cardinality' property to PitchSet, PitchClassSet, IntervalSet.
        Applying: Implementing PitchClassSet.normal_order.
        Applying: Implementing PitchClassSet.normal_order.
        Applying: Fixed PitchClassSet string representation.
        Applying: Implemented PitchClassSet.normal_order. NEW.
        Applying: Refactored PitchClassSet.normal_order as PitchClassSet.get_normal_order().
        Applying: Implemented PitchClassSet.get_prime_form(). NEW.
        Applying: Defined normal order and prime form for empty pitch-class sets.
        Applying: Implemented SetClass ranking and unranking algorithms.
        Using index info to reconstruct a base tree...
        M	abjad/tools/pitchtools/SetClass.py
        .git/rebase-apply/patch:546: trailing whitespace.
            
        .git/rebase-apply/patch:561: trailing whitespace.
            
        warning: 2 lines add whitespace errors.
        Falling back to patching base and 3-way merge...
        Auto-merging abjad/tools/pitchtools/SetClass.py
        Applying: Implemented SetClass.from_pitch_class_set().
        Using index info to reconstruct a base tree...
        M	abjad/tools/pitchtools/SetClass.py
        Falling back to patching base and 3-way merge...
        Auto-merging abjad/tools/pitchtools/SetClass.py
        CONFLICT (content): Merge conflict in abjad/tools/pitchtools/SetClass.py
        error: Failed to merge in the changes.
        Patch failed at 0044 Implemented SetClass.from_pitch_class_set().
        The copy of the patch that failed is found in: .git/rebase-apply/patch

        When you have resolved this problem, run "git rebase --continue".
        If you prefer to skip this patch, run "git rebase --skip" instead.
        To check out the original branch and stop rebasing, run "git rebase --abort".

    I ask for status to understand what this means:

        (abjad3) ✔ ~/abjad/abjad [:b78ad99|✖ 1✔] 
        11:23 $ git st
        rebase in progress; onto 8336f29
        You are currently rebasing branch 'trevor/dev' on '8336f29'.
        (fix conflicts and then run "git rebase --continue")
        (use "git rebase --skip" to skip this patch)
        (use "git rebase --abort" to check out the original branch)

        Unmerged paths:
        (use "git reset HEAD <file>..." to unstage)
        (use "git add <file>..." to mark resolution)

            both modified:   tools/pitchtools/SetClass.py

        no changes added to commit (use "git add" and/or "git commit -a")

    Notice that the patch hex key has changed from `:38dac4f` to `:b78ad99`.
    Presumably this indicates that Git has made it further in the rebase by
    applying more commits.

    Git seems to think that only `pitchtools/SetClass.py` has changed. Using
    Vim to inspect the file shows a 728-line file. This is much shorter than
    the 1677-line file I saved to the desktop before rebasing. Reading through
    the file also shows a single merge conflict.

    So what are my options? I could fix the merge conflict by hand. But this
    seems like a bad idea. Because fixing the version of
    `pitchtools/SetClass.py` now present in my branch will still only get me a
    very old version of the file. So because I have a copy of the most recent
    version of the file, I'll try adding that to my branch and continuing the
    rebase.

    It appears to have eventually worked. Required many cycles of:

        (abjad3) ✔ ~/abjad/abjad [:b78ad99|✖ 1✔] 
        11:23 $ cp ~/Desktop/SetClass tools/pitchtools
        11:23 $ git add tools/pitchtools/SetClass.py
        11:23 $ git rebase --continue

    And sometimes:

        (abjad3) ✔ ~/abjad/abjad [:b78ad99|✖ 1✔] 
        11:23 $ cp ~/Desktop/SetClass tools/pitchtools
        11:23 $ git add tools/pitchtools/SetClass.py
        11:23 $ git rebase --skip

    The `pitchtools/SetClass.py` file now, correctly, has 1677 lines.

    Asking for status now gives this:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|✔] 
        11:34 $ git st
        On branch trevor/dev
        Your branch and 'origin/trevor/dev' have diverged,
        and have 59 and 58 different commits each, respectively.
        (use "git pull" to merge the remote branch into yours)
        nothing to commit, working tree clean

    Note the `[trevor/dev ↓·58↑·59|✔]` branch status indicator.

3. Pull. If there are no merge conflicts then things will look like this:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·3↑·18|✔] 
        13:02 $ git pull
        Merge made by the 'recursive' strategy.

    I can't explain why Git notifies about a "recursive" merge.

    If there are merge conflicts then things will look like this:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|✔] 
        11:37 $ git pull
        CONFLICT (modify/delete): abjad/tools/pitchtools/transpose_pitch_carrier_by_interval.py deleted in 186ca9ec1a593f039134bd6e57170c1d50292c11 and modified in HEAD. Version HEAD of abjad/tools/pitchtools/transpose_pitch_carrier_by_interval.py left in tree.
        Removing abjad/tools/pitchtools/test/test_pitchtools_transpose_pitch_carrier_by_interval.py
        Auto-merging abjad/tools/pitchtools/NumberedPitch.py
        CONFLICT (content): Merge conflict in abjad/tools/pitchtools/NumberedPitch.py
        Auto-merging abjad/tools/pitchtools/NamedPitch.py
        CONFLICT (content): Merge conflict in abjad/tools/pitchtools/NamedPitch.py
        Automatic merge failed; fix conflicts and then commit the result.

    Asking for status will show something like this:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●2✖ 3] 
        11:38 $ git st
        On branch trevor/dev
        Your branch and 'origin/trevor/dev' have diverged,
        and have 59 and 58 different commits each, respectively.
        (use "git pull" to merge the remote branch into yours)
        You have unmerged paths.
        (fix conflicts and run "git commit")
        (use "git merge --abort" to abort the merge)

        Changes to be committed:

            modified:   tools/pitchtools/__init__.py
            deleted:    tools/pitchtools/test/test_pitchtools_transpose_pitch_carrier_by_interval.py

        Unmerged paths:
        (use "git add/rm <file>..." as appropriate to mark resolution)

            both modified:   tools/pitchtools/NamedPitch.py
            both modified:   tools/pitchtools/NumberedPitch.py
            deleted by them: tools/pitchtools/transpose_pitch_carrier_by_interval.py

    What does this mean? The branch status indicator `[trevor/dev ↓·58↑·59|●2✖
    3]` shows that there are two files with merge conflicts and three unmerged
    paths. Reading through the files that Git lists as "unmerged paths" shows
    that `pitchtools/NamedPitch.py` and `pitchtools.NumberedPitch` have merge
    conflicts.

    I fixed the small merge conflicts in `pitchtools/NamedPitch.py` and
    `pitchtools.NumberedPitch` by hand.

    The file `pitchtools/transpose_pitch_carrier_by_interval.py` should be
    deleted. But rebasing has somehow added the file back to my branch. How to
    proceed? Maybe no action is required because `git st` shows the file
    scheduled for deletion anyway.

    So I add my changes to the two files whose merge conflicts I fixed by hand:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●2✖ 3] 
        11:46 $ git add tools/pitchtools/NamedPitch.py 
        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●3✖ 2] 
        11:47 $ git add tools/pitchtools/NumberedPitch.py 

    And then I ask for status:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●4✖ 1] 
        11:47 $ git st
        On branch trevor/dev
        Your branch and 'origin/trevor/dev' have diverged,
        and have 59 and 58 different commits each, respectively.
        (use "git pull" to merge the remote branch into yours)
        You have unmerged paths.
        (fix conflicts and run "git commit")
        (use "git merge --abort" to abort the merge)

        Changes to be committed:

            modified:   tools/pitchtools/NamedPitch.py
            modified:   tools/pitchtools/NumberedPitch.py
            modified:   tools/pitchtools/__init__.py
            deleted:    tools/pitchtools/test/test_pitchtools_transpose_pitch_carrier_by_interval.py

        Unmerged paths:
        (use "git add/rm <file>..." as appropriate to mark resolution)

            deleted by them: tools/pitchtools/transpose_pitch_carrier_by_interval.py

    Commit does not work because of one remaining unmerged path:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●4✖ 1] 
        11:48 $ git commit
        U	abjad/tools/pitchtools/transpose_pitch_carrier_by_interval.py
        error: commit is not possible because you have unmerged files.
        hint: Fix them up in the work tree, and then use 'git add/rm <file>'
        hint: as appropriate to mark resolution and make a commit.
        fatal: Exiting because of an unresolved conflict.

    So I remove:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●4✖ 1] 
        11:49 $ git rm tools/pitchtools/transpose_pitch_carrier_by_interval.py 
        abjad/tools/pitchtools/transpose_pitch_carrier_by_interval.py: needs merge
        rm 'abjad/tools/pitchtools/transpose_pitch_carrier_by_interval.py'

    And then ask for status:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●5] 
        11:49 $ git st
        On branch trevor/dev
        Your branch and 'origin/trevor/dev' have diverged,
        and have 59 and 58 different commits each, respectively.
        (use "git pull" to merge the remote branch into yours)
        All conflicts fixed but you are still merging.
        (use "git commit" to conclude merge)

        Changes to be committed:

            modified:   tools/pitchtools/NamedPitch.py
            modified:   tools/pitchtools/NumberedPitch.py
            modified:   tools/pitchtools/__init__.py
            deleted:    tools/pitchtools/test/test_pitchtools_transpose_pitch_carrier_by_interval.py
            deleted:    tools/pitchtools/transpose_pitch_carrier_by_interval.py

    And then commit:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↓·58↑·59|●5] 
        11:49 $ git commit
        [trevor/dev 0592e15] Merged branch 'trevor/dev' of https://github.com/Abjad/abjad into trevor/dev

    And then ask for status:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↑·60|✔] 
        11:50 $ git st
        On branch trevor/dev
        Your branch is ahead of 'origin/trevor/dev' by 60 commits.
        (use "git push" to publish your local commits)
        nothing to commit, working tree clean

    After pulling, the local copy of your will be ahead of the remote copy of
    your branch:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↑·19|✔] 
        13:02 $ git st
        On branch trevor/dev
        Your branch is ahead of 'origin/trevor/dev' by 19 commits.
        (use "git push" to publish your local commits)
        nothing to commit, working directory clean

    The `[trevor/dev ↑·19|✔]` BSI is a good thing. This means that the local
    copy of the branch has 19 commits that the remote copy doesn't yet have.

4. Add, commit, push:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↑·19|✔] 
        13:03 $ git add .

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↑·19|●1] 
        13:03 $ git commit
        [trevor/dev 4ecff29] Pulled in vimrc updates..
        1 file changed, 1 insertion(+), 1 deletion(-)

        (abjad3) ✔ ~/abjad/abjad [trevor/dev ↑·20|✔] 
        13:03 $ git push
        Counting objects: 24, done.
        Delta compression using up to 4 threads.
        Compressing objects: 100% (23/23), done.
        Writing objects: 100% (24/24), 2.75 KiB | 0 bytes/s, done.
        Total 24 (delta 17), reused 0 (delta 0)
        remote: Resolving deltas: 100% (17/17), completed with 6 local objects.
        To https://github.com/Abjad/abjad.git
        0fcc3a7..4ecff29  trevor/dev -> trevor/dev

    And now the local and remote copies of your branch match:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        13:03 $ git st
        On branch trevor/dev
        Your branch is up-to-date with 'origin/trevor/dev'.
        nothing to commit, working directory clean

    Note, however, that repeating the steps of the rebase (as shown above) will
    cause you to have to go back through all the merge conflict resolution once
    again.


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
        .../pitch_range_inventory/illustration.pdf          | Bin 10592 -> 10592 bytes
        .../materials/tempo_inventory/illustration.pdf      | Bin 24265 -> 24265 bytes
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
        .../pitch_range_inventory/illustration.pdf          | Bin 10592 -> 10592 bytes
        .../materials/tempo_inventory/illustration.pdf      | Bin 24265 -> 24265 bytes
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


Core contributor workflow: setting up a personal development branch (PDB)
=========================================================================

Are you going to be contributing a lot of code to Abjad? Then consider setting
up a personal development branch (PDB) as a customizable staging area for your
work.

1. This workflow revolves around three branches on your local machine:

    1. master
    2. a personal development branch (PDB)
    3. one (or more) feature branches (FB)

    The master and PDB branches will persist on your machine indefinitely. You
    will create and remove FBs on an as-needed basis, as described below.

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


Cherry-picking (from your development branch to a feature branch)
=================================================================

You'll accumulate commits in your DB after working in it for a while. Every so
often you'll want to collect some commits in your DB and make them into a
feature that can be added into the Abjad mainline. You do this by
cherry-picking commits from your DB into a feature branch (FB) that you'll
create specifically for this purpose.

1. Check out master. Pull:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:11 $ git checkout master
        Switched to branch 'master'
        Your branch is behind 'origin/master' by 7 commits, and can be fast-forwarded.
        (use "git pull" to update your local branch)

        (abjad3) ✔ ~/abjad/abjad [master ↓·7|✔] 
        12:11 $ git pull
        Updating 5a15d9f..8336f29
        Fast-forward
        README.rst                                         |  15 +-
        abjad/_version.py                                  |   2 +-
        abjad/docs/source/conf.py                          |   6 +-
        abjad/docs/source/installation.rst                 |   8 +-
        abjad/etc/packaging/packaging_checklist.txt        |  69 +++----
        abjad/etc/packaging/packaging_transcript.txt       |  40 +++++
        abjad/scr/devel/make-packaging-transcript.py       |  31 ++--
        abjad/tools/expressiontools/Callback.py            |   9 +-
        abjad/tools/pitchtools/Accidental.py               | 200 ++++++++++++++-------
        abjad/tools/pitchtools/NamedPitch.py               |  17 +-
        abjad/tools/pitchtools/NamedPitchClass.py          |  16 +-
        abjad/tools/pitchtools/Pitch.py                    |  14 +-
        abjad/tools/pitchtools/PitchRange.py               |  34 ++--
        .../test/test_pitchtools_Accidental___cmp__.py     |  30 +---
        .../test/test_pitchtools_Accidental___eq__.py      |   7 -
        .../test/test_pitchtools_Accidental___init__.py    |   3 +-
        .../test_pitchtools_Accidental_abbreviation.py     |   6 -
        .../test_pitchtools_Accidental_is_abbreviation.py  |  13 --
        .../test/test_pitchtools_Accidental_is_adjusted.py |   1 -
        ...htools_Accidental_symbolic_accidental_string.py |   1 -
        abjad/tools/systemtools/AbjadConfiguration.py      |   4 +-
        abjad/tools/systemtools/IOManager.py               |  41 +++--
        .../test/test_systemtools_IOManager_open_file.py   |   3 +-
        tox.ini                                            |  15 ++
        24 files changed, 351 insertions(+), 234 deletions(-)
        create mode 100644 tox.ini

2. Check out your development branch. Pull:

        (abjad3) ✔ ~/abjad/abjad [master|✔] 
        12:11 $ git checkout trevor/dev
        Switched to branch 'trevor/dev'
        Your branch is up-to-date with 'origin/trevor/dev'.

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:12 $ git pull
        Already up-to-date.

3. Decide which DB commits you want to gather together into a feature.

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:14 $ git lga


    Note hash suffixes to use in the next step.

4. Switch back to master (IMPORTANT):

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        12:06 $ git checkout master
        Switched to branch 'master'
        Your branch is up-to-date with 'origin/master'.

    Why is it so important to switch back to master? Because the branch
    creation that happens in the following step will be based on the status of
    the current branch. And we will want to create a feature branch *based on
    master* (and not based on your development branch).

5. Create a feature branch using Git's checkout command:

        (abjad3) ✔ ~/abjad/abjad [master|✔] 
        12:18 $ git checkout -b trevor-pitchtools-cleanup
        Switched to a new branch 'trevor-pitchtools-cleanup'

    Optionally you can run tests on your FB now just to make sure everything is
    ok before populating your FB:

        (abjad3) ✔ ~/abjad/abjad [trevor/pitchtools-cleanup L|✔] 
        14:47 $ ajv doctest tools/pitchtools
        ...
    
6. Populate your feature branch with hash suffixes from step 4, above:

        (abjad3) ✔ ~/abjad/abjad [trevor/pitchtools-cleanup L|✔] 
        15:08 $ git cherry-pick d11109d
        [trevor/pitchtools-cleanup 8ff6d84] Added ForteNumber class to pitchtools.
        Date: Wed Oct 5 11:21:47 2016 -0500
        1 file changed, 76 insertions(+)
        create mode 100644 abjad/tools/pitchtools/ForteNumber.py

        (abjad3) ✔ ~/abjad/abjad [trevor/pitchtools-cleanup L|✔] 
        15:08 $ git cherry-pick e06302e
        [trevor/pitchtools-cleanup 0806cc6] Improved ForteNumber initialization.
        Date: Thu Oct 6 09:45:06 2016 -0500
        1 file changed, 1 insertion(+), 1 deletion(-)

        (abjad3) ✔ ~/abjad/abjad [trevor/pitchtools-cleanup L|✔] 
        15:11 $ git cherry-pick 2bf112d
        [trevor/pitchtools-cleanup c78bcf8] Changed pitchtools.ForteNumber to pitchtools.SetClass.
        Date: Sat Oct 22 12:38:28 2016 -0500
        1 file changed, 8 insertions(+), 8 deletions(-)
        rename abjad/tools/pitchtools/{ForteNumber.py => SetClass.py} (74%)

        ...

    Call `cherry-pick` as many times as necessary.

    You can run tests between cherry picks to convince yourself that things are
    ok after each cherry pick, or after every couple of cherry picks.

    Note that calling `git st` during (and between) cherry picks apparently
    shows nothing.

7. Push:

        (abjad3) ✔ ~/abjad/abjad [trevor-pitchtools-cleanup L|✔] 
        12:25 $ git push
        fatal: The current branch trevor-pitchtools-cleanup has no upstream branch.
        To push the current branch and set the remote as upstream, use

            git push --set-upstream origin trevor-pitchtools-cleanup

        (abjad3) ✘-128 ~/abjad/abjad [trevor-pitchtools-cleanup L|✔] 
        12:25 $ git push --set-upstream origin trevor-pitchtools-cleanup
        Counting objects: 234, done.
        Delta compression using up to 4 threads.
        Compressing objects: 100% (234/234), done.
        Writing objects: 100% (234/234), 28.45 KiB | 0 bytes/s, done.
        Total 234 (delta 204), reused 0 (delta 0)
        remote: Resolving deltas: 100% (204/204), completed with 39 local objects.
        To https://github.com/Abjad/abjad.git
        * [new branch]      trevor-pitchtools-cleanup -> trevor-pitchtools-cleanup
        Branch trevor-pitchtools-cleanup set up to track remote branch trevor-pitchtools-cleanup from origin.

5. Visit GitHub at http://github.com/Abjad/abjad:

    - You'll be notified that you can make a PR from the newly pushed branch.
    - Make the PR ("Compare & pull request" > "Create pull request").
    - Wait for tests to pass.
    - Make corrections in your feature branch and push again, if necessary.
    - Merge the branch via the PR page.

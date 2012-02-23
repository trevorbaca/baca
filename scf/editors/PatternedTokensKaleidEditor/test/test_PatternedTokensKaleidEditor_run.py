import kaleids
import scf


def test_PatternedTokensKaleidEditor_run_01():

    editor = scf.editors.PatternedTokensKaleidEditor()
    editor.run(user_input='2 16 [2, 3] [6] [-1, 2, -3, 4] q', is_autoadvancing=True)

    kaleid = kaleids.PatternedTokens([-1, 2, -3, 4], 16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    assert editor.target == kaleid

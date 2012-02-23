import kaleids
import scf


def test_PartForcedChunkWithPatternedTokensKaleidEditor_run_01():

    editor = scf.editors.PartForcedChunkWithPatternedTokensKaleidEditor()
    editor.run(user_input='1 [1] 16 [2] [0] [-1] [0] [1] [1] q', is_autoadvancing=True)

    kaleid = kaleids.PartForcedChunkWithPatternedTokens([1], 16,
        prolation_addenda=[2],
        lefts=[0],
        middles=[-1],
        rights=[0],
        left_lengths=[1],
        right_lengths=[1],
        secondary_divisions=[],
        )

    assert editor.target == kaleid

import handlers
import scf


def test_TokenBurnishedSignalFilledTimeTokenMakerKaleidEditor_run_01():

    editor = scf.editors.TokenBurnishedSignalFilledTimeTokenMakerKaleidEditor()
    editor.run(user_input='1 [1, 1, 2, 4] 32 [0] [-1] [0] [-1] [2] [1] q', is_autoadvancing=True)
    
    kaleid = handlers.kaleids.TokenBurnishedSignalFilledTimeTokenMaker(
        [1, 1, 2, 4],
        32,
        prolation_addenda=[0],
        lefts=[-1],
        middles=[0],
        rights=[-1],
        left_lengths=[2],
        right_lengths=[1],
        secondary_divisions=[])

    assert editor.target == kaleid

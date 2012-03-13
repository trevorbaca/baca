from abjad import *
import handlers
import scf


def test_ReiteratedDynamicHandlerEditor_run_01():

    editor = scf.editors.ReiteratedDynamicHandlerEditor()
    editor.run(user_input="1 f Duration(1, 8) q", is_autoadvancing=True)

    handler = handlers.dynamics.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_prolated_duration=Duration(1, 8),
        )

    assert editor.target == handler

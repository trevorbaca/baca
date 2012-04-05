def get_time_token_maker_editor(target=None, session=None):
    from scf.wizards.TimeTokenMakerCreationWizard import TimeTokenMakerCreationWizard
    if target:
        wizard = TimeTokenMakerCreationWizard()
        time_token_maker_editor = wizard.get_handler_editor(target._class_name, target=target)
        return time_token_maker_editor

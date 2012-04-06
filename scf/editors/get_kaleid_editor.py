def get_kaleid_editor(target=None, session=None):
    from scf.wizards.TimeTokenMakerCreationWizard import TimeTokenMakerCreationWizard
    if target:
        wizard = TimeTokenMakerCreationWizard()
        kaleid_editor = wizard.get_handler_editor(target._class_name, target=target)
        return kaleid_editor

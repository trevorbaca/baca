def get_kaleid_editor(target=None, session=None):
    from scf.wizards.KaleidWizard import KaleidWizard
    if target:
        wizard = KaleidWizard()
        kaleid_editor = wizard.get_kaleid_editor(target._class_name, target=target)
        return kaleid_editor

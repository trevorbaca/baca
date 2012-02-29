def get_kaleid_editor(target=None, session=None):
    from scf.wizards.KaleidWizard import KaleidWizard
    print repr(target)
    print repr(session)
    if target:
        wizard = KaleidWizard()
        kaleid_editor = wizard.get_kaleid_editor(target._class_name)
        kaleid_editor._target = target
        return kaleid_editor

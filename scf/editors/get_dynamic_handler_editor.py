def get_dynamic_handler_editor(target=None, session=None):
    from scf.wizards.DynamicHandlerCreationWizard import DynamicHandlerCreationWizard
    if target:
        wizard = DynamicHandlerCreationWizard()
        dynamic_handler_editor = wizard.get_handler_editor(target._class_name, target=target)
        return dynamic_handler_editor

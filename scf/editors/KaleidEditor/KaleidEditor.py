from scf.editors.InteractiveEditor import InteractiveEditor


class KaleidEditor(InteractiveEditor):
    
    ### READ-ONLY ATTRIBUTES ###

    @property
    def target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target._class_name)
            result.append('')
            result.extend(InteractiveEditor.target_summary_lines.fget(self))
        return result

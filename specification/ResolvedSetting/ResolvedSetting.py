from baca.specification.Setting import Setting


class ResolvedSetting(Setting):
    
    ### CLASS ATTRIBUTES ###

    initializer_attribute_names = (
        'segment_name', 'context_name', 'scope', 'attribute_name', 'source', 'persistent', 'value', 
        'fresh',
        )

    ### INITIALIZER ###

    def __init__(self, 
        segment_name, context_name, scope, attribute_name, source, persistent, value, fresh=True):
        Setting.__init__(self, segment_name, context_name, scope, attribute_name, source, persistent)
        self.value = value
        self.fresh = fresh

from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.AttributeNameEnumeration import AttributeNameEnumeration


class DirectiveInventory(AbjadObject, list):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self):
        list.__init__(self)

    def __repr__(self):
        return '{}({})'.format(self._class_name, list.__repr__(self))

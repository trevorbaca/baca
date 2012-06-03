from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from baca.specification.AttributeNameEnumeration import AttributeNameEnumeration
from baca.specification.Directive import Directive


class DirectiveInventory(ObjectInventory):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Directive

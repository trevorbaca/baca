'''Set MenuSection.return_value_attr to one of 'body', 'key' or 'number'.
The behavior of the setting interacts with string tokens and tuple tokens as follows.
Behaviors marked (NB) are cases of forgiveness implemented such that the
system will always supply a return value, even where the return value
has to be selected from the next most likely available attribute.

When section has string tokens ...

    With numbering turned off ...

        * return body when return_value_attr set to 'body'
        * return body when return_value_attr set to 'key' (NB)
        * return body when return_value_attr set to 'number' (NB)

    With numbering turned on ...

        * return body when return_value_attr set to 'body'
        * return body when return_value_attr set to 'key' (NB)
        * return number when return_value_attr set to 'number'

When section has tuple tokens ...

    With numbering turned off ...

        * return body when return_value_attr set to 'body'
        * return key when return_value_attr set to 'key'
        * return key when return_value_attr set to 'number' (NB)

    With numbering turned on ...

        * return body when return_value_attr set to 'body'
        * return key when return_value_attr set to 'key'
        * return number when return_value_attr set to 'number'
'''

from MenuSection import MenuSection

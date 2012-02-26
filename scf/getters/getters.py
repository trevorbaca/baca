from scf.menuing.UserInputGetter import UserInputGetter


def get_duration(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_duration(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_integer(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_integer(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_string(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_string(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

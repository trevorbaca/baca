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

def get_integers(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_integers(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_markup(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_markup(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_nonnegative_integers(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_nonnegative_integers(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_nonzero_integers(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_nonzero_integers(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_positive_integer_power_of_two(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_positive_integer_power_of_two(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_positive_integers(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_positive_integers(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_string(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_string(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

def get_symbolic_pitch_range_string(attribute_spaced_name, session=None, existing_value=None, allow_none=True):
    getter = UserInputGetter(session=session)
    getter.append_symbolic_pitch_range_string(attribute_spaced_name)
    getter.allow_none = allow_none
    return getter

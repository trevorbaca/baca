from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import pitchtools
import re


def is_argument_range_string(expr):
    pattern = re.compile('^(\w+( *- *\w+)?)(, *\w+( *- *\w+)?)*$')
    return pattern.match(expr) is not None

def is_available_underscore_delimited_lowercase_package_name(expr):
    from baca.scf.SCFObject import SCFObject
    if iotools.is_underscore_delimited_lowercase_package_name(expr):
        if 3 <= len(expr):
            scf_object = SCFObject()
            return not scf_object.package_exists(expr)
    return False

def is_boolean(expr):
    return isinstance(expr, bool)

def is_existing_package_name(expr):
    from baca.scf.SCFObject import SCFObject
    scf_object = SCFObject()
    return scf_object.package_exists(expr)

def is_integer(expr):
    return isinstance(expr, int)

def is_integer_or_none(expr):
    return expr is None or is_integer(expr)

def is_markup(expr):
    return isinstance(expr, markuptools.Markup)

def is_markup_token(expr):
    try:
        result = markuptools.Markup(expr)
        return isinstance(result, markuptools.Markup)
    except:
        return False
        
def is_named_chromatic_pitch(expr):
    return isinstance(expr, pitchtools.NamedChromaticPitch)

def is_negative_integer(expr):
    return is_integer(expr) and expr < 0

def is_nonnegative_integer(expr):
    return is_integer(expr) and expr <= 0

def is_nonpositive_integer(expr):
    return is_integer(expr) and 0 <= expr

def is_pitch_range_or_none(expr):
    return isinstance(expr, (pitchtools.PitchRange, type(None)))

def is_positive_integer(expr):
    return is_integer(expr) and 0 < expr

def is_string(expr):
    return isinstance(expr, str)

def is_string_or_none(expr):
    return isinstance(expr, (str, type(None)))

def is_readable_argument_range_string_for_argument_list(argument_range_string, argument_list):
    from baca.scf.menuing.MenuSection import MenuSection
    if isinstance(argument_range_string, str):
        dummy_section = MenuSection()
        dummy_section.tokens = argument_list[:]
        if dummy_section.argument_range_string_to_numbers(argument_range_string) is not None:
            return True
    return False

def is_underscore_delimited_lowercase_package_name(expr):
    return iotools.is_underscore_delimited_lowercase_package_name(expr) and 3 <= len(expr)

def is_yes_no_string(expr):
    return 'yes'.startswith(expr.lower()) or 'no'.startswith(expr.lower())

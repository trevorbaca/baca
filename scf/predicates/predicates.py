from abjad.tools import markuptools
from abjad.tools import pitchtools


def is_argument_range_string(expr):
    pattern = re.compile('^(\w+( *- *\w+)?)(, *\w+( *- *\w+)?)*$')
    return pattern.match(expr) is not None

def is_boolean(expr):
    return isinstance(expr, bool)

def is_integer(expr):
    return isinstance(expr, int)

def is_integer_or_none(expr):
    return expr is None or is_integer(expr)

def is_markup(expr):
    return isinstance(expr, markuptools.Markup)

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

def is_valid_argument_range_string_for_argument_list(argument_range_string, argument_list):
    from baca.scf.menuing.MenuSection import MenuSection
    if isinstance(argument_range_string, str):
        dummy_section = MenuSection()
        dummy_section.tokens = argument_list[:]
        if dummy_section.argument_range_string_to_numbers(argument_range_string) is not None:
            return True
    return False

def is_yes_no_string(expr):
    return 'yes'.startswith(expr.lower()) or 'no'.startswith(expr.lower())

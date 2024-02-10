import enum
import types


class enums(enum.Enum):
    ALREADY_PITCHED = enum.auto()
    ALLOW_OCTAVE = enum.auto()
    ALLOW_OUT_OF_RANGE = enum.auto()
    ALLOW_REPEAT_PITCH = enum.auto()
    ANCHOR_NOTE = enum.auto()
    ANCHOR_SKIP = enum.auto()

    BOW_SPEED = enum.auto()

    CIRCLE_BOW = enum.auto()
    CLB = enum.auto()
    CLOCK_TIME_RESTART = enum.auto()
    COVERED = enum.auto()

    DAMP = enum.auto()
    DO_NOT_TRANSPOSE = enum.auto()

    FERMATA_MEASURE = enum.auto()
    FERMATA_DURATION = enum.auto()
    FRAMED_LEAF = enum.auto()

    HALF_CLT = enum.auto()
    HIDDEN = enum.auto()
    HIDDEN_NOTE_VOICE = enum.auto()

    INTERMITTENT = enum.auto()

    MATERIAL = enum.auto()
    MOCK = enum.auto()
    MULTIMEASURE_REST = enum.auto()
    MULTIMEASURE_REST_CONTAINER = enum.auto()

    NOT_YET_PITCHED = enum.auto()
    NOT_YET_REGISTERED = enum.auto()
    NOTE = enum.auto()

    PITCH = enum.auto()

    RHYTHM = enum.auto()
    REMOVE_ALL_EMPTY_STAVES = enum.auto()
    REPEAT_PITCH_CLASS = enum.auto()
    REST_VOICE = enum.auto()
    RIGHT_OPEN_BEAM = enum.auto()

    SCP = enum.auto()
    SKIP = enum.auto()
    SOUNDS_DURING_SECTION = enum.auto()
    SPAZZOLATO = enum.auto()
    STAFF_POSITION = enum.auto()
    STRING_NUMBER = enum.auto()

    TEMPORARY_CONTAINER = enum.auto()

    TASTO = enum.auto()

    VIBRATO = enum.auto()


colors = types.SimpleNamespace(
    blue="\033[94m",
    cyan="\033[36m",
    end="\033[0m",
    green="\033[32m",
    green_bold="\033[1;32m",
    magenta="\033[35m",
    red="\033[91m",
    red_bold="\033[1;31m",
    yellow="\033[33m",
)


def dummy():
    """
    Read module-level items.
    """

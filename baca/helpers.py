"""
Other functions.
"""
import os

import abjad


def call(argument):
    if callable(argument):
        argument()
    else:

        def composite(function):
            function(argument)

        return composite


def function_name(frame, *, n=None):
    """
    Gets function (and class) name from ``frame``.
    """
    parts = []
    path = frame.f_code.co_filename.removesuffix(".py")
    found_library = False
    for part in reversed(path.split(os.sep)):
        parts.append(part)
        if part == "baca":
            break
        if found_library:
            break
        if part == "library":
            found_library = True
    parts = [_ for _ in parts if _ != "library"]
    parts.reverse()
    if parts[0] == "baca":
        parts.pop()
    if "self" in frame.f_locals:
        class_name = frame.f_locals["self"].__class__.__name__
        parts.append(class_name)
    parts.append(frame.f_code.co_name)
    string = ".".join(parts) + ("()" if n is None else f"({n})")
    return abjad.Tag(string)

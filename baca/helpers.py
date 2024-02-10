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
    file_name = path.split(os.sep)[-1]
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
    modules = ("array", "build", "dynamics", "math", "mspanners", "override", "path")
    # TODO: add "rspanners"
    modules += ("piecewise", "score", "section", "select", "sequence", "spanners")
    modules += ("treat", "typings")
    if file_name in modules:
        parts.append(file_name)
    if "self" in frame.f_locals:
        class_name = frame.f_locals["self"].__class__.__name__
        parts.append(class_name)
    parts.append(frame.f_code.co_name)
    string = ".".join(parts) + ("()" if n is None else f"({n})")
    return abjad.Tag(string)

"""
Score.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers


def assert_lilypond_identifiers(score):
    for context in abjad.iterate.components(score, abjad.Context):
        if not abjad.string.is_lilypond_identifier(context.name):
            raise Exception(f"invalid LilyPond identifier: {context.name!r}")


def assert_unique_context_names(score):
    names = []
    for context in abjad.iterate.components(score, abjad.Context):
        if context.name in names:
            raise Exception(f"duplicate context name: {context.name!r}.")


def attach_lilypond_tag(tag, context, *, part_manifest=None):
    if not abjad.string.is_lilypond_identifier(tag):
        raise Exception(f"invalid LilyPond identifier: {tag!r}.")
    part_names = []
    if part_manifest is not None:
        part_names = [_.name for _ in part_manifest.parts]
    if part_names and tag not in part_names:
        raise Exception(f"not listed in parts manifest: {tag!r}.")
    literal = abjad.LilyPondLiteral(rf"\tag #'{tag}", site="before")
    tag = _helpers.function_name(_frame())
    abjad.attach(literal, context, tag=tag)


def make_global_context(
    *,
    make_breaks_context=False,
    make_spacing_annotations_context=False,
    make_spacing_commands_context=False,
):
    tag = _helpers.function_name(_frame())
    contexts = []
    context = abjad.Context(
        lilypond_type="GlobalRests",
        name="Rests",
        tag=tag,
    )
    contexts.append(context)
    context = abjad.Context(
        lilypond_type="GlobalSkips",
        name="Skips",
        tag=tag,
    )
    contexts.append(context)
    if make_breaks_context is True:
        context = abjad.Context(
            lilypond_type="GlobalSkips",
            name="Breaks",
            tag=tag,
        )
        contexts.append(context)
    if make_spacing_commands_context is True:
        context = abjad.Context(
            lilypond_type="GlobalSkips",
            name="SpacingCommands",
            tag=tag,
        )
        contexts.append(context)
    if make_spacing_annotations_context is True:
        context = abjad.Context(
            lilypond_type="GlobalSkips",
            name="SpacingAnnotations",
            tag=tag,
        )
        contexts.append(context)
    global_context = abjad.Context(
        contexts,
        lilypond_type="GlobalContext",
        simultaneous=True,
        name="GlobalContext",
        tag=tag,
    )
    return global_context


def make_music_context(*contexts):
    contexts = tuple(_ for _ in contexts if _ is not None)
    tag = _helpers.function_name(_frame())
    return abjad.Context(
        contexts,
        lilypond_type="MusicContext",
        simultaneous=True,
        name="MusicContext",
        tag=tag,
    )


def make_staff_group(stem, *contexts):
    if not isinstance(stem, str):
        raise Exception(f"stem must be string: {stem!r}.")
    tag = _helpers.function_name(_frame())
    contexts = tuple(_ for _ in contexts if _ is not None)
    if contexts:
        return abjad.StaffGroup(contexts, name=f"{stem}StaffGroup", tag=tag)
    else:
        return None

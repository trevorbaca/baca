"""
Templates.
"""
from inspect import currentframe as _frame

import abjad

from . import scoping as _scoping


def assert_lilypond_identifiers(score):
    for context in abjad.iterate.components(score, abjad.Context):
        if not abjad.string.is_lilypond_identifier(context.name):
            raise Exception(f"invalid LilyPond identifier: {context.name!r}")


def assert_matching_custom_context_names(score):
    for context in abjad.iterate.components(score, abjad.Context):
        if context.lilypond_type in abjad.Context.lilypond_types:
            continue
        if context.name == context.lilypond_type:
            continue
        if context.name.replace("_", "") == context.lilypond_type:
            continue
        raise Exception(f"context {context.lilypond_type} has name {context.name!r}.")


def assert_unique_context_names(score):
    names = []
    for context in abjad.iterate.components(score, abjad.Context):
        if context.name in names:
            raise Exception(f"duplicate context name: {context.name!r}.")


def attach_lilypond_tag(tag, context, *, part_manifest=None):
    for tag_ in tag.split("."):
        if not abjad.string.is_lilypond_identifier(tag_):
            raise Exception(f"invalid LilyPond identifier: {tag_!r}.")
        part_names = []
        if part_manifest is not None:
            part_names = [_.name for _ in part_manifest.parts]
        if part_names and tag_ not in part_names:
            raise Exception(f"not listed in parts manifest: {tag_!r}.")
    literal = abjad.LilyPondLiteral(rf"\tag {tag}", "before")
    tag = _scoping.site(_frame())
    abjad.attach(literal, context, tag=tag)


def make_global_context():
    tag = _scoping.site(_frame())
    global_rests = abjad.Context(
        lilypond_type="GlobalRests",
        name="Global_Rests",
        tag=tag,
    )
    global_skips = abjad.Context(
        lilypond_type="GlobalSkips",
        name="Global_Skips",
        tag=tag,
    )
    global_context = abjad.Context(
        [global_rests, global_skips],
        lilypond_type="GlobalContext",
        simultaneous=True,
        name="Global_Context",
        tag=tag,
    )
    return global_context


def make_music_context(*contexts):
    contexts = tuple(_ for _ in contexts if _ is not None)
    tag = _scoping.site(_frame())
    return abjad.Context(
        contexts,
        lilypond_type="MusicContext",
        simultaneous=True,
        name="Music_Context",
        tag=tag,
    )


def make_staff_group(stem, *contexts):
    if not isinstance(stem, str):
        raise Exception(f"stem must be string: {stem!r}.")
    tag = _scoping.site(_frame())
    contexts = tuple(_ for _ in contexts if _ is not None)
    if contexts:
        return abjad.StaffGroup(contexts, name=f"{stem}_Staff_Group", tag=tag)
    else:
        return None

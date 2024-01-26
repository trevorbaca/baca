"""
Figures.
"""

import dataclasses
import typing

import abjad

from . import select as _select
from . import tags as _tags


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Anchor:
    """
    Anchor.

    ``use_remote_stop_offset`` is true when contribution anchors to remote components'
    stop offset; otherwise anchors to remote components' start offset.
    """

    figure_name: str | None = None
    local_selector: typing.Callable | None = None
    remote_selector: typing.Callable | None = None
    remote_voice_name: str | None = None
    use_remote_stop_offset: bool = False

    def __post_init__(self):
        if self.figure_name is not None:
            assert isinstance(self.figure_name, str), repr(self.figure_name)
        if self.local_selector is not None and not callable(self.local_selector):
            raise TypeError(f"must be callable: {self.local_selector!r}.")
        if self.remote_selector is not None and not callable(self.remote_selector):
            raise TypeError(f"must be callable: {self.remote_selector!r}.")
        if self.remote_voice_name is not None:
            assert isinstance(self.remote_voice_name, str), repr(self.remote_voice_name)
        assert isinstance(self.use_remote_stop_offset, bool), repr(
            self.use_remote_stop_offset
        )


def anchor(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to start offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
    )


def anchor_after(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to stop offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def anchor_to_figure(figure_name: str) -> Anchor:
    """
    Anchors music in this figure to start of ``figure_name``.
    """
    return Anchor(figure_name=figure_name)


def label_figure(
    tuplets, figure_name, accumulator, direction=None, do_not_increment=False
):
    figure_name = figure_name or ""
    figure_number = accumulator.figure_number
    if not do_not_increment:
        accumulator.figure_number += 1
    parts = figure_name.split("_")
    if len(parts) == 1:
        body = parts[0]
        figure_label_string = f'"{body}"'
    elif len(parts) == 2:
        body, subscript = parts
        figure_label_string = rf'\concat {{ "{body}" \sub {subscript} }}'
    else:
        raise Exception(f"unrecognized figure name: {figure_name!r}.")
    string = r"\markup"
    string += rf" \concat {{ [ \raise #0.25 \fontsize #-2 ({figure_number})"
    if figure_name:
        string += rf" \hspace #1 {figure_label_string} ] }}"
    else:
        string += r" ] }"
    figure_label_markup = abjad.Markup(string)
    bundle = abjad.bundle(figure_label_markup, r"- \tweak color #blue")
    leaf = abjad.select.leaf(tuplets, 0)
    abjad.annotate(leaf, "figure_name", figure_name)
    if not do_not_increment:
        pleaves = _select.pleaves(tuplets)
        if pleaves:
            leaf = pleaves[0]
        else:
            leaf = abjad.select.leaf(tuplets, 0)
        abjad.attach(
            bundle,
            leaf,
            deactivate=True,
            direction=direction,
            tag=_tags.FIGURE_LABEL,
        )


def resume() -> Anchor:
    """
    Resumes music at next offset across all voices in score.
    """
    return Anchor()


def resume_after(remote_voice_name) -> Anchor:
    """
    Resumes music after remote components.
    """
    return Anchor(
        remote_selector=lambda _: abjad.select.leaf(_, -1),
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )

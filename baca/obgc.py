import abjad
import typing


class OnBeatGraceContainer(abjad.GraceContainer):
    """
    On-beat grace container.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

    ###__slots__ = ("_command", "_main_leaf")
    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, components=None, *, tag: str = None) -> None:
        abjad.GraceContainer.__init__(self, components, tag=tag)

    ### PRIVATE METHODS ###

    def _format_open_brackets_slot(self, bundle):
        result = []
        string = f"{self.command} {{"
        result.append([("grace_brackets", "open"), [string]])
        return tuple(result)

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

import abjad
import collections


class LBSD(abjad.AbjadObject):
    """
    Line-break system details.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_alignment_distances',
        '_y_offset',
        )

    _override = r'\overrideProperty'
    _override += ' Score.NonMusicalPaperColumn.line-break-system-details'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        y_offset=None,
        alignment_distances=None,
        ):
        self._y_offset = y_offset
        if alignment_distances is not None:
            assert isinstance(alignment_distances, collections.Iterable)
            alignment_distances = tuple(alignment_distances)
        self._alignment_distances = alignment_distances

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        alignment_distances = ' '.join(
            str(_) for _ in self.alignment_distances
            )
        string = rf"\baca_lbsd #{self.y_offset} #'({alignment_distances})"
        bundle.before.commands.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def alignment_distances(self):
        """
        Gets alignment distances.
        """
        return self._alignment_distances

    @property
    def y_offset(self):
        """
        Gets Y offset.
        """
        return self._y_offset

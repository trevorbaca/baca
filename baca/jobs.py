"""
Jobs.
"""
import pathlib

import abjad

from . import path as _path
from . import tags as _tags


class Job:
    """
    Job.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_activate",
        "_deactivate",
        "_deactivate_first",
        "_message_zero",
        "_path",
        "_prepend_empty_chord",
        "_skip_file_name",
        "_title",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        activate=None,
        deactivate=None,
        deactivate_first=None,
        message_zero=None,
        path=None,
        prepend_empty_chord=None,
        skip_file_name=None,
        title=None,
    ):
        self._activate = activate
        self._deactivate = deactivate
        self._deactivate_first = deactivate_first
        self._message_zero = message_zero
        self._path = path
        self._prepend_empty_chord = prepend_empty_chord
        self._skip_file_name = skip_file_name
        self._title = title

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls job on job ``path``.
        """
        messages = []
        if self.title is not None:
            messages.append(self.title)
        total_count = 0
        if isinstance(self.path, str):
            text = self.path
        if self.deactivate_first is True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, pathlib.Path):
                        result = _path.deactivate(
                            self.path,
                            match,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str), repr(self.path)
                        result = abjad.deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
                        assert result is not None
                        text, count, skipped = result
        if self.activate is not None:
            assert isinstance(self.activate, tuple)
            match, name = self.activate
            if match is not None:
                if isinstance(self.path, pathlib.Path):
                    result = _path.activate(
                        self.path,
                        match,
                        message_zero=True,
                        name=name,
                        skip_file_name=self.skip_file_name,
                    )
                    assert result is not None
                    count, skipped, messages_ = result
                    messages.extend(messages_)
                    total_count += count
                else:
                    assert isinstance(self.path, str)
                    text, count, skipped = abjad.activate(
                        text,
                        match,
                        skip_file_name=self.skip_file_name,
                        skipped=True,
                    )
        if self.deactivate_first is not True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, pathlib.Path):
                        result = _path.deactivate(
                            self.path,
                            match,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str)
                        text, count, skipped = abjad.deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
        if total_count == 0 and not self.message_zero:
            messages = []
        if isinstance(self.path, pathlib.Path):
            return messages
        else:
            assert isinstance(self.path, str)
            return text

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def activate(self):
        """
        Gets activate match / message pair.
        """
        return self._activate

    @property
    def deactivate(self):
        """
        Gets deactivate match / message pair.
        """
        return self._deactivate

    @property
    def deactivate_first(self):
        """
        Is true when deactivate runs first.
        """
        return self._deactivate_first

    @property
    def message_zero(self):
        """
        Is true when job returns messages even when no matches are found.
        """
        return self._message_zero

    @property
    def path(self):
        """
        Gets path.
        """
        return self._path

    @property
    def prepend_empty_chord(self):
        """
        Is true when deactivate prepends LilyPond empty chord ``<>`` command.
        """
        return self._prepend_empty_chord

    @property
    def skip_file_name(self):
        """
        Gets skip file name.
        """
        return self._skip_file_name

    @property
    def title(self):
        """
        Gets title.
        """
        return self._title


def color_clefs(path, undo=False):
    name = "clef color"

    def match(tags):
        tags_ = _tags.clef_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            deactivate=(match, name),
            path=path,
            title="Uncoloring clefs ...",
        )
    else:
        return Job(activate=(match, name), path=path, title="Coloring clefs ...")


def color_dynamics(path, undo=False):
    name = "dynamic color"

    def match(tags):
        tags_ = _tags.dynamic_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            deactivate=(match, name),
            path=path,
            title="Uncoloring dynamics ...",
        )
    else:
        return Job(
            activate=(match, name),
            path=path,
            title="Coloring dynamics ...",
        )


def color_instruments(path, undo=False):
    """
    Colors instruments.
    """
    name = "instrument color"

    def match(tags):
        tags_ = _tags.instrument_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            deactivate=(match, name),
            path=path,
            title="Uncoloring instruments ...",
        )
    else:
        return Job(
            activate=(match, name),
            path=path,
            title="Coloring instruments ...",
        )


def color_margin_markup(path, undo=False):
    """
    Colors margin markup.
    """
    name = "margin markup color"

    def match(tags):
        tags_ = _tags.margin_markup_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            deactivate=(match, name),
            path=path,
            title="Uncoloring margin markup ...",
        )
    else:
        return Job(
            activate=(match, name),
            path=path,
            title="Coloring margin markup ...",
        )


def color_metronome_marks(path, undo=False):
    """
    Colors metronome marks.
    """

    def activate(tags):
        tags_ = _tags.metronome_mark_color_expression_tags(path)
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = _tags.metronome_mark_color_suppression_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            activate=(deactivate, "metronome mark color suppression"),
            deactivate=(activate, "metronome mark color expression"),
            path=path,
            title="Uncoloring metronome marks ...",
        )
    else:
        return Job(
            activate=(activate, "metronome mark color expression"),
            deactivate=(deactivate, "metronome mark color suppression"),
            path=path,
            title="Coloring metronome marks ...",
        )


def color_persistent_indicators(path, undo=False):
    """
    Color persistent indicators.
    """
    name = "persistent indicator"
    activate_name = "persistent indicator color expression"

    def activate(tags):
        tags_ = _tags.persistent_indicator_color_expression_tags(path)
        return bool(set(tags) & set(tags_))

    deactivate_name = "persistent indicator color suppression"

    def deactivate(tags):
        tags_ = _tags.persistent_indicator_color_suppression_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            activate=(deactivate, deactivate_name),
            deactivate=(activate, activate_name),
            path=path,
            title=f"Uncoloring {name}s ...",
        )
    else:
        return Job(
            activate=(activate, activate_name),
            deactivate=(deactivate, deactivate_name),
            path=path,
            title=f"Coloring {name}s ...",
        )


def color_staff_lines(path, undo=False):
    """
    Colors staff lines.
    """
    name = "staff lines color"

    def match(tags):
        tags_ = _tags.staff_lines_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            deactivate=(match, name),
            path=path,
            title="Uncoloring staff lines ...",
        )
    else:
        return Job(
            activate=(match, name),
            path=path,
            title="Coloring staff lines ...",
        )


def color_time_signatures(path, undo=False):
    """
    Colors time signatures.
    """
    name = "time signature color"

    def match(tags):
        tags_ = _tags.time_signature_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            deactivate=(match, name),
            path=path,
            title="Uncoloring time signatures ...",
        )
    else:
        return Job(
            activate=(match, name),
            path=path,
            title="Coloring time signatures ...",
        )


def handle_edition_tags(path):
    """
    Handles edition tags.

    The logic here is important:

        * deactivations run first:

            -TAG (where TAG is either my directory or my buildtype)

            +TAG (where TAG is neither my directory nor my buildtype)

        * activations run afterwards:

            TAG_SET such that there exists at least one build-forbid -TAG (equal to
            neither my directory nor my buildtype) in TAG_SET and such that there exists
            no -TAG (equal to either my directory or my buildtype) in TAG_SET

            +TAG (where TAG is either my directory or my buildtype)

        Notionally: first we deactivate anything that is tagged EITHER specifically
        against me OR specifically for another build; then we activate anything that is
        deactivated for editions other than me; then we activate anything is tagged
        specifically for me.

    ..  todo: Tests.

    """
    if path.parent.parent.name == "segments":
        my_name = "SEGMENT"
    elif path.name.endswith("-score") or path.parent.name.endswith("-score"):
        my_name = "SCORE"
    elif path.name.endswith("-parts"):
        my_name = "PARTS"
    elif path.parent.name.endswith("-parts"):
        my_name = "PARTS"
    else:
        raise Exception(path)
    this_edition = abjad.Tag(f"+{abjad.String(my_name).to_shout_case()}")
    not_this_edition = abjad.Tag(f"-{abjad.String(my_name).to_shout_case()}")
    if path.is_dir():
        directory_name = path.name
    else:
        directory_name = path.parent.name
    this_directory = abjad.Tag(f"+{abjad.String(directory_name).to_shout_case()}")
    not_this_directory = abjad.Tag(f"-{abjad.String(directory_name).to_shout_case()}")

    def deactivate(tags):
        if not_this_edition in tags:
            return True
        if not_this_directory in tags:
            return True
        for tag in tags:
            if str(tag).startswith("+"):
                return True
        return False

    def activate(tags):
        for tag in tags:
            if tag in [not_this_edition, not_this_directory]:
                return False
        for tag in tags:
            if str(tag).startswith("-"):
                return True
        return bool(set(tags) & set([this_edition, this_directory]))

    return Job(
        activate=(activate, "this-edition"),
        deactivate=(deactivate, "other-edition"),
        deactivate_first=True,
        path=path,
        title="Handling edition tags ...",
    )


def handle_fermata_bar_lines(path):
    """
    Handles fermata bar lines.
    """
    if path.name == "_segments":
        path = path.parent

    def activate(tags):
        return bool(set(tags) & set([_tags.FERMATA_MEASURE]))

    # then deactivate non-EOL tags:
    bol_measure_numbers = _path.get_metadatum(path, "bol_measure_numbers")
    if bol_measure_numbers:
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        final_measure_number = _path.get_metadatum(path, "final_measure_number")
        if final_measure_number is not None:
            eol_measure_numbers.append(final_measure_number)
        eol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

        def deactivate(tags):
            if _tags.FERMATA_MEASURE in tags:
                if not bool(set(tags) & set(eol_measure_numbers)):
                    return True
            return False

    else:
        deactivate = None
    return Job(
        activate=(activate, "bar line adjustment"),
        deactivate=(deactivate, "EOL fermata bar line"),
        path=path,
        title="Handling fermata bar lines ...",
    )


def handle_mol_tags(path):
    """
    Handles MOL (middle-of-line) tags.
    """
    if path.name == "_segments":
        path = path.parent

    # activate all middle-of-line tags
    def activate(tags):
        tags_ = set([_tags.NOT_MOL, _tags.ONLY_MOL])
        return bool(set(tags) & tags_)

    # then deactivate conflicting middle-of-line tags
    bol_measure_numbers = _path.get_metadatum(path, "bol_measure_numbers")
    if bol_measure_numbers:
        nonmol_measure_numbers = bol_measure_numbers[:]
        final_measure_number = _path.get_metadatum(path, "final_measure_number")
        if final_measure_number is not None:
            nonmol_measure_numbers.append(final_measure_number + 1)
        nonmol_measure_numbers = [
            abjad.Tag(f"MEASURE_{_}") for _ in nonmol_measure_numbers
        ]

        def deactivate(tags):
            if _tags.NOT_MOL in tags:
                if not bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            if _tags.ONLY_MOL in tags:
                if bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            return False

    else:
        deactivate = None
    return Job(
        activate=(activate, "MOL"),
        deactivate=(deactivate, "conflicting MOL"),
        path=path,
        title="Handling MOL tags ...",
    )


def handle_shifted_clefs(path):
    """
    Handles shifted clefs.
    """

    def activate(tags):
        return _tags.SHIFTED_CLEF in tags

    # then deactivate shifted clefs at BOL:
    if path.name == "_segments":
        metadata_source = path.parent
    else:
        metadata_source = path
    string = "bol_measure_numbers"
    bol_measure_numbers = _path.get_metadatum(metadata_source, string)
    if bol_measure_numbers:
        bol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

        def deactivate(tags):
            if _tags.SHIFTED_CLEF not in tags:
                return False
            if any(_ in tags for _ in bol_measure_numbers):
                return True
            return False

    else:
        deactivate = None
    return Job(
        activate=(activate, "shifted clef"),
        deactivate=(deactivate, "BOL clef"),
        path=path,
        title="Handling shifted clefs ...",
    )


def hide_default_clefs(path, undo=False):
    """
    Hides default clefs.
    """
    name = "default clef"

    def match(tags):
        tags_ = [_tags.DEFAULT_CLEF]
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            activate=(match, name),
            path=path,
            title="Showing default clefs ...",
        )
    else:
        return Job(
            deactivate=(match, name),
            path=path,
            title="Hiding default clefs ...",
        )


def join_broken_spanners(path):
    """
    Joins broken spanners.
    """

    def activate(tags):
        tags_ = [_tags.SHOW_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = [_tags.HIDE_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    return Job(
        activate=(activate, "broken spanner expression"),
        deactivate=(deactivate, "broken spanner suppression"),
        path=path,
        title="Joining broken spanners ...",
    )


def show_music_annotations(path, undo=False):
    """
    Shows music annotations.
    """
    name = "music annotation"

    def match(tags):
        tags_ = _tags.music_annotation_tags()
        return bool(set(tags) & set(tags_))

    def match_2(tags):
        tags_ = [_tags.INVISIBLE_MUSIC_COMMAND]
        return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            activate=(match_2, name),
            deactivate=(match, name),
            path=path,
            title=f"Hiding {name}s ...",
        )
    else:
        return Job(
            activate=(match, name),
            deactivate=(match_2, name),
            path=path,
            title=f"Showing {name}s ...",
        )


def show_tag(
    path,
    tag,
    *,
    match=None,
    prepend_empty_chord=None,
    skip_file_name=None,
    undo=False,
):
    """
    Shows tag.
    """
    if isinstance(tag, str):
        assert match is not None, repr(match)
    else:
        assert isinstance(tag, abjad.Tag), repr(tag)
    name = str(tag)

    if match is None:

        def match(tags):
            tags_ = [tag]
            return bool(set(tags) & set(tags_))

    if undo:
        return Job(
            deactivate=(match, name),
            path=path,
            prepend_empty_chord=prepend_empty_chord,
            skip_file_name=skip_file_name,
            title=f"Hiding {name} tags ...",
        )
    else:
        return Job(
            activate=(match, name),
            path=path,
            skip_file_name=skip_file_name,
            title=f"Showing {name} tags ...",
        )

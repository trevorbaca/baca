import os
import pathlib
import shutil
import typing

import abjad

configuration = abjad.Configuration()


class Path(pathlib.PosixPath):
    """
    Path in score package.
    """

    ### CLASS VARIABLES ###

    _secondary_names = (
        ".gitignore",
        ".log",
        ".timing",
        "__init__.py",
        "__make_pdf__.py",
        "__make_midi__.py",
        "__metadata__",
        "__persist__",
        "_assets",
        "_segments",
        "illustration.untagged.ily",
        "illustration.untagged.ly",
        "layout.untagged.ly",
        "stylesheet.ily",
    )

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation of path.
        """
        return f"Path('{self}')"

    ### PRIVATE PROPERTIES ###

    @property
    def _assets(self):
        """
        Gets _assets directory.
        """
        if self.is_builds():
            return self / "_assets"
        if self.is_score_build():
            return self / "_assets"
        if self.is_parts():
            return self / "_assets"
        if self.is_part():
            return self.parent / "_assets"
        return None

    @property
    def _segments(self):
        """
        Gets _segments directory.
        """
        if self.is__assets():
            return self.parent / "_segments"
        if self.is__segments():
            return self
        if self.is_score_build():
            return self / "_segments"
        if self.is_parts():
            return self / "_segments"
        if self.is_part():
            return self.parent / "_segments"
        if self.parent._segments is not None:
            return self.parent._segments
        return None

    ### PUBLIC PROPERTIES ###

    @property
    def build(self):
        """
        Gets build directory.
        """
        if self.is_build():
            return self
        elif self.parent.is_build():
            return self.parent
        else:
            return None

    @property
    def builds(self):
        """
        Gets builds directory.
        """
        if self.contents:
            return self.contents / "builds"
        else:
            return None

    @property
    def contents(self):
        """
        Gets contents directory.
        """
        parts = str(self).split(os.sep)
        previous_part = None
        for i, part in enumerate(reversed(parts)):
            if part == previous_part:
                if i == 1:
                    return self
                wrapper = os.sep.join(parts[: -(i - 1)])
                wrapper = Path(wrapper)
                return wrapper
            previous_part = part
        return None

    @property
    def distribution(self):
        """
        Gets distribution directory.
        """
        if self.contents:
            return self.contents / "distribution"
        else:
            return None

    @property
    def etc(self):
        """
        Gets etc directory.
        """
        if self.contents:
            return self.contents / "etc"
        else:
            return None

    @property
    def scores(self):
        """
        Gets scores directory.
        """
        path = os.path.expanduser("~")
        path = Path(path) / "Scores"
        return None
        return path

    @property
    def segments(self):
        """
        Gets segments directory.
        """
        if self.contents:
            return self.contents / "segments"
        else:
            return None

    @property
    def wrapper(self):
        """
        Gets wrapper directory.
        """
        parts = str(self).split(os.sep)
        previous_part = None
        for i, part in enumerate(reversed(parts)):
            if part == previous_part:
                wrapper = os.sep.join(parts[:-i])
                wrapper = Path(wrapper)
                return wrapper
            previous_part = part
        return None

    ### PUBLIC METHODS ###

    def activate(
        self,
        tag,
        *,
        indent=0,
        message_zero=False,
        name=None,
        prepend_empty_chord=None,
        skip_file_name=None,
        undo=False,
    ):
        """
        Activates ``tag`` in path.

        Case 0: path is a non-LilyPond file. Method does nothing.

        Case 1: path is a LilyPond (.ily, .ly) file starting with
        ``illustration``, ``layout`` or ``segment``. Method activates ``tag``
        in file.

        Case 2: path is a directory. Method descends directory recursively and
        activates ``tag`` in LilyPond files given in case 1.

        Returns triple.

        First item in triple is count of deactivated tags activated by method.

        Second item in pair is count of already-active tags skipped by method.

        Third item in pair is list of canonical string messages that explain
        what happened.
        """
        if isinstance(tag, str):
            raise Exception(f"must be tag or callable: {tag!r}")
        if self.name == skip_file_name:
            return None
        assert isinstance(indent, int), repr(indent)
        if self.is_file():
            if self.suffix not in (".ily", ".ly"):
                count, skipped = 0, 0
            else:
                text = self.read_text()
                if undo:
                    text, count, skipped = abjad.deactivate(
                        text,
                        tag,
                        prepend_empty_chord=prepend_empty_chord,
                        skipped=True,
                    )
                else:
                    text, count, skipped = abjad.activate(text, tag, skipped=True)
                self.write_text(text)
        else:
            assert self.is_dir(), repr(self)
            count, skipped = 0, 0
            for path in sorted(self.glob("**/*")):
                path = type(self)(path)
                if path.suffix not in (".ily", ".ly"):
                    continue
                if not (
                    path.name.startswith("illustration")
                    or path.name.startswith("layout")
                    or path.name.startswith("segment")
                ):
                    continue
                if path.name == skip_file_name:
                    continue
                result = path.activate(
                    tag, prepend_empty_chord=prepend_empty_chord, undo=undo
                )
                assert result is not None
                count_, skipped_, _ = result
                count += count_
                skipped += skipped_
        if name is None:
            name = str(tag)
        if undo:
            adjective = "inactive"
            gerund = "deactivating"
        else:
            adjective = "active"
            gerund = "activating"
        messages = []
        total = count + skipped
        if total == 0 and message_zero:
            messages.append(f"found no {name} tags")
        if 0 < total:
            tags = abjad.String("tag").pluralize(total)
            messages.append(f"found {total} {name} {tags}")
            if 0 < count:
                tags = abjad.String("tag").pluralize(count)
                message = f"{gerund} {count} {name} {tags}"
                messages.append(message)
            if 0 < skipped:
                tags = abjad.String("tag").pluralize(skipped)
                message = f"skipping {skipped} ({adjective}) {name} {tags}"
                messages.append(message)
        whitespace = indent * " "
        messages_ = [
            abjad.String(whitespace + abjad.String(_).capitalize_start() + " ...")
            for _ in messages
        ]
        return count, skipped, messages_

    def add_buildspace_metadatum(self, name, value, document_name=None):
        """
        Adds metadatum with ``name`` and ``value`` into buildspace metadata
        with optional ``document_name``.
        """
        assert self.is_buildspace(), repr(self)
        if self.is_parts():
            if document_name is not None:
                part_dictionary = self.get_metadatum(document_name, abjad.OrderedDict())
            else:
                part_dictionary = abjad.OrderedDict()
            part_dictionary[name] = value
            assert abjad.String(document_name).is_shout_case()
            self.add_metadatum(document_name, part_dictionary)
        else:
            self.add_metadatum(name, value)

    def add_metadatum(self, name, value, *, file_name="__metadata__"):
        """
        Adds metadatum.
        """
        assert " " not in name, repr(name)
        metadata = self.get_metadata(file_name=file_name)
        metadata[name] = value
        self.write_metadata_py(metadata)

    def count(self, tag):
        """
        Counts ``tag`` in path.

        Returns two pairs.

        Pair 1 gives (active tags, activate lines).

        Pair 2 gives (deactivated tags, deactivated lines).
        """
        assert isinstance(tag, str) or callable(tag), repr(tag)
        assert self.is_file(), repr(self)
        active_tags, active_lines = 0, 0
        deactivated_tags, deactivated_lines = 0, 0
        with open(self) as pointer:
            last_line_had_tag = False
            for line_ in pointer.readlines():
                line = abjad.Line(line_)
                if line.match(tag):
                    if line.is_active():
                        active_lines += 1
                        if not last_line_had_tag:
                            active_tags += 1
                    else:
                        deactivated_lines += 1
                        if not last_line_had_tag:
                            deactivated_tags += 1
                    last_line_had_tag = True
                else:
                    last_line_had_tag = False
        pair_1 = (active_tags, active_lines)
        pair_2 = (deactivated_tags, deactivated_lines)
        return pair_1, pair_2

    def deactivate(
        self,
        tag,
        *,
        indent=0,
        message_zero=False,
        name=None,
        prepend_empty_chord=None,
        skip_file_name=None,
    ):
        """
        Deactivates ``tag`` in path.
        """
        if isinstance(tag, str):
            raise Exception(f"must be tag or callable: {tag!r}")
        return self.activate(
            tag,
            name=name,
            indent=indent,
            message_zero=message_zero,
            prepend_empty_chord=prepend_empty_chord,
            skip_file_name=skip_file_name,
            undo=True,
        )

    def extern(
        self,
        *,
        include_path=None,
        score_path=None,
    ):
        """
        Externalizes LilyPond file parsable chunks.

        Produces skeleton ``.ly`` together with ``.ily``.

        Writes skeleton ``.ly`` to ``score_path`` when ``score_path`` is set.
        Overwrites this path with skeleton ``.ly`` when ``score_path`` is
        unset.

        Writes ``.ily`` to ``include_path`` when ``include_path`` is set.
        Writes ``.ily`` to this path with ``.ily` suffix when ``include_path``
        is not set.
        """
        tag = abjad.Tag("baca.Path.extern()")
        if not self.suffix == ".ly":
            raise Exception(f"must be lilypond file: {self}.")
        if include_path is None:
            include_path = self.with_suffix(".ily")
        assert isinstance(include_path, type(self)), repr(include_path)
        if score_path is None:
            score_path = self
        assert isinstance(score_path, type(self)), repr(score_path)
        preamble_lines, score_lines = [], []
        stack, finished_variables = abjad.OrderedDict(), abjad.OrderedDict()
        found_score = False
        with open(self) as pointer:
            for line in pointer.readlines():
                if (
                    line.startswith(r"\score")
                    or line.startswith(r"\context Score")
                    or line.startswith("{")
                ):
                    found_score = True
                if not found_score:
                    preamble_lines.append(line)
                elif " %*% " in line:
                    words = line.split()
                    site = words.index("%*%")
                    name = words[site + 1]
                    # first line in expression:
                    if name not in stack:
                        stack[name] = []
                        stack[name].append(line)
                    # last line in expression
                    else:
                        stack[name].append(line)
                        finished_variables[name] = stack[name]
                        del stack[name]
                        count = len(line) - len(line.lstrip())
                        indent = count * " "
                        dereference = indent + fr"\{name}"
                        first_line = finished_variables[name][0]
                        # these 4 lines can be removed after right-side tags:
                        if "NOT_TOPMOST" in first_line:
                            tag_ = tag.append(abjad.Tag("NOT_TOPMOST"))
                        else:
                            tag_ = tag
                        result = abjad.tag.double_tag([dereference], tag_)
                        dereference = []
                        for tag_line in result[:1]:
                            dereference.append(indent + tag_line)
                        dereference.append(result[-1])
                        dereference = [_ + "\n" for _ in dereference]
                        if bool(stack):
                            items = list(stack.items())
                            items[-1][-1].extend(dereference)
                        else:
                            score_lines.extend(dereference)
                elif bool(stack):
                    items = list(stack.items())
                    items[-1][-1].append(line)
                else:
                    score_lines.append(line)
        lines = []
        if include_path.parent == self.parent:
            include_name = include_path.name
        else:
            include_name = str(include_path)
        include_line = f'\\include "{include_name}"'
        include_lines = abjad.tag.double_tag([include_line], tag)
        include_lines = [_ + "\n" for _ in include_lines]
        last_include = 0
        for i, line in enumerate(preamble_lines):
            if line.startswith(r"\include"):
                last_include = i
        preamble_lines[last_include + 1 : last_include + 1] = include_lines
        if preamble_lines[-2] == "\n":
            del preamble_lines[-2]
        lines.extend(preamble_lines)
        lines.extend(score_lines)
        lines_ = []
        for line in lines:
            lines_.append(line)
        text = "".join(lines_)
        score_path.write_text(text)
        lines = []
        items = list(finished_variables.items())
        total = len(items)
        for i, item in enumerate(items):
            name, variable_lines = item
            first_line = variable_lines[0]
            count = len(first_line) - len(first_line.lstrip())
            first_line = first_line[count:]
            first_line = f"{name} = {first_line}"
            words = first_line.split()
            site = words.index("%*%")
            first_line = " ".join(words[:site])
            first_lines = abjad.tag.double_tag([first_line], tag)
            first_lines = [_ + "\n" for _ in first_lines]
            lines.extend(first_lines)
            for variable_line in variable_lines[1:]:
                assert variable_line[:count].isspace(), repr(line)
                variable_line = variable_line[count:]
                if variable_line == "":
                    variable_line = "\n"
                assert variable_line.endswith("\n"), repr(variable_line)
                lines.append(variable_line)
            not_topmost_index = None
            for j, line in enumerate(reversed(lines)):
                if line == "%! NOT_TOPMOST\n":
                    not_topmost_index = j
                    break
                if line.isspace():
                    break
            if not_topmost_index is not None:
                assert 0 < not_topmost_index
                index = -(not_topmost_index + 1)
                del lines[index]
            last_line = lines[-1]
            assert last_line.startswith("} ") or last_line.startswith(">> ")
            words = last_line.split()
            site = words.index("%*%")
            last_line = " ".join(words[:site])
            last_lines = abjad.tag.double_tag([last_line], tag)
            last_lines = [_ + "\n" for _ in last_lines]
            lines[-1:] = last_lines
            if i < total - 1:
                lines.append("\n")
                lines.append("\n")
        text = "".join(lines)
        include_path.write_text(text)

    def get_asset_type(self):
        """
        Gets asset identifier.
        """
        if self.is_scores():
            return "package"
        elif self.is_wrapper():
            return "asset"
        elif self.is_contents():
            return "directory"
        elif self.is_segments():
            return "package"
        elif self.is_builds():
            return "directory"
        else:
            return "asset"

    def get_files_ending_with(self, name):
        """
        Gets files in path ending with ``name``.
        """
        paths = []
        for path in self.list_paths():
            if path.name.endswith(name):
                paths.append(path)
        return paths

    def get_identifier(self):
        """
        Gets identifier.

        Returns title when path is contents directory.

        Returns name metadatum when name metadatum exists.

        Returns path name otherwise.
        """
        if self.is_wrapper():
            result = self.contents.get_title()
        elif self.is_contents():
            result = self.get_title()
        elif self.is_dir():
            result = self.get_metadatum("name", self.name)
        else:
            result = self.name
        return abjad.String(result)

    def get_metadata(self, file_name="__metadata__"):
        """
        Gets metadata.
        """
        assert file_name in ("__metadata__", "__persist__"), repr(file_name)
        metadata_py_path = self / file_name
        metadata = None
        if metadata_py_path.is_file():
            file_contents_string = metadata_py_path.read_text()
            import baca

            namespace = {"abjad": abjad, "baca": baca}
            metadata = eval(file_contents_string, namespace)
        return abjad.OrderedDict(metadata)

    def get_metadatum(
        self,
        metadatum_name,
        default=None,
        *,
        file_name="__metadata__",
    ):
        """
        Gets metadatum.
        """
        metadata = self.get_metadata(file_name=file_name)
        metadatum = metadata.get(metadatum_name)
        if not metadatum:
            metadatum = default
        return metadatum

    def get_next_package(self, cyclic=False):
        """
        Gets next package.
        """
        paths = list(sorted(self.parent.glob("*")))
        paths = [_ for _ in paths if _.name[0].isalnum()]
        assert self in paths, repr((self, paths))
        index = paths.index(self)
        if index == len(paths) - 1 and not cyclic:
            return None
        path = abjad.CyclicTuple(paths)[index + 1]
        return path

    def get_next_score(self, cyclic=False):
        """
        Gets next score.
        """
        if not self.is_dir():
            return None
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[0]
        if self.scores is not None:
            wrappers = self.scores.list_paths()
        else:
            wrappers = []
        if not wrappers:
            return None
        wrapper = self.wrapper
        if wrapper == wrappers[-1] and not cyclic:
            return None
        assert isinstance(wrapper, Path)
        index = wrappers.index(wrapper)
        cyclic_wrappers = abjad.CyclicTuple(wrappers)
        return cyclic_wrappers[index + 1]

    def get_previous_package(self, cyclic=False):
        """
        Gets previous package.
        """
        assert self.is_dir()
        paths = list(sorted(self.parent.glob("*")))
        paths = [_ for _ in paths if _.name[0].isalnum()]
        assert self in paths, repr((self, paths))
        index = paths.index(self)
        if index == 0 and not cyclic:
            return None
        path = abjad.CyclicTuple(paths)[index - 1]
        return path

    def get_previous_score(self, cyclic=False):
        """
        Gets previous score.
        """
        if not self.is_dir():
            return None
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[-1]
        if self.scores is not None:
            wrappers = self.scores.list_paths()
        else:
            wrappers = []
        if not wrappers:
            return None
        wrapper = self.wrapper
        if wrapper == wrappers[0] and not cyclic:
            return None
        assert wrapper is not None
        index = wrappers.index(wrapper)
        cyclic_wrappers = abjad.CyclicTuple(wrappers)
        return cyclic_wrappers[index - 1]

    def get_title(self, year=True):
        """
        Gets score title.
        """
        if year and self.get_metadatum("year"):
            title = self.get_title(year=False)
            year = self.get_metadatum("year")
            result = f"{title} ({year})"
            return result
        else:
            result = self.get_metadatum("title")
            result = result or self.name
            return result

    def is__assets(self):
        """
        Is true when path is _assets directory.
        """
        return self.name == "_assets"

    def is__segments(self):
        """
        Is true when path is _segments directory.
        """
        return self.name == "_segments"

    def is_build(self):
        """
        Is true when path is build directory.
        """
        if self.name in ("_assets", "_segments"):
            return False
        if self.parent.name == "builds":
            return True
        if self.parent.parent.name == "builds" and self.suffix == "":
            return True
        return False

    def is_builds(self):
        """
        Is true when path is builds directory.
        """
        return self.name == "builds"

    def is_buildspace(self):
        """
        Is true when path is buildspace.

            * build
            * builds
            * segment
            * segments
            * _segments

        """
        if self.is_build() or self.is_builds():
            return True
        if self.is__segments() or self.is_segment() or self.is_segments():
            return True
        return False

    def is_contents(self):
        """
        Is true when path is contents directory.
        """
        if self.scores is not None:
            return self.scores / self.name / self.name == self
        else:
            return False

    def is_definitionspace(self):
        """
        Is true when path is any of segment or segments directories.
        """
        if self.is_segment():
            return True
        if self.is_segments():
            return True
        return False

    def is_distribution(self):
        """
        Is true when path is distribution directory.
        """
        return self.name == "distribution"

    def is_etc(self):
        """
        Is true when path is etc directory.
        """
        return self.name == "etc"

    def is_external(self):
        """
        Is true when path is not a score package path.
        """
        if str(self).startswith(str(self.scores)):
            return False
        return True

    def is_part(self):
        """
        Is true when directory is part directory.
        """
        return self.parent.is_parts()

    def is_parts(self):
        """
        Is true when directory is parts directory.
        """
        if self.is_build():
            if self.name.endswith("-parts"):
                return True
            else:
                return self.get_metadatum("parts_directory") is True
        else:
            return False

    def is_score_build(self):
        """
        Is true when directory is score build directory.
        """
        if self.is_build():
            if "-part" in str(self):
                return False
            if self.get_metadatum("parts_directory") is True:
                return False
            if self.parent.get_metadatum("parts_directory") is True:
                return False
            return True
        else:
            return False

    def is_scores(self):
        """
        Is true when path is scores directory.
        """
        return self == self.scores

    def is_segment(self):
        """
        Is true when path is segment directory.
        """
        if self.name[0] == ".":
            return False
        return self.parent.name == "segments" and self.parent.parent.name != "abjad"

    def is_segments(self):
        """
        Is true when path is segments directory.

        """
        return self.name == "segments" and self.parent.name != "abjad"

    def is_wrapper(self):
        """
        Is true when path is wrapper directory
        """
        if self.scores is not None:
            return self.scores / self.name == self
        else:
            return False

    def list_paths(self):
        """
        Lists paths.
        """
        paths = []
        if not self.exists():
            return paths
        is_external = self.is_external()
        is_segments = self.is_segments()
        names = []
        for name in sorted([_.name for _ in self.iterdir()]):
            name = abjad.String(name)
            if name.startswith("_") and not (is_external or is_segments):
                continue
            if name in (".DS_Store", ".cache", ".git", ".gitmodules"):
                continue
            if name in ("__init__.py", "__pycache__"):
                continue
            elif name in self._secondary_names:
                continue
            path = self / name
            try:
                path.relative_to(self)
            except ValueError:
                continue
            names.append(name)
        if is_segments:
            names = [_ for _ in names if not _.endswith("backup")]
            names = [_ for _ in names if not _.startswith(".")]
            names = Path.sort_segment_names(names)
        if self.is__segments():
            prefix = "segment-"
            names = [_ for _ in names if _.startswith(prefix)]
            single_character_names, double_character_names = [], []
            for name in names:
                segment_name = name[len(prefix) :]
                segment_name = segment_name.replace("-", "_")
                if segment_name.endswith(".ly"):
                    segment_name = segment_name[:-3]
                elif segment_name.endswith(".ily"):
                    segment_name = segment_name[:-4]
                else:
                    raise ValueError(segment_name)
                if len(segment_name) == 1:
                    single_character_names.append(name)
                elif len(segment_name) == 2:
                    double_character_names.append(name)
                else:
                    raise NotImplementedError(segment_name)
            names = single_character_names + double_character_names
        paths = [self / _ for _ in names]
        return paths

    def list_secondary_paths(self):
        """
        Lists secondary paths.
        """
        paths = []
        for path in sorted(self.glob("*")):
            if path.name in sorted(self._secondary_names):
                paths.append(type(self)(path))
        return paths

    def remove(self):
        """
        Removes path if it exists.
        """
        if self.is_file():
            self.unlink()
        elif self.is_dir():
            shutil.rmtree(str(self))

    def remove_metadatum(self, name, *, file_name="__metadata__"):
        """
        Removes metadatum.
        """
        assert " " not in name, repr(name)
        metadata = self.get_metadata(file_name=file_name)
        try:
            metadata.pop(name)
        except KeyError:
            pass
        self.write_metadata_py(metadata, file_name=file_name)

    @staticmethod
    def sort_segment_names(strings):
        """
        Sorts segment name ``strings``.

        ..  container:: example

            >>> strings = ['AA', 'Z', '_11', '_9']
            >>> baca.Path.sort_segment_names(strings)
            ['_9', '_11', 'Z', 'AA']

        """
        names = []
        for string in strings:
            name = abjad.String(string)
            names.append(name)

        def _compare(name_1, name_2):
            letter_1 = name_1.segment_letter()
            letter_2 = name_2.segment_letter()
            rank_1 = name_1.segment_rank()
            rank_2 = name_2.segment_rank()
            if letter_1 == letter_2:
                if rank_1 < rank_2:
                    return -1
                if rank_1 == rank_2:
                    return 0
                if rank_1 > rank_2:
                    return 1
            if letter_1 == "_":
                return -1
            if letter_2 == "_":
                return 1
            if len(letter_1) == len(letter_2):
                if letter_1 < letter_2:
                    return -1
                if letter_2 < letter_1:
                    return 1
            if len(letter_1) < len(letter_2):
                return -1
            assert len(letter_2) < len(letter_1)
            return 1

        names_ = abjad.TypedList(names)
        names_.sort(cmp=_compare)
        return list(names_)

    def trim(self):
        """
        Trims path.
        """
        if self.is_external():
            return str(self)
        assert self.scores is not None, repr(self)
        count = len(self.scores.parts) + 1
        parts = self.parts
        parts = parts[count:]
        path = pathlib.Path(*parts)
        if str(path) == ".":
            return str(self)
        return str(path)

    def with_name(self, name):
        """
        Gets path with ``name``.
        """
        return self.parent / name

    def write_metadata_py(
        self,
        metadata,
        *,
        file_name="__metadata__",
        variable_name="metadata",
    ):
        """
        Writes ``metadata`` to metadata file in current directory.
        """
        metadata_py_path = self / file_name
        lines = []
        dictionary = abjad.OrderedDict(metadata)
        items = list(dictionary.items())
        items.sort()
        dictionary = abjad.OrderedDict(items)
        if dictionary:
            line = abjad.storage(dictionary)
            lines.append(line)
        else:
            lines.append("abjad.OrderedDict()")
        lines.append("")
        text = "\n".join(lines)
        metadata_py_path.write_text(text)
        os.system(f"black --target-version=py38 {metadata_py_path} > /dev/null 2>&1")


def get_measure_profile_metadata(path) -> typing.Tuple[int, int, list]:
    """
    Gets measure profile metadata.

    Reads segment metadata when path is segment.

    Reads score metadata when path is not segment.

    Returns tuple of three metadata: first measure number; measure count;
    list of fermata measure numbers.
    """
    if path.parent.is_segment():
        string = "first_measure_number"
        first_measure_number = path.parent.get_metadatum(string)
        time_signatures = path.parent.get_metadatum("time_signatures")
        if bool(time_signatures):
            measure_count = len(time_signatures)
        else:
            measure_count = 0
        string = "fermata_measure_numbers"
        fermata_measure_numbers = path.parent.get_metadatum(string)
    else:
        first_measure_number = 1
        dictionary = path.contents.get_metadatum("time_signatures")
        dictionary = dictionary or abjad.OrderedDict()
        measure_count = 0
        for segment, time_signatures in dictionary.items():
            measure_count += len(time_signatures)
        string = "fermata_measure_numbers"
        dictionary = path.contents.get_metadatum(string)
        dictionary = dictionary or abjad.OrderedDict()
        fermata_measure_numbers = []
        for segment, fermata_measure_numbers_ in dictionary.items():
            fermata_measure_numbers.extend(fermata_measure_numbers_)
    return (first_measure_number, measure_count, fermata_measure_numbers)

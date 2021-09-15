"""
Templates.
"""
import typing

import abjad

from . import const as _const
from . import tags as _tags


def assert_lilypond_identifiers(score):
    for context in abjad.iterate(score).components(abjad.Context):
        if not abjad.String(context.name).is_lilypond_identifier():
            raise Exception(f"invalid LilyPond identifier: {context.name!r}")


def assert_matching_custom_context_names(score):
    for context in abjad.iterate(score).components(abjad.Context):
        if context.lilypond_type in abjad.Context.lilypond_types:
            continue
        if context.name == context.lilypond_type:
            continue
        if context.name.replace("_", "") == context.lilypond_type:
            continue
        message = f"context {context.lilypond_type}"
        message += f" has name {context.name!r}."
        raise Exception(message)


def assert_unique_context_names(score):
    names = []
    for context in abjad.iterate(score).components(abjad.Context):
        if context.name in names:
            raise Exception(f"duplicate context name: {context.name!r}.")


def make_global_context():
    site = "abjad.ScoreTemplate._make_global_context()"
    tag = abjad.Tag(site)
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


class ScoreTemplate:
    """
    Score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_voice_abbreviations",)

    _always_make_global_rests = False

    _do_not_require_margin_markup = False

    _part_manifest = None

    voice_colors: dict = {}

    ### INITIALIZER ###

    def __init__(self):
        self._voice_abbreviations = abjad.OrderedDict()

    ### PRIVATE METHODS ###

    def _attach_lilypond_tag(self, tag, context):
        for tag_ in tag.split("."):
            if not abjad.String(tag_).is_lilypond_identifier():
                raise Exception(f"invalid LilyPond identifier: {tag_!r}.")
            part_names = []
            if self.part_manifest is not None:
                part_names = [_.name for _ in self.part_manifest.parts]
            if part_names and tag_ not in part_names:
                raise Exception(f"not listed in parts manifest: {tag_!r}.")
        literal = abjad.LilyPondLiteral(fr"\tag {tag}", "before")
        site = "baca.ScoreTemplate._attach_liypond_tag()"
        tag = abjad.Tag(site)
        abjad.attach(literal, context, tag=tag)

    def _validate_voice_names(self, score):
        voice_names = []
        for voice in abjad.iterate(score).components(abjad.Voice):
            voice_names.append(voice.name)
        for voice_name in sorted(self.voice_colors):
            if voice_name not in voice_names:
                raise Exception(f"voice not in score: {voice_name!r}.")

    ### PUBLIC PROPERTIES ###

    @property
    def always_make_global_rests(self):
        """
        Is true when score template always makes global rests.
        """
        return self._always_make_global_rests

    @property
    def do_not_require_margin_markup(self):
        """
        Is true when score template does not require margin markup.

        Conventionally, solos do not require margin markup.
        """
        return self._do_not_require_margin_markup

    @property
    def part_manifest(self):
        """
        Gets part manifest.
        """
        return self._part_manifest

    @property
    def voice_abbreviations(self):
        """
        Gets voice abbreviations.
        """
        return self._voice_abbreviations

    ### PUBLIC METHODS ###

    # TODO: implement only on classes that need it
    def allows_instrument(self, staff_name, instrument):
        """
        Is true when ``staff_name`` allows ``instrument``.

        To be implemented by concrete score template classes.
        """
        return True

    def group_families(self, *families) -> typing.List[abjad.Context]:
        """
        Groups ``families`` only when more than one family is passed in.
        """
        families_ = []
        for family in families:
            if family is not None:
                assert isinstance(family, tuple), repr(family)
                if any(_ for _ in family[1:] if _ is not None):
                    families_.append(family)
        families = tuple(families_)
        contexts = []
        if len(families) == 0:
            pass
        elif len(families) == 1:
            family = families[0]
            contexts.extend([_ for _ in family[1:] if _ is not None])
        else:
            for family in families:
                if not isinstance(family, tuple):
                    assert isinstance(family, abjad.Context)
                    contexts.append(family)
                    continue
                square_staff_group = self.make_square_staff_group(*family)
                assert square_staff_group is not None
                contexts.append(square_staff_group)
        return contexts

    def make_music_context(self, *contexts) -> abjad.Context:
        """
        Makes music context.
        """
        contexts = tuple(_ for _ in contexts if _ is not None)
        site = "baca.ScoreTemplate.make_music_context()"
        tag = abjad.Tag(site)
        return abjad.Context(
            contexts,
            lilypond_type="MusicContext",
            simultaneous=True,
            name="Music_Context",
            tag=tag,
        )

    def make_piano_staff(
        self, stem: str, *contexts
    ) -> typing.Optional[abjad.StaffGroup]:
        """
        Makes piano staff.
        """
        if not isinstance(stem, str):
            raise Exception(f"stem must be string: {stem!r}.")
        contexts = tuple(_ for _ in contexts if _ is not None)
        if contexts:
            return abjad.StaffGroup(contexts, name=f"{stem}_Piano_Staff")
        else:
            return None

    def make_square_staff_group(
        self, stem: str, *contexts
    ) -> typing.Optional[typing.Union[abjad.Staff, abjad.StaffGroup]]:
        """
        Makes square staff group.
        """
        if not isinstance(stem, str):
            raise Exception(f"stem must be string: {stem!r}.")
        site = "baca.ScoreTemplate.make_square_staff_group()"
        tag = abjad.Tag(site)
        contexts = tuple(_ for _ in contexts if _ is not None)
        result = None
        if len(contexts) == 1:
            prototype = (abjad.Staff, abjad.StaffGroup)
            assert isinstance(contexts[0], prototype), repr(contexts[0])
            result = contexts[0]
        elif 1 < len(contexts):
            name = f"{stem}_Square_Staff_Group"
            staff_group = abjad.StaffGroup(contexts, name=name, tag=tag)
            abjad.setting(staff_group).system_start_delimiter = "#'SystemStartSquare"
            result = staff_group
        return result

    def make_staff_group(
        self, stem: str, *contexts
    ) -> typing.Optional[abjad.StaffGroup]:
        """
        Makes staff group.
        """
        if not isinstance(stem, str):
            raise Exception(f"stem must be string: {stem!r}.")
        site = "baca.ScoreTemplate.make_staff_group()"
        tag = abjad.Tag(site)
        contexts = tuple(_ for _ in contexts if _ is not None)
        if contexts:
            return abjad.StaffGroup(contexts, name=f"{stem}_Staff_Group", tag=tag)
        else:
            return None


def attach_defaults(argument):
    """
    Attaches defaults to all staff and staff group contexts in ``argument`` when
    ``argument`` is a score.

    Attaches defaults to ``argument`` (without iterating ``argument``) when ``argument``
    is a staff or staff group.

    Returns list of one wrapper for every indicator attached.
    """
    prototype = (abjad.Score, abjad.Staff, abjad.StaffGroup)
    assert isinstance(argument, prototype), repr(argument)
    wrappers = []
    tag = _const.REMOVE_ALL_EMPTY_STAVES
    empty_prototype = (abjad.MultimeasureRest, abjad.Skip)
    prototype = (abjad.Staff, abjad.StaffGroup)
    if isinstance(argument, abjad.Score):
        staff__groups = list(abjad.Selection(argument).components(prototype))
        staves = list(abjad.Selection(argument).components(abjad.Staff))
    elif isinstance(argument, abjad.Staff):
        staff__groups = [argument]
        staves = [argument]
    else:
        assert isinstance(argument, abjad.StaffGroup), repr(argument)
        staff__groups = [argument]
        staves = []
    for staff__group in staff__groups:
        leaf = None
        voices = abjad.Selection(staff__group).components(abjad.Voice)
        assert isinstance(voices, abjad.Selection), repr(voices)
        # find leaf 0 in first nonempty voice
        for voice in voices:
            leaves = []
            for leaf_ in abjad.Iteration(voice).leaves():
                if abjad.get.has_indicator(leaf_, _const.HIDDEN):
                    leaves.append(leaf_)
            if not all(isinstance(_, empty_prototype) for _ in leaves):
                leaf = abjad.get.leaf(voice, 0)
                break
        # otherwise, find first leaf in voice in non-removable staff
        if leaf is None:
            for voice in voices:
                voice_might_vanish = False
                for component in abjad.get.parentage(voice):
                    if abjad.get.annotation(component, tag) is True:
                        voice_might_vanish = True
                if not voice_might_vanish:
                    leaf = abjad.get.leaf(voice, 0)
                    if leaf is not None:
                        break
        # otherwise, as last resort find first leaf in first voice
        if leaf is None:
            leaf = abjad.get.leaf(voices[0], 0)
        if leaf is None:
            continue
        instrument = abjad.get.indicator(leaf, abjad.Instrument)
        if instrument is None:
            string = "default_instrument"
            instrument = abjad.get.annotation(staff__group, string)
            if instrument is not None:
                wrapper = abjad.attach(
                    instrument,
                    leaf,
                    context=staff__group.lilypond_type,
                    tag=abjad.Tag("abjad.ScoreTemplate.attach_defaults(1)"),
                    wrapper=True,
                )
                wrappers.append(wrapper)
        margin_markup = abjad.get.indicator(leaf, abjad.MarginMarkup)
        if margin_markup is None:
            string = "default_margin_markup"
            margin_markup = abjad.get.annotation(staff__group, string)
            if margin_markup is not None:
                wrapper = abjad.attach(
                    margin_markup,
                    leaf,
                    tag=_tags.NOT_PARTS.append(
                        abjad.Tag("abjad.ScoreTemplate.attach_defaults(2)")
                    ),
                    wrapper=True,
                )
                wrappers.append(wrapper)
    for staff in staves:
        leaf = abjad.get.leaf(staff, 0)
        clef = abjad.get.indicator(leaf, abjad.Clef)
        if clef is not None:
            continue
        clef = abjad.get.annotation(staff, "default_clef")
        if clef is not None:
            wrapper = abjad.attach(
                clef,
                leaf,
                tag=abjad.Tag("abjad.ScoreTemplate.attach_defaults(3)"),
                wrapper=True,
            )
            wrappers.append(wrapper)
    return wrappers


def make_empty_score(*counts):
    r"""
    Makes empty score for doc examples.

    ..  container:: example

        >>> score = baca.make_empty_score(1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            {
                \context Staff = "Music_Staff"
                {
                    \context Voice = "Music_Voice"
                    {
                    }
                }
            }
        >>

    ..  container:: example

        >>> score = baca.make_empty_score(4)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Music_Voice_1"
                    {
                    }
                    \context Voice = "Music_Voice_2"
                    {
                    }
                    \context Voice = "Music_Voice_3"
                    {
                    }
                    \context Voice = "Music_Voice_4"
                    {
                    }
                >>
            }
        >>

    ..  container:: example

        >>> score = baca.make_empty_score(1, 1, 1, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            <<
                \context StaffGroup = "Music_Staff_Group"
                <<
                    \context Staff = "Music_Staff_1"
                    {
                        \context Voice = "Music_Voice_1"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_2"
                    {
                        \context Voice = "Music_Voice_2"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_3"
                    {
                        \context Voice = "Music_Voice_3"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_4"
                    {
                        \context Voice = "Music_Voice_4"
                        {
                        }
                    }
                >>
            >>
        >>

    ..  container:: example

        >>> score = baca.make_empty_score(1, 2, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            <<
                \context StaffGroup = "Music_Staff_Group"
                <<
                    \context Staff = "Music_Staff_1"
                    {
                        \context Voice = "Music_Voice_1"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_2"
                    <<
                        \context Voice = "Music_Voice_2"
                        {
                        }
                        \context Voice = "Music_Voice_3"
                        {
                        }
                    >>
                    \context Staff = "Music_Staff_3"
                    {
                        \context Voice = "Music_Voice_4"
                        {
                        }
                    }
                >>
            >>
        >>

    """

    site = "baca.make_configuration_empty_score()"
    tag = abjad.Tag(site)
    global_context = make_global_context()
    single_staff = len(counts) == 1
    single_voice = single_staff and counts[0] == 1
    staves, voice_number = [], 1
    for staff_index, voice_count in enumerate(counts):
        if single_staff:
            name = "Music_Staff"
        else:
            staff_number = staff_index + 1
            name = f"Music_Staff_{staff_number}"
        simultaneous = 1 < voice_count
        staff = abjad.Staff(name=name, simultaneous=simultaneous, tag=tag)
        voices = []
        for voice_index in range(voice_count):
            if single_voice:
                name = "Music_Voice"
            else:
                name = f"Music_Voice_{voice_number}"
            voice = abjad.Voice(name=name, tag=tag)
            voices.append(voice)
            voice_number += 1
        staff.extend(voices)
        staves.append(staff)

    if len(staves) == 1:
        music = staves
        simultaneous = False
    else:
        music = [abjad.StaffGroup(staves, name="Music_Staff_Group")]
        simultaneous = True

    music_context = abjad.Context(
        music,
        lilypond_type="MusicContext",
        simultaneous=simultaneous,
        name="Music_Context",
        tag=tag,
    )

    score = abjad.Score([global_context, music_context], name="Score", tag=tag)
    return score


def make_empty_score_maker(*counts):
    """
    Makes empty score maker.
    """

    def closure():
        return make_empty_score(*counts)

    return closure

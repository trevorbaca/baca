import abjad
import roman # type: ignore
import typing


class ScoreTemplate(abjad.ScoreTemplate):
    r'''Score template
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_defaults',
        )

    voice_colors: dict = {
        }

    ### INITIALIZER ###

    def __init__(self) -> None:
        super(ScoreTemplate, self).__init__()
        self._defaults: list = []

    ### PRIVATE METHODS ###

    @staticmethod
    def _assert_lilypond_identifiers(score):
        for context in abjad.iterate(score).components(abjad.Context):
            if not abjad.String(context.name).is_lilypond_identifier():
                message = f'invalid LilyPond identifier: {context.name!r}'
                raise Exception(message)
        
    @staticmethod
    def _assert_matching_custom_context_names(score):
        for context in abjad.iterate(score).components(abjad.Context):
            if context.lilypond_type in abjad.Context.lilypond_types:
                continue
            if context.name != context.lilypond_type:
                message = f'context {context.lilypond_type}'
                message += f' has name {context.name!r}.'
                raise Exception(message)

    @staticmethod
    def _assert_unique_context_names(score):
        names = []
        for context in abjad.iterate(score).components(abjad.Context):
            if context.name in names:
                raise Exception(f'duplicate context name: {context.name!r}.')

    def _attach_calltime_defaults(self, score):
        assert isinstance(score, abjad.Score)
        for lilypond_type, annotation, indicator in self.defaults:
            context = score[lilypond_type]
            abjad.annotate(context, annotation, indicator)
        
    def _attach_lilypond_tag(self, tag, context):
        for tag_ in tag.split('.'):
            if not abjad.String(tag_).is_lilypond_identifier():
                raise Exception(f'invalid LilyPond identifier: {tag_!r}.')
            part_names = [_.name for _ in self.part_manifest.parts]
            if part_names and tag_ not in part_names:
                raise Exception(f'not listed in parts manifest: {tag_!r}.')
        literal = abjad.LilyPondLiteral(fr'\tag {tag}', 'before')
        abjad.attach(literal, context, tag='ST4')

    @staticmethod
    def _set_square_delimiter(staff_group):
        abjad.setting(staff_group).system_start_delimiter = 'SystemStartSquare'

    @staticmethod
    def _to_roman(n):
        return roman.toRoman(n)

    def _validate_voice_names(self, score):
        voice_names = []
        for voice in abjad.iterate(score).components(abjad.Voice):
            voice_names.append(voice.name)
        for voice_name in sorted(self.voice_colors):
            if voice_name not in voice_names:
                raise Exception(f'voice not in score: {voice_name!r}.')

    ### PUBLIC PROPERTIES ###

    @property
    def defaults(self) -> list:
        r'''Gets defaults.
        '''
        return self._defaults

    ### PUBLIC METHODS ###

    def group_families(self, *families) -> typing.List[abjad.Context]:
        r'''Groups `families` only when more than one family is passed in.

        Returns list of zero or more contexts.
        '''
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
        r'''Makes music context.
        '''
        contexts = tuple(_ for _ in contexts if _ is not None)
        return abjad.Context(
            contexts,
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )

    def make_piano_staff(
        self,
        stem: str,
        *contexts,
        ) -> abjad.StaffGroup:
        r'''Makes piano staff.
        '''
        if not isinstance(stem, str):
            raise Exception(f'stem must be string: {stem!r}.')
        contexts = tuple(_ for _ in contexts if _ is not None)
        if contexts:
            return abjad.StaffGroup(contexts, name=f'{stem}PianoStaff')
        else:
            return None

    def make_square_staff_group(
        self,
        stem: str,
        *contexts,
        ) -> abjad.StaffGroup:
        r'''Makes square staff group.
        '''
        if not isinstance(stem, str):
            raise Exception(f'stem must be string: {stem!r}.')
        contexts = tuple(_ for _ in contexts if _ is not None)
        result = None
        if len(contexts) == 1:
            result = contexts[0]
        elif 1 < len(contexts):
            name = f'{stem}SquareStaffGroup'
            staff_group = abjad.StaffGroup(contexts, name=name)
            self._set_square_delimiter(staff_group)
            result = staff_group
        return result

    def make_staff_group(
        self,
        stem: str,
        *contexts,
        ) -> abjad.StaffGroup:
        r'''Makes staff group.
        '''
        if not isinstance(stem, str):
            raise Exception(f'stem must be string: {stem!r}.')
        contexts = tuple(_ for _ in contexts if _ is not None)
        if contexts:
            return abjad.StaffGroup(contexts, name=f'{stem}StaffGroup')
        else:
            return None

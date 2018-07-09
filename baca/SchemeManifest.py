import abjad


class SchemeManifest(abjad.AbjadObject):
    """
    Scheme manifest.

    New functions defined in ``~/baca/baca/lilypond/baca.ily`` must
    currently be added here by hand.

    TODO: eliminate duplication. Define custom Scheme functions here
    (``SchemeManifest``) and teach ``SchemeManifest`` to write
    ``~/baca/baca/lilypond/baca.ily`` automatically.
    """

    ### CLASS VARIABLES ###

    _dynamics = (
        ('baca_appena_udibile', 'appena udibile'),
        ('baca_f_but_accents_sffz', 'f'),
        ('baca_f_sub_but_accents_continue_sffz', 'f'),
        ('baca_ffp', 'p'),
        ('baca_fffp', 'p'),
        ('niente', 'niente'),
        ('baca_p_sub_but_accents_continue_sffz', 'p'),
        ('baca_sff', 'ff'),
        ('baca_sffp', 'p'),
        ('baca_sffpp', 'pp'),
        ('baca_sfffz', 'fff'),
        ('baca_sffz', 'ff'),
        ('baca_sfpp', 'pp'),
        ('baca_sfz_f', 'f'),
        ('baca_sfz_p', 'p'),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def dynamics(self):
        """
        Gets dynamics.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> for dynamic in scheme_manifest.dynamics:
            ...     dynamic
            ...
            'baca_appena_udibile'
            'baca_f_but_accents_sffz'
            'baca_f_sub_but_accents_continue_sffz'
            'baca_ffp'
            'baca_fffp'
            'niente'
            'baca_p_sub_but_accents_continue_sffz'
            'baca_sff'
            'baca_sffp'
            'baca_sffpp'
            'baca_sfffz'
            'baca_sffz'
            'baca_sfpp'
            'baca_sfz_f'
            'baca_sfz_p'

        Returns list.
        """
        return [_[0] for _ in self._dynamics]

    ### PUBLIC METHODS ###

    def dynamic_to_steady_state(self, dynamic):
        """
        Changes ``dynamic`` to steady state.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> scheme_manifest.dynamic_to_steady_state('sfz_p')
            'p'

        Returns string.
        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
            if dynamic_ == 'baca_' + dynamic:
                return steady_state
        raise KeyError(dynamic)

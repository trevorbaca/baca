import abjad


class SchemeManifest(abjad.AbjadObject):
    r"""Scheme manifest.

    New functions defined in ``~/baca/baca/stylesheets/scheme.ily`` must
    currently be added here by hand.

    TODO: eliminate duplication. Define ALL custom Scheme functions here
    (``SchemeManifest``) and teach ``SchemeManifest`` to write
    ``~/baca/baca/stylesheets/scheme.ily`` to disk automatically.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    _dynamics = (
        ('appena_udibile', 'appena udibile'),
        ('f_but_accents_sffz', 'f'),
        ('f_sub_but_accents_continue_sffz', 'f'),
        ('p_sub_but_accents_continue_sffz', 'p'),
        ('sfz_f', 'f'),
        ('sfz_p', 'p'),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def dynamics(self):
        r"""Gets dynamics.

        ..  container:: example

            >>> for dynamic in baca.scheme.dynamics:
            ...     dynamic
            ...
            'appena_udibile'
            'f_but_accents_sffz'
            'f_sub_but_accents_continue_sffz'
            'p_sub_but_accents_continue_sffz'
            'sfz_f'
            'sfz_p'

        Returns list.
        """
        return [_[0] for _ in self._dynamics]

    ### PUBLIC METHODS ###

    def dynamic_to_steady_state(self, dynamic):
        r"""Changes `dynamic` to steady state.

        ..  container:: example

            >>> baca.scheme.dynamic_to_steady_state('sfz_p')
            'p'

        Returns string.
        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
        raise KeyError(dynamic)

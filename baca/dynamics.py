import abjad


class SchemeManifest:
    """
    Scheme manifest.

    New functions defined in ``~/baca/lilypond/baca.ily`` must be added here.
    """

    _dynamics = (
        ("baca-appena-udibile", "appena udibile"),
        ("baca-f-but-accents-sffz", "f"),
        ("baca-f-sub-but-accents-continue-sffz", "f"),
        ("baca-ffp", "p"),
        ("baca-fffp", "p"),
        ("niente", "niente"),
        ("baca-p-sub-but-accents-continue-sffz", "p"),
        #
        ("baca-pppf", "f"),
        ("baca-pppff", "ff"),
        ("baca-pppfff", "fff"),
        #
        ("baca-ppf", "f"),
        ("baca-ppff", "ff"),
        ("baca-ppfff", "fff"),
        #
        ("baca-pf", "f"),
        ("baca-pff", "ff"),
        ("baca-pfff", "fff"),
        #
        ("baca-ppp-ppp", "ppp"),
        ("baca-ppp-pp", "pp"),
        ("baca-ppp-p", "p"),
        ("baca-ppp-mp", "mp"),
        ("baca-ppp-mf", "mf"),
        ("baca-ppp-f", "f"),
        ("baca-ppp-ff", "ff"),
        ("baca-ppp-fff", "fff"),
        #
        ("baca-pp-ppp", "ppp"),
        ("baca-pp-pp", "pp"),
        ("baca-pp-p", "p"),
        ("baca-pp-mp", "mp"),
        ("baca-pp-mf", "mf"),
        ("baca-pp-f", "f"),
        ("baca-pp-ff", "ff"),
        ("baca-pp-fff", "fff"),
        #
        ("baca-p-ppp", "ppp"),
        ("baca-p-pp", "pp"),
        ("baca-p-p", "p"),
        ("baca-p-mp", "mp"),
        ("baca-p-mf", "mf"),
        ("baca-p-f", "f"),
        ("baca-p-ff", "ff"),
        ("baca-p-fff", "fff"),
        #
        ("baca-mp-ppp", "ppp"),
        ("baca-mp-pp", "pp"),
        ("baca-mp-p", "p"),
        ("baca-mp-mp", "mp"),
        ("baca-mp-mf", "mf"),
        ("baca-mp-f", "f"),
        ("baca-mp-ff", "ff"),
        ("baca-mp-fff", "fff"),
        #
        ("baca-mf-ppp", "ppp"),
        ("baca-mf-pp", "pp"),
        ("baca-mf-p", "p"),
        ("baca-mf-mp", "mp"),
        ("baca-mf-mf", "mf"),
        ("baca-mf-f", "f"),
        ("baca-mf-ff", "ff"),
        ("baca-mf-fff", "fff"),
        #
        ("baca-f-ppp", "ppp"),
        ("baca-f-pp", "pp"),
        ("baca-f-p", "p"),
        ("baca-f-mp", "mp"),
        ("baca-f-mf", "mf"),
        ("baca-f-f", "f"),
        ("baca-f-ff", "ff"),
        ("baca-f-fff", "fff"),
        #
        ("baca-ff-ppp", "ppp"),
        ("baca-ff-pp", "pp"),
        ("baca-ff-p", "p"),
        ("baca-ff-mp", "mp"),
        ("baca-ff-mf", "mf"),
        ("baca-ff-f", "f"),
        ("baca-ff-ff", "ff"),
        ("baca-ff-fff", "fff"),
        #
        ("baca-fff-ppp", "ppp"),
        ("baca-fff-pp", "pp"),
        ("baca-fff-p", "p"),
        ("baca-fff-mp", "mp"),
        ("baca-fff-mf", "mf"),
        ("baca-fff-f", "f"),
        ("baca-fff-ff", "ff"),
        ("baca-fff-fff", "fff"),
        #
        ("baca-sff", "ff"),
        ("baca-sffp", "p"),
        ("baca-sffpp", "pp"),
        ("baca-sfffz", "fff"),
        ("baca-sffz", "ff"),
        ("baca-sfpp", "pp"),
        ("baca-sfz-f", "f"),
        ("baca-sfz-p", "p"),
    )

    @property
    def dynamics(self) -> list[str]:
        """
        Gets dynamics.

        ..  container:: example

            >>> scheme_manifest = baca.dynamics.SchemeManifest()
            >>> for dynamic in scheme_manifest.dynamics:
            ...     dynamic
            ...
            'baca-appena-udibile'
            'baca-f-but-accents-sffz'
            'baca-f-sub-but-accents-continue-sffz'
            'baca-ffp'
            'baca-fffp'
            'niente'
            'baca-p-sub-but-accents-continue-sffz'
            'baca-pppf'
            'baca-pppff'
            'baca-pppfff'
            'baca-ppf'
            'baca-ppff'
            'baca-ppfff'
            'baca-pf'
            'baca-pff'
            'baca-pfff'
            'baca-ppp-ppp'
            'baca-ppp-pp'
            'baca-ppp-p'
            'baca-ppp-mp'
            'baca-ppp-mf'
            'baca-ppp-f'
            'baca-ppp-ff'
            'baca-ppp-fff'
            'baca-pp-ppp'
            'baca-pp-pp'
            'baca-pp-p'
            'baca-pp-mp'
            'baca-pp-mf'
            'baca-pp-f'
            'baca-pp-ff'
            'baca-pp-fff'
            'baca-p-ppp'
            'baca-p-pp'
            'baca-p-p'
            'baca-p-mp'
            'baca-p-mf'
            'baca-p-f'
            'baca-p-ff'
            'baca-p-fff'
            'baca-mp-ppp'
            'baca-mp-pp'
            'baca-mp-p'
            'baca-mp-mp'
            'baca-mp-mf'
            'baca-mp-f'
            'baca-mp-ff'
            'baca-mp-fff'
            'baca-mf-ppp'
            'baca-mf-pp'
            'baca-mf-p'
            'baca-mf-mp'
            'baca-mf-mf'
            'baca-mf-f'
            'baca-mf-ff'
            'baca-mf-fff'
            'baca-f-ppp'
            'baca-f-pp'
            'baca-f-p'
            'baca-f-mp'
            'baca-f-mf'
            'baca-f-f'
            'baca-f-ff'
            'baca-f-fff'
            'baca-ff-ppp'
            'baca-ff-pp'
            'baca-ff-p'
            'baca-ff-mp'
            'baca-ff-mf'
            'baca-ff-f'
            'baca-ff-ff'
            'baca-ff-fff'
            'baca-fff-ppp'
            'baca-fff-pp'
            'baca-fff-p'
            'baca-fff-mp'
            'baca-fff-mf'
            'baca-fff-f'
            'baca-fff-ff'
            'baca-fff-fff'
            'baca-sff'
            'baca-sffp'
            'baca-sffpp'
            'baca-sfffz'
            'baca-sffz'
            'baca-sfpp'
            'baca-sfz-f'
            'baca-sfz-p'

        """
        return [_[0] for _ in self._dynamics]

    def dynamic_to_steady_state(self, dynamic) -> str:
        """
        Changes ``dynamic`` to steady state.

        ..  container:: example

            >>> scheme_manifest = baca.dynamics.SchemeManifest()
            >>> scheme_manifest.dynamic_to_steady_state("sfz-p")
            'p'

        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
            if dynamic_ == "baca-" + dynamic:
                return steady_state
        raise KeyError(dynamic)


# TODO: move tests to tests/test_dynamics.py
def make_dynamic(
    string: str, *, forbid_al_niente_to_bar_line: bool = False
) -> abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle:
    r"""
    Makes dynamic.

    ..  container:: example

        >>> baca.dynamics.make_dynamic("p")
        Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("sffz")
        Dynamic(name='ff', command='\\baca-sffz', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=3)

        >>> baca.dynamics.make_dynamic("niente")
        Dynamic(name='niente', command='\\!', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity())

        >>> baca.dynamics.make_dynamic("<")
        StartHairpin(shape='<')

        >>> baca.dynamics.make_dynamic("o<|")
        StartHairpin(shape='o<|')

        >>> baca.dynamics.make_dynamic("appena-udibile")
        Dynamic(name='appena udibile', command='\\baca-appena-udibile', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=None)

    ..  container:: example

        Stop hairpin:

        >>> baca.dynamics.make_dynamic("!")
        StopHairpin(leak=False)

    ..  container:: example

        Ancora dynamics:

        >>> baca.dynamics.make_dynamic("p-ancora")
        Dynamic(name='p', command='\\baca-p-ancora', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-ancora")
        Dynamic(name='f', command='\\baca-f-ancora', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Composite dynamics:

        >>> baca.dynamics.make_dynamic("pf")
        Dynamic(name='f', command='\\baca-pf', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=2)

        >>> baca.dynamics.make_dynamic("pff")
        Dynamic(name='ff', command='\\baca-pff', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=3)

    ..  container:: example

        Effort dynamics:

        >>> baca.dynamics.make_dynamic('"p"')
        Dynamic(name='"p"', command='\\baca-effort-p', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic('"f"')
        Dynamic(name='"f"', command='\\baca-effort-f', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (parenthesized):

        >>> baca.dynamics.make_dynamic('("p")')
        Dynamic(name='p', command='\\baca-effort-p-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic('("f")')
        Dynamic(name='f', command='\\baca-effort-f-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (ancora):

        >>> baca.dynamics.make_dynamic('"p"-ancora')
        Dynamic(name='p', command='\\baca-effort-ancora-p', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic('"f"-ancora')
        Dynamic(name='f', command='\\baca-effort-ancora-f', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (sempre):

        >>> baca.dynamics.make_dynamic('"p"-sempre')
        Dynamic(name='p', command='\\baca-effort-p-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic('"f"-sempre')
        Dynamic(name='f', command='\\baca-effort-f-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Sub. effort dynamics:

        >>> baca.dynamics.make_dynamic("p-effort-sub")
        Dynamic(name='p', command='\\baca-p-effort-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-effort-sub")
        Dynamic(name='f', command='\\baca-f-effort-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Mezzo:

        >>> baca.dynamics.make_dynamic("m")
        Dynamic(name='m', command='\\baca-m', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=None)

    ..  container:: example

        Parenthesized dynamics:

        >>> baca.dynamics.make_dynamic("(p)")
        Dynamic(name='p', command='\\baca-p-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("(f)")
        Dynamic(name='f', command='\\baca-f-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Poco scratch dynamics:

        >>> baca.dynamics.make_dynamic("p-poco-scratch")
        Dynamic(name='p', command='\\baca-p-poco-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-poco-scratch")
        Dynamic(name='f', command='\\baca-f-poco-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Possibile dynamics:

        >>> baca.dynamics.make_dynamic("p-poss")
        Dynamic(name='p', command='\\baca-p-poss', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-poss")
        Dynamic(name='f', command='\\baca-f-poss', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Scratch dynamics:

        >>> baca.dynamics.make_dynamic("p-scratch")
        Dynamic(name='p', command='\\baca-p-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-scratch")
        Dynamic(name='f', command='\\baca-f-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Sempre dynamics:

        >>> baca.dynamics.make_dynamic("p-sempre")
        Dynamic(name='p', command='\\baca-p-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-sempre")
        Dynamic(name='f', command='\\baca-f-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Subito dynamics:

        >>> baca.dynamics.make_dynamic("p-sub")
        Dynamic(name='p', command='\\baca-p-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-sub")
        Dynamic(name='f', command='\\baca-f-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Whiteout dynamics:

        >>> baca.dynamics.make_dynamic("p-whiteout")
        Dynamic(name='p', command='\\baca-p-whiteout', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.dynamics.make_dynamic("f-whiteout")
        Dynamic(name='f', command='\\baca-f-whiteout', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Al niente hairpins are special-cased to carry to-barline tweaks:

        >>> baca.dynamics.make_dynamic(">o")
        Bundle(indicator=StartHairpin(shape='>o'), tweaks=(Tweak(string='- \\tweak to-barline ##t', tag=None),))

        >>> baca.dynamics.make_dynamic("|>o")
        Bundle(indicator=StartHairpin(shape='|>o'), tweaks=(Tweak(string='- \\tweak to-barline ##t', tag=None),))

    """
    assert isinstance(string, str), repr(string)
    scheme_manifest = SchemeManifest()
    indicator: abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle
    if "_" in string:
        raise Exception(f"use hyphens instead of underscores ({string!r}).")
    if string == "niente":
        indicator = abjad.Dynamic("niente", command=r"\!")
    elif string.endswith("-ancora") and '"' not in string:
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-ancora"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-ancora") and '"' in string:
        dynamic = string.split("-")[0]
        dynamic = dynamic.strip('"')
        command = rf"\baca-effort-ancora-{dynamic}"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-effort-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-effort-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith('("') and string.endswith('")'):
        dynamic = string.strip('(")')
        command = rf"\baca-effort-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith("(") and string.endswith(")"):
        dynamic = string.strip("()")
        command = rf"\baca-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poco-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poco-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poss"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poss"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and not string.startswith('"'):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and string.startswith('"'):
        dynamic = string.split("-")[0].strip('"')
        command = rf"\baca-effort-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-whiteout"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-whiteout"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif "baca-" + string in scheme_manifest.dynamics:
        name = scheme_manifest.dynamic_to_steady_state(string)
        command = "\\baca-" + string
        pieces = string.split("-")
        if pieces[0] in ("sfz", "sffz", "sfffz"):
            sforzando = True
        else:
            sforzando = False
        name_is_textual = not (sforzando)
        indicator = abjad.Dynamic(
            name,
            command=command,
            name_is_textual=name_is_textual,
        )
    elif string.startswith('"'):
        assert string.endswith('"')
        stripped_string = string.strip('"')
        command = rf"\baca-effort-{stripped_string}"
        indicator = abjad.Dynamic(f"{string}", command=command)
    elif string in abjad.StartHairpin.known_shapes:
        indicator = abjad.StartHairpin(string)
        if string.endswith(">o") and not forbid_al_niente_to_bar_line:
            indicator = abjad.bundle(indicator, r"- \tweak to-barline ##t")
    elif string == "!":
        indicator = abjad.StopHairpin()
    elif string == "m":
        indicator = abjad.Dynamic("m", command=r"\baca-m")
    else:
        failed = False
        try:
            indicator = abjad.Dynamic(string)
        except Exception:
            failed = True
        if failed:
            raise Exception(f"the string {string!r} initializes no known dynamic.")
    prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin, abjad.Bundle)
    assert isinstance(indicator, prototype), repr(indicator)
    return indicator

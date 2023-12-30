import abjad

import baca
import pytest


def test_ancora_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-ancora")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-ancora")

    dynamic = baca.dynamics.make_dynamic("f-ancora")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-ancora")


def test_ancora_effort_dynamics():
    dynamic = baca.dynamics.make_dynamic('"p"-ancora')
    assert dynamic == abjad.Dynamic("p", command="\\baca-effort-ancora-p")

    dynamic = baca.dynamics.make_dynamic('"f"-ancora')
    assert dynamic == abjad.Dynamic("f", command="\\baca-effort-ancora-f")


def test_al_niente_start_hairpins():
    """
    Al niente start hairpins are special-cased to carry to-barline tweaks.
    """

    dynamic = baca.dynamics.make_dynamic(">o")
    assert dynamic == abjad.Bundle(
        indicator=abjad.StartHairpin(shape=">o"),
        tweaks=(abjad.Tweak(string="- \\tweak to-barline ##t", tag=None),),
    )

    dynamic = baca.dynamics.make_dynamic("|>o")
    assert dynamic == abjad.Bundle(
        indicator=abjad.StartHairpin(shape="|>o"),
        tweaks=(abjad.Tweak(string="- \\tweak to-barline ##t", tag=None),),
    )


def test_appena_udibile():
    dynamic = baca.dynamics.make_dynamic("appena-udibile")
    assert dynamic == abjad.Dynamic(
        "appena udibile",
        command=r"\baca-appena-udibile",
        name_is_textual=True,
        ordinal=None,
    )


def test_composite_dynamics():
    dynamic = baca.dynamics.make_dynamic("pf")
    assert dynamic == abjad.Dynamic("f", command="\\baca-pf", name_is_textual=True)

    dynamic = baca.dynamics.make_dynamic("pff")
    assert dynamic == abjad.Dynamic("ff", command="\\baca-pff", name_is_textual=True)


def test_dynamics():
    dynamic = baca.dynamics.make_dynamic("p")
    assert dynamic == abjad.Dynamic("p")


def test_effort_dynamics():
    dynamic = baca.dynamics.make_dynamic('"p"')
    assert dynamic == abjad.Dynamic('"p"', command="\\baca-effort-p")

    dynamic = baca.dynamics.make_dynamic('"f"')
    assert dynamic == abjad.Dynamic('"f"', command="\\baca-effort-f")


def test_errors():
    with pytest.raises(Exception):
        baca.dynamics.make_dynamic("text")


def test_mezzo():
    dynamic = baca.dynamics.make_dynamic("m")
    assert dynamic == abjad.Dynamic("m", command="\\baca-m")


def test_niente():
    dynamic = baca.dynamics.make_dynamic("niente")
    assert dynamic == abjad.Dynamic("niente")


def test_parenthesized_dynamics():
    dynamic = baca.dynamics.make_dynamic("(p)")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-parenthesized")

    dynamic = baca.dynamics.make_dynamic("(f)")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-parenthesized")


def test_parenthesized_effort_dynamics():
    dynamic = baca.dynamics.make_dynamic('("p")')
    assert dynamic == abjad.Dynamic("p", command="\\baca-effort-p-parenthesized")

    dynamic = baca.dynamics.make_dynamic('("f")')
    assert dynamic == abjad.Dynamic("f", command="\\baca-effort-f-parenthesized")


def test_poco_scratch_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-poco-scratch")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-poco-scratch")

    dynamic = baca.dynamics.make_dynamic("f-poco-scratch")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-poco-scratch")


def test_possibile_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-poss")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-poss")

    dynamic = baca.dynamics.make_dynamic("f-poss")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-poss")


def test_scratch_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-scratch")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-scratch")

    dynamic = baca.dynamics.make_dynamic("f-scratch")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-scratch")


def test_sempre_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-sempre")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-sempre")

    dynamic = baca.dynamics.make_dynamic("f-sempre")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-sempre")


def test_sempre_effort_dynamics():
    dynamic = baca.dynamics.make_dynamic('"p"-sempre')
    assert dynamic == abjad.Dynamic("p", command="\\baca-effort-p-sempre")

    dynamic = baca.dynamics.make_dynamic('"f"-sempre')
    assert dynamic == abjad.Dynamic("f", command="\\baca-effort-f-sempre")


def test_sforzandi():
    dynamic = baca.dynamics.make_dynamic("sffz")
    assert dynamic == abjad.Dynamic("ff", command=r"\baca-sffz")


def test_start_hairpins():
    dynamic = baca.dynamics.make_dynamic("<")
    assert dynamic == abjad.StartHairpin("<")

    dynamic = baca.dynamics.make_dynamic("o<|")
    assert dynamic == abjad.StartHairpin("o<|")


def test_stop_hairpins():
    dynamic = baca.dynamics.make_dynamic("!")
    assert dynamic == abjad.StopHairpin()


def test_subito_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-sub")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-sub")

    dynamic = baca.dynamics.make_dynamic("f-sub")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-sub")


def test_subito_effort_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-effort-sub")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-effort-sub")

    dynamic = baca.dynamics.make_dynamic("f-effort-sub")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-effort-sub")


def test_whiteout_dynamics():
    dynamic = baca.dynamics.make_dynamic("p-whiteout")
    assert dynamic == abjad.Dynamic("p", command="\\baca-p-whiteout")

    dynamic = baca.dynamics.make_dynamic("f-whiteout")
    assert dynamic == abjad.Dynamic("f", command="\\baca-f-whiteout")

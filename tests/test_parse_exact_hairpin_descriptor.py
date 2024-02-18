import abjad
import baca


def test_01():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p<f")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic(name="p"),
        spanner_start=abjad.StartHairpin(shape="<"),
        stop_indicator=abjad.Dynamic("f"),
    )


def test_02():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p<")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic(name="p"),
        spanner_start=abjad.StartHairpin(shape="<"),
    )


def test_03():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic(name="p"),
    )


def test_04():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("<")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        spanner_start=abjad.StartHairpin(shape="<"),
    )


def test_05():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p+f")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic(name="p"),
        stop_indicator=abjad.Dynamic("f"),
    )


def test_06():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p+")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic(name="p"),
    )


def test_07():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("+f")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        stop_indicator=abjad.Dynamic("f"),
    )


def test_08():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("<f")
    assert len(specifiers) == 1
    specifier = specifiers[0]
    assert specifier == baca.hairpins.ExactHairpinSpecifier(
        spanner_start=abjad.StartHairpin(shape="<"),
        stop_indicator=abjad.Dynamic("f"),
    )


def test_09():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("o< mf>o!")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.ExactHairpinSpecifier(
        spanner_start=abjad.StartHairpin(shape="o<"),
    )
    assert specifiers[1] == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic("mf"),
        spanner_start=abjad.StartHairpin(shape=">o"),
        stop_indicator=abjad.StopHairpin(),
    )


def test_10():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("< <")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.ExactHairpinSpecifier(
        spanner_start=abjad.StartHairpin(shape="<"),
    )
    assert specifiers[1] == baca.hairpins.ExactHairpinSpecifier(
        spanner_start=abjad.StartHairpin(shape="<"),
    )


def test_11():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("<! <!")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.ExactHairpinSpecifier(
        spanner_start=abjad.StartHairpin(shape="<"),
        stop_indicator=abjad.StopHairpin(),
    )
    assert specifiers[1] == baca.hairpins.ExactHairpinSpecifier(
        spanner_start=abjad.StartHairpin(shape="<"),
        stop_indicator=abjad.StopHairpin(),
    )


def test_12():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p f")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic("p"),
    )
    assert specifiers[1] == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic("f"),
    )


def test_13():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p+f p")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic("p"),
        stop_indicator=abjad.Dynamic("f"),
    )
    assert specifiers[1] == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic("p"),
    )


def test_14():
    specifiers = baca.hairpins.parse_exact_hairpin_descriptor("p+f +f")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.ExactHairpinSpecifier(
        start_dynamic=abjad.Dynamic("p"),
        stop_indicator=abjad.Dynamic("f"),
    )
    assert specifiers[1] == baca.hairpins.ExactHairpinSpecifier(
        stop_indicator=abjad.Dynamic("f"),
    )

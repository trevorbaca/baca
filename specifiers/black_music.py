from abjad import *
from abjad.tools import contexttools
from abjad.tools import durationtools
from scf import specifiers


music_specifier = specifiers.MusicSpecifier([
	specifiers.MusicContributionSpecifier(
		name='black violin pizzicati',
		description='lower register violin pizzicati',
		instrument_specifier=specifiers.InstrumentSpecifier(
			instrument=instrumenttools.Violin()
			)
		),
	specifiers.MusicContributionSpecifier(
		name='black cello pizzicati',
		description='midrange cello pizzicati',
		instrument_specifier=specifiers.InstrumentSpecifier(
			instrument=instrumenttools.Cello()
			)
		)
	],
	inventory_name='black music'
	)
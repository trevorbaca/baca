from abjad import *
from abjad.tools import contexttools
from abjad.tools import durationtools
from scf import specifiers


music_specifier = specifiers.MusicSpecifier([
	specifiers.MusicContributionSpecifier(
		name='green violin pizzicati',
		description='upper register violin pizzicati',
		instrument_specifier=specifiers.InstrumentSpecifier(
			instrument=instrumenttools.Violin()
			)
		)
	],
	inventory_name='green music'
	)
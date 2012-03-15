from abjad.tools import durationtools
from abjad.tools import pitchtools
import handlers


red_marcati = handlers.articulations.ReiteratedArticulationHandler(
	articulation_list=['^', '.'],
	minimum_prolated_duration=durationtools.Duration(
		1,
		64
		),
	maximum_prolated_duration=durationtools.Duration(
		1,
		4
		),
	minimum_written_pitch=pitchtools.NamedChromaticPitch(
		'a,,,'
		),
	maximum_written_pitch=pitchtools.NamedChromaticPitch(
		"c''''"
		)
	)
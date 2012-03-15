from abjad.tools import durationtools
import handlers


red_forte = handlers.dynamics.ReiteratedDynamicHandler(
	dynamic_name='f',
	minimum_prolated_duration=durationtools.Duration(
		1,
		16
		)
	)

from abjad.tools import durationtools
import handlers


reiterated_forte = handlers.dynamics.ReiteratedDynamicHandler(
	dynamic_name='f',
	minimum_prolated_duration=durationtools.Duration(
		1,
		16
		)
	)
from abjad.tools import durationtools
import handlertools


red_forte = handlertools.dynamics.ReiteratedDynamicHandler(
	dynamic_name='f',
	minimum_duration=durationtools.Duration(
		1,
		16
		)
	)

from abjad.tools import markuptools


red_directives = markuptools.MarkupInventory([
	markuptools.Markup(
		'\\bold { staccatissimo luminoso }',
		markup_name='staccatissimo',
		style_string='backslash'
		),
	markuptools.Markup(
		'\\italic { serenamente }',
		markup_name='serenamente',
		style_string='backslash'
		)
	],
	name='red directives'
	)
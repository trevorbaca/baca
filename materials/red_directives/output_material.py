from abjad.tools import markuptools


red_directives = markuptools.MarkupInventory([
	markuptools.Markup(
		'\\bold { staccatissimo luminoso }',
		style_string='backslash'
		),
	markuptools.Markup(
		'\\italic { serenamente }',
		style_string='backslash'
		)
	],
	inventory_name='red directives'
	)
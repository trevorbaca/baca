from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._Instrument import _Instrument
from scf import getters
from scf import wizards
from scf.editors.ListEditor import ListEditor
from scf.editors.InstrumentEditor import InstrumentEditor
from scf.editors.TargetManifest import TargetManifest


class PerformerEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_item_class = _Instrument
    target_item_creator_class = wizards.InstrumentCreationWizard
    target_item_creator_class_kwargs = {'is_ranged': True}
    target_item_editor_class = InstrumentEditor
    target_item_identifier = 'instrument'
    target_manifest = TargetManifest(scoretools.Performer,
        ('name', 'nm', getters.get_string),
        target_attribute_name='name',
        )
    
    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def target_items(self):
        return self.target.instruments 

    ### PUBLIC METHODS ###

    # TODO: move to performer creation wizard
    def set_initial_configuration_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        self.conditionally_initialize_target()
        menu = self.make_initial_configuration_menu()
        while True:
            self.push_breadcrumb(self.target.name)
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            if isinstance(result, list):
                for instrument_name in result:
                    instrument_class = instrumenttools.default_instrument_name_to_instrument_class(
                        instrument_name)
                    instrument = instrument_class()
                    self.target.instruments.append(instrument)
                break
            elif result == 'none':
                break
            elif result == 'other':
                self.push_backtrack()
                wizard = wizards.InstrumentCreationWizard(session=self.session, is_ranged=True)
                instruments = wizard.run()
                self.pop_backtrack()
                if self.backtrack():
                    break
                if instruments is not None:
                    for instrument in instruments:
                        self.target.instruments.append(instrument)
                break
            else:
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    # TODO: move to performer creation wizard
    def make_initial_configuration_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True, is_ranged=True) 
        section.title = 'select instruments'
        likely_instruments = self.target.likely_instruments_based_on_performer_name
        likely_instrument_names = [x().instrument_name for x in likely_instruments]
        most_likely_instrument = self.target.most_likely_instrument_based_on_performer_name
        default_index = None
        if most_likely_instrument is not None:
            most_likely_instrument_name = most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(most_likely_instrument_name)
            likely_instrument_names[most_likely_index] = '{} (default)'.format(most_likely_instrument_name)
            most_likely_number = most_likely_index + 1
            default_index = most_likely_index
        if likely_instruments:
            section.tokens = likely_instrument_names
            section.default_index = default_index
            section = menu.make_section(is_keyed=False)
            section.append(('other', 'other instruments'))
        else:
            section.tokens = instrumenttools.list_instrument_names()
            section.default_index = default_index
            section = menu.make_section(is_keyed=False)
        section.append(('none', 'no instruments'))
        return menu

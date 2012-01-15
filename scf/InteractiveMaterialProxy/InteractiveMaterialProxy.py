from baca.scf.MaterialProxy import MaterialProxy
import copy


class InteractiveMaterialProxy(MaterialProxy):

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, user_input_wrapper):
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        
    def edit_item(self, key, value):
        prompt = key.replace('_', ' ')
        default = repr(value)
        response = self.handle_raw_input_with_default('{}> '.format(prompt), default=default)
        command = 'from abjad import *'
        exec(command)
        new_value = eval(response)
        return new_value

    def initialize_user_input_wrapper(self):
        user_input_wrapper = copy.deepcopy(self.user_input_template)
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        return user_input_wrapper

    def make_lilypond_file_from_user_input_wrapper(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        return lilypond_file

    def overwrite_user_input_wrapper_with_demo_user_input_values(self, user_input_wrapper):
        for key in self.user_input_template:
            user_input_wrapper[key] = self.user_input_template[key]    

    def read_user_input_values_from_disk(self):
        import baca
        score_wrangler = baca.scf.ScoreWrangler()
        material_proxy = score_wrangler.select_interactive_material_proxy(klasses=(type(self),))
        self.user_input_wrapper = copy.deepcopy(material_proxy.user_input_wrapper)
    
    def run(self, user_input_wrapper=None):
        if user_input_wrapper is None:
            user_input_wrapper = self.initialize_user_input_wrapper()
        self.user_input_wrapper = user_input_wrapper
        self._original_score = self.score
        self._original_material_underscored_name = self.material_underscored_name
        self._original_user_input_wrapper = copy.deepcopy(user_input_wrapper)
        while True:
            menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
            section.tokens = self.user_input_wrapper.editable_lines
            if self.user_input_wrapper.is_complete:
                section.append(('p', 'show pdf of given input'))
                section.append(('m', 'write material to disk'))
            if self.has_material_underscored_name:
                section.append(('n', 'rename material'))
            else:
                section.append(('n', 'name material'))
            section.append(('nc', 'clear name'))
            section.append(('d', 'show demo input values'))
            section.append(('o', 'overwrite with demo input values'))
            section.append(('i', 'read values from disk'))
            section.append(('c', 'clear values'))
            if self.purview is not None:
                section.append(('l', 'change location'))
            else:
                section.append(('l', 'set location'))
            result = menu.run()
            if result == 'c':
                self.clear_user_input_wrapper(self.user_input_wrapper)
            elif result == 'd':
                self.show_demo_user_input_values()
            elif result == 'i':
                self.read_user_input_values_from_disk()
            elif result == 'l':
                self.set_purview_interactively()
            elif result == 'n':
                self.name_material()
            elif result == 'nc':
                self.unname_material()
            elif result == 'o':
                self.overwrite_user_input_wrapper_with_demo_user_input_values(self.user_input_wrapper)
            elif result == 'p':
                lilypond_file = self.make_lilypond_file_from_user_input_wrapper(self.user_input_wrapper)
                lilypond_file.file_initial_user_includes.append(self.stylesheet)
                lilypond_file.header_block.title = markuptools.Markup(self.generic_output_name.capitalize())
                lilypond_file.header_block.subtitle = markuptools.Markup('(unsaved)')
                iotools.show(lilypond_file)
            elif result == 'src':
                self.edit_source_file()
            elif mathtools.is_integer_equivalent_expr(result):
                number = int(result)    
                index = number - 1
                result, value = self.user_input_wrapper.list_items[index]
                new_value = self.edit_item(result)
                self.user_input_wrapper[result] = new_value

    def show_demo_user_input_values(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        items = []
        for i, (key, value) in enumerate(self.user_input_template.iteritems()):
            item = '{}: {!r}'.format(key.replace('_', ' '), value)
            items.append(item)
        section.tokens = items
        menu.run()

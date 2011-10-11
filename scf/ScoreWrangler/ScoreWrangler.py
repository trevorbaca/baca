from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.menuing import Menu
from baca.scf.ScoreProxy import ScoreProxy
import os


class ScoreWrangler(DirectoryProxy):

    def __init__(self):
        DirectoryProxy.__init__(self, os.environ.get('SCORES'))

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC METHODS ###

    def create_score_package(self, score_package_importable_name):
        raise NotImplementedError

    def fix_score_package_structures(self):
        for score_proxy in self.iterate_score_proxies():
            score_proxy.fix_package_structure()
            score_proxy.profile_package_structure()
            print ''

    def get_score_package_short_name_from_user(self, menu_header=None):
        menu_specifier = Menu(client=self)
        menu_specifier.menu_header = menu_header
        menu_specifier.menu_body = 'select score by number.'
        menu_specifier.items_to_number = self.list_score_titles_with_years()
        number, score_title = menu_specifier.display_menu()
        score_package_short_name = self.score_title_to_score_package_short_name(score_title)
        return score_package_short_name

    def iterate_interactive_material_package_proxies(self):
        for material_package_proxy in self.iterate_material_package_proxies():
            if material_package_proxy.is_interactive:
                yield material_package_proxy

    def iterate_material_package_proxies(self, class_names=None):
        for score_proxy in self.iterate_score_proxies():
            for material_package_proxy in score_proxy.iterate_material_package_proxies():
                if class_names is None or material_package_proxy.get_tag('maker') in class_names:
                    yield material_package_proxy
        for material_name in os.listdir(self.baca_materials_directory_name):
            if material_name[0].isalpha():
                package_importable_name = 'baca.materials.%s' % material_name
                material_package_proxy = self.get_material_package_proxy(package_importable_name)
                if class_names is None or material_package_proxy.get_tag('maker') in class_names:
                    yield material_package_proxy

    def iterate_score_proxies(self):
        for score_package_importable_name in self.list_score_package_importable_names():
            score_proxy = ScoreProxy(score_package_importable_name)
            yield score_proxy

    def list_numbered_score_titles_with_years(self):
        numbered_score_titles_with_years = []
        for i, score_title_with_year in enumerate(self.list_score_titles_with_years()):
            number = str(i + 1)
            numbered_score_titles_with_years.append((number, score_title_with_year))
        return numbered_score_titles_with_years

    def list_score_directories(self):
        score_directories = []
        for score_package_importable_name in self.list_score_package_importable_names():
            score_directory = os.path.join(self.directory, score_package_importable_name)
            score_directories.append(score_directory)
        return score_directories

    def list_score_info_triples(self):
        score_info_triples = []
        for score_package_importable_name in self.list_score_package_importable_names():
            score_title = self.score_package_short_name_to_score_title(score_package_importable_name)
            score_year = self.score_package_short_name_to_score_year(score_package_importable_name)
            score_info_triple = (score_package_importable_name, score_title, score_year)
            score_info_triples.append(score_info_triple)
        return score_info_triples

    def list_score_package_importable_names(self):
        '''This method is primary.
        '''
        score_package_importable_names = []
        for score_package_importable_name in os.listdir(self.directory):
            directory = os.path.join(self.directory, score_package_importable_name)
            if os.path.isdir(directory):
                initializer = os.path.join(directory, '__init__.py')
                if os.path.isfile(initializer):
                    if not self.score_package_short_name_to_hide_in_front_end(score_package_importable_name):
                        score_package_importable_names.append(score_package_importable_name)
        return score_package_importable_names

    def list_score_package_short_names(self):
        return self.list_score_package_importable_names()

    def list_score_titles(self):
        score_titles = []
        for score_package_short_name in self.list_score_package_short_names():
            score_title = self.score_package_short_name_to_score_title(score_package_short_name)
            score_titles.append(score_title)
        return score_titles

    def list_score_titles_with_years(self):
        score_titles_with_years = []
        for score_package_short_name, score_title, score_year in self.list_score_info_triples():
            score_title_with_year = '%s (%s)' % (score_title, score_year)
            score_titles_with_years.append(score_title_with_year)
        return score_titles_with_years

    def list_materials_packages(self):
        materials_packages = []
        for score_package_importable_name in self.list_well_formed_score_package_importable_names():
            score_proxy = ScoreProxy(score_package_importable_name)
            materials_packages.extend(score_proxy.list_materials_packages())
        return materials_packages

    def list_well_formed_score_package_importable_names(self):
        score_package_importable_names = os.listdir(self.directory)
        score_package_importable_names = [x for x in score_package_importable_names if x[0].isalpha()]
        score_package_importable_names.remove('poeme')
        return score_package_importable_names

    def profile_score_package_structures(self):
        for score_proxy in self.iterate_score_proxies():
            score_proxy.profile_package_structure()
            print ''

    def score_package_short_name_to_hide_in_front_end(self, score_package_short_name):
        try:
            exec('from %s import _hide_in_front_end' % score_package_short_name)
            return _hide_in_front_end
        except ImportError:
            return False

    def score_package_short_name_to_score_title(self, score_package_short_name):
        try:
            exec('from %s import score_title' % score_package_short_name)
            return score_title
        except ImportError:
            return None

    def score_package_short_name_to_score_year(self, score_package_short_name):
        try:
            exec('from %s import score_year' % score_package_short_name)
            return score_year
        except ImportError:
            return None

    def score_title_to_score_package_short_name(self, score_title):
        for package_short_name, title, year in self.list_score_info_triples():
            if score_title.startswith(title):
                return package_short_name

    def select_interactive_material_package_proxy(self, menu_header=None, klasses=None):
        material_package_proxies = list(self.iterate_interactive_material_package_proxies())
        menu = Menu(client=self)
        menu.menu_header = menu_header
        menu.items_to_number = material_package_proxies
        key, value = menu.display_menu()
        return value

    def select_score_interactively(self, menu_header=None):
        menu = Menu(client=self)
        menu.menu_header = menu_header
        menu.menu_body = 'select score'
        menu.items_to_number = self.list_score_titles_with_years()
        menu.sentence_length_items.append(('s', 'studio'))
        key, value = menu.display_menu()
        if key == 's':
            return None
        score_package_short_name = self.score_title_to_score_package_short_name(value)
        score_proxy = ScoreProxy(score_package_short_name)
        return score_proxy
    
    def svn_ci_scores(self, prompt_proceed=True):
        commit_message = raw_input('Commit message> ')
        print ''
        print 'Commit message will be: "%s"\n' % commit_message
        if not self.confirm():
            return
        for score_proxy in self.iterate_score_proxies():
            score_proxy.svn_ci(commit_message=commit_message, prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

    def svn_st_scores(self, prompt_proced=True):
        for score_proxy in self.iterate_score_proxies():
            score_proxy.svn_st(prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

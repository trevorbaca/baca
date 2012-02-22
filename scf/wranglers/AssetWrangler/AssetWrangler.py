from abjad.tools import iotools
from baca.scf.core.SCFObject import SCFObject
import os


class AssetWrangler(SCFObject):

    def __init__(self, 
        score_external_asset_container_importable_name=None, 
        score_internal_asset_container_importable_name_infix=None, 
        session=None):
        SCFObject.__init__(self, session=session)
        if score_external_asset_container_importable_name is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_external_asset_container_importable_name)
        if score_internal_asset_container_importable_name_infix is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_internal_asset_container_importable_name_infix)
        self._score_external_asset_container_importable_name = \
            score_external_asset_container_importable_name
        self._score_internal_asset_container_importable_name_infix = \
            score_internal_asset_container_importable_name_infix

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.score_external_asset_container_importable_name == \
                other.score_external_asset_container_importable_name:
                if self.score_internal_asset_container_importable_name_infix == \
                    other.score_internal_asset_container_importable_name_infix:
                    return True
        return False

    def __repr__(self):
        parts = []
        if self.score_external_asset_container_importable_name:
            parts.append(self.score_external_asset_container_importable_name)
        if self.score_internal_asset_container_importable_name_infix:
            parts.append(self.score_internal_asset_container_importable_name_infix)
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self.class_name, parts)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    # asset class #

    @property
    def asset_class(self):
        self.print_implemented_on_child_classes()

    # asset containers (all) #

    @property
    def asset_container_importable_names(self):
        result = [] 
        if self.score_external_asset_container_importable_name:
            result.append(self.score_external_asset_container_importable_name)
        result.extend(self.list_score_internal_asset_container_importable_names())
        return result

    @property
    def asset_container_path_names(self):
        result = []
        for package_importable_name in self.asset_container_importable_names:
            result.append(self.package_importable_name_to_path_name(package_importable_name))
        return result

    # current asset container #

    @property
    def current_asset_container_importable_name(self):
        if self.session.is_in_score:
            return self.dot_join([
                self.session.current_score_package_short_name, 
                self.score_internal_asset_container_importable_name_infix])
        else:
            return self.score_external_asset_container_importable_name

    @property
    def current_asset_container_path_name(self):
        return self.package_importable_name_to_path_name(
            self.current_asset_container_importable_name)

    # score-external asset container #

    @property
    def score_external_asset_container_importable_name(self):
        return self._score_external_asset_container_importable_name
    
    @property
    def score_external_asset_container_initializer_file_name(self):
        return os.path.join(self.score_external_asset_container_path_name, '__init__.py')

    @property
    def score_external_asset_container_path_name(self):
        return self.package_importable_name_to_path_name(
            self.score_external_asset_container_importable_name)

    # score-external assets #

    @property
    def score_external_asset_human_readable_names(self):
        result = []
        for path_name in self.score_external_asset_path_names:
            path_name = path_name.rstrip(os.path.sep)
            base_name = os.path.basename(path_name)
            human_readable_name = self.change_string_to_human_readable_string(base_name)
            result.append(human_readable_name)
        return result

    @property
    def score_external_asset_path_names(self):
        result = []
        if self.score_external_asset_container_path_name:
            for name in os.listdir(self.score_external_asset_container_path_name):
                if name[0].isalpha():
                    result.append(os.path.join(self.score_external_asset_container_path_name, name))
        return result

    @property
    def score_external_asset_proxies(self):
        result = []
        for asset_path_name in self.score_external_asset_path_names:
            asset_proxy = self.get_asset_proxy(asset_path_name)
            result.append(asset_proxy)
        return result

    # infix #

    @property
    def score_internal_asset_container_importable_name_infix(self):
        return self._score_internal_asset_container_importable_name_infix

    # temporary asset #

    @property
    def temporary_asset_path_name(self):
        return os.path.join(self.current_asset_container_path_name, self.temporary_asset_short_name)

    @property
    def temporary_asset_short_name(self):
        self.print_implemented_on_child_classes()

    ### PUBLIC METHODS ###
    
    def conditionally_make_asset_container_packages(self, is_interactive=False):
        self.conditionally_make_score_external_asset_container_package()
        self.conditionally_make_score_internal_asset_container_packages()
        self.proceed('missing packages created.', prompt=is_interactive)

    def conditionally_make_score_external_asset_container_package(self):
        self.conditionally_make_empty_package(self.score_external_asset_container_importable_name)

    def conditionally_make_score_internal_asset_container_packages(self, head=None):
        for score_internal_asset_container_importable_name in \
            self.list_score_internal_asset_container_importable_names(head=head):
            self.conditionally_make_empty_package(score_internal_asset_container_importable_name)

    def fix_visible_assets(self, is_interactive=True):
        results = []
        for asset_proxy in self.list_visible_asset_proxies():
            results.append(asset_proxy.fix(is_interactive=is_interactive))
            if is_interactive:
                asset_proxy.profile()
        return results

    def get_asset_proxy(self, asset_full_name):
        return self.asset_class(asset_full_name, session=self.session)

    # assets (all) #

    def list_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_asset_path_names(head=head):
            path_name = path_name.rstrip(os.path.sep)
            base_name = os.path.basename(path_name)
            human_readable_name = self.change_string_to_human_readable_string(base_name)
            result.append(human_readable_name)
        return result

    def list_asset_path_names(self, head=None):
        result = []
        if head in (None, self.home_package_importable_name):
            result.extend(self.score_external_asset_path_names)
        result.extend(self.list_score_internal_asset_path_names(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for asset_path_name in self.list_asset_path_names(head=head):
            asset_proxy = self.get_asset_proxy(asset_path_name)
            result.append(asset_proxy)
        return result

    # score-internal asset containers #

    def list_score_internal_asset_container_importable_names(self, head=None):
        result = []
        for score_package_short_name in self.list_score_package_short_names(head=head):
            parts = [score_package_short_name]
            if self.score_internal_asset_container_importable_name_infix:
                parts.append(self.score_internal_asset_container_importable_name_infix)
            score_internal_score_package_importable_name = self.dot_join(parts)
            result.append(score_internal_score_package_importable_name)
        return result

    def list_score_internal_asset_container_path_names(self, head=None):
        result = []
        for package_importable_name in \
            self.list_score_internal_asset_container_importable_names(head=head):
            result.append(self.package_importable_name_to_path_name(package_importable_name))
        return result            

    # score-internal assets #

    def list_score_internal_asset_path_names(self, head=None):
        result = []
        for path_name in self.list_score_internal_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                if name[0].isalpha():
                    result.append(os.path.join(path_name, name))
        return result

    # visible assets #

    def list_visible_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_visible_asset_path_names(head=head):
            path_name = path_name.rstrip(os.path.sep)
            base_name = os.path.basename(path_name)
            human_readable_name = self.change_string_to_human_readable_string(base_name)
            result.append(human_readable_name)
        return result

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_path_names(head=head)
        bodies = self.list_visible_asset_human_readable_names(head=head)
        return zip(keys, bodies)

    def list_visible_asset_path_names(self, head=None):
        return self.list_asset_path_names(head=head)

    def list_visible_asset_proxies(self, head=None):
        return self.list_asset_proxies(head=head)

    # other #

    def make_asset(self, asset_short_name):
        assert iotools.is_underscore_delimited_lowercase_string(asset_short_name)
        asset_path_name = os.path.join(self.current_asset_container_path_name, asset_short_name)
        asset_proxy = self.get_asset_proxy(asset_path_name)
        asset_proxy.write_stub_to_disk()

    def make_asset_interactively(self):
        self.print_implemented_on_child_classes()

    def profile_visible_assets(self):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.profile()

    def run(self):
        self.print_implemented_on_child_classes()

    def svn_add(self, prompt=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_add(prompt=False)
        self.proceed(prompt=prompt)

    def svn_ci(self, prompt=True):
        getter = self.make_getter(where=self.where())
        getter.append_string('commit message')
        commit_message = getter.run()
        if self.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self.display(line)
        if not self.confirm():
            return
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_ci(commit_message=commit_message, prompt=False)
        self.proceed(prompt=prompt)

    def svn_st(self, prompt=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_st(prompt=False)
        self.proceed(prompt=prompt)

    def svn_up(self, prompt=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_up(prompt=False)
        self.proceed(prompt=prompt)

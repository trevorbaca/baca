from abjad.tools import iotools
from baca.scf.core.SCFObject import SCFObject
import os


class AssetWrangler(SCFObject):

    def __init__(self, 
        score_external_asset_container_package_importable_name=None, 
        score_internal_asset_container_package_importable_name_suffix=None, 
        session=None):
        SCFObject.__init__(self, session=session)
        if score_external_asset_container_package_importable_name is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_external_asset_container_package_importable_name)
        if score_internal_asset_container_package_importable_name_suffix is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_internal_asset_container_package_importable_name_suffix)
        self._score_external_asset_container_package_importable_name = \
            score_external_asset_container_package_importable_name
        self._score_internal_asset_container_package_importable_name_suffix = \
            score_internal_asset_container_package_importable_name_suffix

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.score_external_asset_container_package_importable_name == \
                other.score_external_asset_container_package_importable_name:
                if self.score_internal_asset_container_package_importable_name_suffix == \
                    other.score_internal_asset_container_package_importable_name_suffix:
                    return True
        return False

    def __repr__(self):
        parts = []
        if self.score_external_asset_container_package_importable_name:
            parts.append(self.score_external_asset_container_package_importable_name)
        if self.score_internal_asset_container_package_importable_name_suffix:
            parts.append(self.score_internal_asset_container_package_importable_name_suffix)
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self.class_name, parts)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def current_asset_container_directory_name(self):
        return self.package_importable_name_to_directory_name(
            self.current_asset_container_package_importable_name)

    @property
    def current_asset_container_package_importable_name(self):
        if self.session.is_in_score:
            return self.dot_join([
                self.session.current_score_package_short_name, 
                self.score_internal_asset_container_package_importable_name_suffix])
        else:
            return self.score_external_asset_container_package_importable_name

    @property
    def score_external_wrangled_asset_path_names(self):
        result = []
        if self.score_external_asset_container_directory_name:
            for name in os.listdir(self.score_external_asset_container_directory_name):
                if name[0].isalpha():
                    result.append(os.path.join(self.score_external_asset_container_directory_name, name))
        return result

    @property
    def score_external_asset_container_directory_name(self):
        return self.package_importable_name_to_directory_name(
            self.score_external_asset_container_package_importable_name)

    @property
    def score_external_asset_container_initializer_file_name(self):
        return os.path.join(self.score_external_asset_container_directory_name, '__init__.py')

    @property
    def score_external_asset_container_package_importable_name(self):
        return self._score_external_asset_container_package_importable_name
    
    @property
    def score_internal_asset_container_package_importable_name_suffix(self):
        return self._score_internal_asset_container_package_importable_name_suffix

    @property
    def asset_container_directory_names(self):
        result = []
        for asset_container_package_importable_name in self.asset_container_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(
                asset_container_package_importable_name))
        return result

    @property
    def asset_container_package_importable_names(self):
        result = [] 
        if self.score_external_asset_container_package_importable_name:
            result.append(self.score_external_asset_container_package_importable_name)
        result.extend(self.list_score_internal_asset_container_package_importable_names())
        return result

    ### PUBLIC METHODS ###
    
    def conditionally_make_score_external_asset_container_package(self):
        self.conditionally_make_empty_package(self.score_external_asset_container_package_importable_name)

    def conditionally_make_score_internal_asset_container_packages(self, head=None):
        for score_internal_asset_container_package_importable_name in \
            self.list_score_internal_asset_container_package_importable_names(head=head):
            self.conditionally_make_empty_package(score_internal_asset_container_package_importable_name)

    def conditionally_make_asset_container_packages(self, is_interactive=False):
        self.conditionally_make_score_external_asset_container_package()
        self.conditionally_make_score_internal_asset_container_packages()
        self.proceed('missing packages created.', prompt=is_interactive)

    def get_wrangled_asset_proxy(self, asset_full_name):
        self.print_implemented_on_child_classes()
        
    def list_score_internal_wrangled_asset_path_names(self, head=None):
        result = []
        for directory_name in self.list_score_internal_asset_container_directory_names(head=head):
            for name in os.listdir(directory_name):
                if name[0].isalpha():
                    result.append(os.path.join(directory_name, name))
        return result

    def list_score_internal_asset_container_directory_names(self, head=None):
        result = []
        for package_importable_name in \
            self.list_score_internal_asset_container_package_importable_names(head=head):
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result            

    def list_score_internal_asset_container_package_importable_names(self, head=None):
        result = []
        for score_package_short_name in self.list_score_package_short_names(head=head):
            parts = [score_package_short_name]
            if self.score_internal_asset_container_package_importable_name_suffix:
                parts.append(self.score_internal_asset_container_package_importable_name_suffix)
            score_internal_score_package_importable_name = self.dot_join(parts)
            result.append(score_internal_score_package_importable_name)
        return result

    def list_visible_wrangled_asset_proxies(self, head=None):
        return self.list_wrangled_asset_proxies(head=head)

    def list_wrangled_asset_menuing_pairs(self, head=None):
        keys = self.list_visible_wrangled_asset_path_names(head=head)
        bodies = self.list_visible_wrangled_asset_human_readable_names(head=head)
        return zip(keys, bodies)

    def list_wrangled_asset_proxies(self, head=None):
        self.print_not_implemented()

    def make_wrangled_asset(self, package_short_name):
        self.print_not_implemented()

    def make_wrangled_asset_interactively(self):
        self.print_implemented_on_child_classes()

    def profile_visible_assets(self):
        self.print_not_implemented()

    def run(self):
        self.print_implemented_on_child_classes()

    def svn_add(self, prompt=True):
        for asset_proxy in self.list_visible_wrangled_asset_proxies():
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
        for asset_proxy in self.list_visible_wrangled_asset_proxies():
            asset_proxy.svn_ci(commit_message=commit_message, prompt=False)
        self.proceed(prompt=prompt)

    def svn_st(self, prompt=True):
        for asset_proxy in self.list_visible_wrangled_asset_proxies():
            asset_proxy.svn_st(prompt=False)
        self.proceed(prompt=prompt)

    def svn_up(self, prompt=True):
        for asset_proxy in self.list_visible_wrangled_asset_proxies():
            asset_proxy.svn_up(prompt=False)
        self.proceed(prompt=prompt)

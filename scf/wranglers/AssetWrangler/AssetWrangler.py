from abjad.tools import iotools
from baca.scf.core.SCFObject import SCFObject
from baca.scf.proxies.PackageProxy import PackageProxy
import os


class AssetWrangler(SCFObject):

    def __init__(self, 
        score_external_asset_container_importable_names=None, 
        score_internal_asset_container_importable_name_infix=None, 
        session=None):
        SCFObject.__init__(self, session=session)
        if score_external_asset_container_importable_names:
            assert all([iotools.is_underscore_delimited_lowercase_package_name(x)
                for x in score_external_asset_container_importable_names])
        if score_internal_asset_container_importable_name_infix:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_internal_asset_container_importable_name_infix)
        self._score_external_asset_container_importable_names = \
            score_external_asset_container_importable_names or []
        self._score_internal_asset_container_importable_name_infix = \
            score_internal_asset_container_importable_name_infix

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.list_score_external_asset_container_importable_names() == \
                other.list_score_external_asset_container_importable_names():
                if self.score_internal_asset_container_importable_name_infix == \
                    other.score_internal_asset_container_importable_name_infix:
                    return True
        return False

    def __repr__(self):
        parts = []
        parts.extend(self.list_score_external_asset_container_importable_names())
        if self.score_internal_asset_container_importable_name_infix:
            parts.append(self.score_internal_asset_container_importable_name_infix)
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self.class_name, parts)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    # asset class #

    @property
    def asset_class(self):
        self.print_implemented_on_child_classes()

    @property
    def asset_container_class(self):
        return PackageProxy

    # current asset container #

    @property
    def current_asset_container_human_readable_name(self):
        return self.path_name_to_human_readable_base_name(self.current_asset_container_path_name)

    @property
    def current_asset_container_importable_name(self):
        if self.session.is_in_score:
            return self.dot_join([
                self.session.current_score_package_short_name, 
                self.score_internal_asset_container_importable_name_infix])
        elif self.list_score_external_asset_container_importable_names():
            return self.list_score_external_asset_container_importable_names()[0]

    @property
    def current_asset_container_path_name(self):
        return self.package_importable_name_to_path_name(
            self.current_asset_container_importable_name)

    @property
    def current_asset_container_proxy(self):
        return self.asset_container_class(self.current_asset_container_importable_name)

    # infix #

    @property
    def score_internal_asset_container_importable_name_infix(self):
        return self._score_internal_asset_container_importable_name_infix

    # temporary asset #

    @property
    def temporary_asset_human_readable_name(self):
        return self.path_name_to_human_readable_base_name(self.temporary_asset_path_name)

    @property
    def temporary_asset_path_name(self):
        return os.path.join(self.current_asset_container_path_name, self.temporary_asset_short_name)

    @property
    def temporary_asset_short_name(self):
        self.print_implemented_on_child_classes()

    @property
    def temporary_asset_proxy(self):
        return self.asset_class(self.temporary_asset_importable_name)

    ### PUBLIC METHODS ###
    
    def conditionally_make_asset_container_packages(self, is_interactive=False):
        self.conditionally_make_score_external_asset_container_package()
        self.conditionally_make_score_internal_asset_container_packages()
        self.proceed('missing packages created.', prompt=is_interactive)

    def conditionally_make_score_external_asset_container_package(self):
        for importable_name in self.list_score_external_asset_container_importable_names():
            self.conditionally_make_empty_package(importable_name)

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

    # asset containers (all) #

    def list_asset_container_human_readable_names(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_human_readable_names(head=head))    
        result.extend(self.list_score_internal_asset_container_human_readable_names(head=head))    
        return result

    def list_asset_container_importable_names(self, head=None):
        result = [] 
        result.extend(self.list_score_external_asset_container_importable_names(head=head))
        result.extend(self.list_score_internal_asset_container_importable_names(head=head))
        return result

    def list_asset_container_path_names(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_path_names(head=head))
        result.extend(self.list_score_internal_asset_container_path_names(head=head))
        return result

    def list_asset_container_proxies(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_proxies(head=head))
        result.extend(self.list_score_internal_asset_container_proxies(head=head))
        return result

    # assets (all) #

    def list_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_asset_path_names(self, head=None):
        result = []
        if head in (None, self.home_package_importable_name):
            result.extend(self.list_score_external_asset_path_names(head=head))
        result.extend(self.list_score_internal_asset_path_names(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for asset_path_name in self.list_asset_path_names(head=head):
            asset_proxy = self.get_asset_proxy(asset_path_name)
            result.append(asset_proxy)
        return result

    # score-external asset containers #

    def list_score_external_asset_container_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_external_asset_container_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_score_external_asset_container_importable_names(self, head=None):
        result = []
        for importable_name in self._score_external_asset_container_importable_names:
            if head is None or importable_name.startswith(head):
                result.append(importable_name)
        return result
    
    def list_score_external_asset_container_path_names(self, head=None):
        result = []
        for importable_name in self.list_score_external_asset_container_importable_names(head=head):
            result.append(self.package_importable_name_to_path_name(importable_name))
        return result

    def list_score_external_asset_container_proxies(self, head=None):
        result = []
        for importable_name in self.list_score_external_asset_container_importable_names(head=head):
            asset_container_proxy = self.asset_container_class(importable_name)
            result.append(asset_container_proxy)
        return result

    # score-external assets #

    def list_score_external_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_external_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_score_external_asset_path_names(self, head=None):
        result = []
        for path_name in self.list_score_external_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                if name[0].isalpha():
                    result.append(os.path.join(path_name, name))
        return result

    def list_score_external_asset_proxies(self, head=None):
        result = []
        for asset_path_name in self.list_score_external_asset_path_names(head=head):
            asset_proxy = self.get_asset_proxy(asset_path_name)
            result.append(asset_proxy)
        return result

    # score-internal asset containers #

    def list_score_internal_asset_container_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_internal_asset_container_human_readable_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

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

    def list_score_internal_asset_container_proxies(self, head=None):
        result = []
        for importable_name in self.list_score_internal_asset_container_importable_names(head=head):
            asset_container_proxy = self.asset_container_class(importable_name)
            result.append(asset_container_proxy)
        return result

    # score-internal assets #

    def list_score_internal_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_internal_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_score_internal_asset_path_names(self, head=None):
        result = []
        for path_name in self.list_score_internal_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                if name[0].isalpha():
                    result.append(os.path.join(path_name, name))
        return result

    def list_score_internal_asset_proxies(self, head=None):
        result = []
        for importable_name in self.list_score_internal_asset_importable_names(head=head):
            asset_proxy = self.asset_class_name(importable_name)
            result.append(asset_proxy)
        return result

    # visible assets #

    def list_visible_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_visible_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

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

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_path_names(head=head)
        bodies = self.list_visible_asset_human_readable_names(head=head)
        return zip(keys, bodies)

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

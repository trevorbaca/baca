from abjad.tools import iotools
from baca.scf.proxies.PackageProxy import PackageProxy
from baca.scf.core.SCFObject import SCFObject
import os


class PackageWrangler(SCFObject):

    def __init__(self, 
        score_external_wrangler_target_package_importable_name=None, 
        score_internal_wrangler_target_package_importable_name_suffix=None, 
        session=None):
        SCFObject.__init__(self, session=session)
        if score_external_wrangler_target_package_importable_name is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_external_wrangler_target_package_importable_name)
        if score_internal_wrangler_target_package_importable_name_suffix is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_internal_wrangler_target_package_importable_name_suffix)
        self._score_external_wrangler_target_package_importable_name = \
            score_external_wrangler_target_package_importable_name
        self._score_internal_wrangler_target_package_importable_name_suffix = \
            score_internal_wrangler_target_package_importable_name_suffix

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.score_external_wrangler_target_package_importable_name == \
                other.score_external_wrangler_target_package_importable_name:
                if self.score_internal_wrangler_target_package_importable_name_suffix == \
                    other.score_internal_wrangler_target_package_importable_name_suffix:
                    return True
        return False

    def __repr__(self):
        parts = []
        if self.score_external_wrangler_target_package_importable_name:
            parts.append(self.score_external_wrangler_target_package_importable_name)
        if self.score_internal_wrangler_target_package_importable_name_suffix:
            parts.append(self.score_internal_wrangler_target_package_importable_name_suffix)
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self.class_name, parts)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def current_wrangler_target_directory_name(self):
        return self.package_importable_name_to_directory_name(
            self.current_wrangler_target_package_importable_name)

    @property
    def current_wrangler_target_package_importable_name(self):
        if self.session.is_in_score:
            score_package_short_name = self.session.current_score_package_short_name
            return self.dot_join([
                score_package_short_name, self.score_internal_wrangler_target_package_importable_name_suffix])
        else:
            return self.score_external_wrangler_target_package_importable_name

    @property
    def score_internal_wrangler_target_package_importable_name_suffix(self):
        return self._score_internal_wrangler_target_package_importable_name_suffix

    @property
    def temporary_package_directory_name(self):
        return os.path.join(self.current_wrangler_target_directory_name, '__temporary_package')

    @property
    def temporary_package_importable_name(self):
        package_path = self.current_wrangler_target_package_importable_name
        if package_path:
            return self.dot_join([package_path, '__temporary_package'])
        else:
            return '__temporary_package'

    @property
    def score_external_wrangled_package_directory_names(self):
        result = []
        for package_importable_name in self.score_external_wrangled_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result
        
    @property
    def score_external_wrangled_package_importable_names(self):
        result = []
        if self.score_external_wrangler_target_package_importable_name is not None:
            global_package_directory_name = self.package_importable_name_to_directory_name(
                self.score_external_wrangler_target_package_importable_name)
            for name in os.listdir(global_package_directory_name):
                if name[0].isalpha():
                    result.append('{}.{}'.format(
                        self.score_external_wrangler_target_package_importable_name, name))
        return result

    @property
    def score_external_wrangler_target_directory_name(self):
        return self.package_importable_name_to_directory_name(
            self.score_external_wrangler_target_package_importable_name)

    @property
    def score_external_wrangler_target_package_importable_name(self):
        return self._score_external_wrangler_target_package_importable_name
    
    @property
    def wrangler_target_directory_names(self):
        result = []
        for wrangler_target_package_importable_name in self.wrangler_target_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(
                wrangler_target_package_importable_name))
        return result

    @property
    def wrangler_target_package_importable_names(self):
        result = [] 
        if self.score_external_wrangler_target_package_importable_name:
            result.append(self.score_external_wrangler_target_package_importable_name)
        result.extend(self.list_score_internal_wrangler_target_package_importable_names())
        return result

    ### PUBLIC METHODS ###
    
    def conditionally_make_score_external_wrangler_target_package(self):
        self.conditionally_make_empty_package(self.score_external_wrangler_target_package_importable_name)

    def conditionally_make_score_internal_wrangler_target_packages(self, head=None):
        for score_internal_wrangler_target_package_importable_name in \
            self.list_score_internal_wrangler_target_package_importable_names(head=head):
            self.conditionally_make_empty_package(score_internal_wrangler_target_package_importable_name)

    def conditionally_make_wrangler_target_packages(self):
        self.conditionally_make_score_external_wrangler_target_package()
        self.conditionally_make_score_internal_wrangler_target_packages()

    def fix_visible_wrangled_package_structures(self, prompt=True):
        results = []
        for package_proxy in self.list_visible_wrangled_package_proxies():
            results.append(package_proxy.fix_package_structure(is_interactive=prompt))
            if prompt:
                package_proxy.profile_package_structure()
        return results

    def get_wrangled_package_proxy(self, package_importable_name):
        return PackageProxy(package_importable_name, session=self.session)
        
    def list_score_internal_wrangled_package_directory_names(self, head=None):
        result = []
        for package_importable_name in self.list_score_internal_wrangled_package_importable_names(head=head):
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result

    def list_score_internal_wrangled_package_importable_names(self, head=None):
        result = []
        for package_importable_name in \
            self.list_score_internal_wrangler_target_package_importable_names(head=head):
            if self.score_internal_wrangler_target_package_importable_name_suffix:
                package_directory_name = self.package_importable_name_to_directory_name(
                    package_importable_name)
                for name in os.listdir(package_directory_name):
                    if name[0].isalpha():
                        result.append('{}.{}'.format(package_importable_name, name))
            else:
                result.append(package_importable_name)
        return result

    def list_score_internal_wrangler_target_directory_names(self, head=None):
        result = []
        for package_importable_name in \
            self.list_score_internal_wrangler_target_package_importable_names(head=head):
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result            

    def list_score_internal_wrangler_target_package_importable_names(self, head=None):
        result = []
        for score_package_short_name in self.list_score_package_short_names(head=head):
            parts = [score_package_short_name]
            if self.score_internal_wrangler_target_package_importable_name_suffix:
                parts.append(self.score_internal_wrangler_target_package_importable_name_suffix)
            score_external_score_package_importable_name = self.dot_join(parts)
            result.append(score_external_score_package_importable_name)
        return result

    def list_wrangled_package_directory_names(self, head=None):
        result = []
        for package_importable_name in self.list_wrangled_package_importable_names(head=head):
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result

    def list_wrangled_package_importable_names(self, head=None):
        if head is None: head = ''
        result, package_importable_names = [], []
        package_importable_names.extend(self.score_external_wrangled_package_importable_names)
        package_importable_names.extend(
            self.list_score_internal_wrangled_package_importable_names(head=head))
        for package_importable_name in package_importable_names:
            if package_importable_name.startswith(head):
                result.append(package_importable_name)
        return result

    def list_wrangled_package_menuing_pairs(self, head=None):
        package_importable_names = self.list_wrangled_package_importable_names(head=head)
        package_spaced_names = self.list_wrangled_package_spaced_names(head=head)
        return zip(package_importable_names, package_spaced_names)

    def list_wrangled_package_proxies(self, head=None):
        result = []
        for package_importable_name in self.list_wrangled_package_importable_names(head=head):
            wrangled_package_proxy = self.get_wrangled_package_proxy(package_importable_name)
            result.append(wrangled_package_proxy)
        return result

    def list_visible_wrangled_package_proxies(self, head=None):
        return self.list_wrangled_package_proxies(head=head)

    def list_wrangled_package_short_names(self, head=None):
        result = []
        for x in self.list_wrangled_package_importable_names(head=head):
            result.append(x.split('.')[-1])
        return result

    def list_visible_wrangled_package_short_names(self, head=None):
        result = []
        for package_proxy in self.list_visible_wrangled_package_proxies(head=head):
            result.append(package_proxy.package_short_name)
        return result

    def list_wrangled_package_spaced_names(self, head=None):
        result = []
        for x in self.list_wrangled_package_short_names(head=head):
            result.append(x.replace('_', ' '))
        return result

    def list_visible_wrangled_package_spaced_names(self, head=None):
        result = []
        for x in self.list_visible_wrangled_package_short_names(head=head):
            result.append(x.replace('_', ' '))
        return result

    def make_wrangled_package(self, package_short_name):
        assert iotools.is_underscore_delimited_lowercase_package_name(package_short_name)
        package_directory_name = os.path.join(self.current_wrangler_target_directory_name, package_short_name)
        os.mkdir(package_directory_name)
        package_proxy = self.get_wrangled_package_proxy(package_short_name)
        package_proxy.fix_package_structure(is_interactive=False)

    def make_wrangled_package_interactively(self):
        self.print_implemented_on_child_classes()

    def profile_visible_wrangled_package_structures(self):
        for package_proxy in self.list_visible_wrangled_package_proxies():
            package_proxy.profile_package_structure()

    def svn_add(self, prompt=True):
        for package_proxy in self.list_visible_wrangled_package_proxies():
            package_proxy.svn_add(prompt=False)
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
        for package_proxy in self.list_visible_wrangled_package_proxies():
            package_proxy.svn_ci(commit_message=commit_message, prompt=False)
        self.proceed(prompt=prompt)

    def svn_st(self, prompt=True):
        for package_proxy in self.list_visible_wrangled_package_proxies():
            package_proxy.svn_st(prompt=False)
        self.proceed(prompt=prompt)

    def svn_up(self, prompt=True):
        for package_proxy in self.list_visible_wrangled_package_proxies():
            package_proxy.svn_up(prompt=False)
        self.proceed(prompt=prompt)

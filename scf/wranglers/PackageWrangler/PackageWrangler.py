from abjad.tools import iotools
from baca.scf.proxies.PackageProxy import PackageProxy
from baca.scf.core.SCFObject import SCFObject
import os


class PackageWrangler(SCFObject):

    def __init__(self, 
        toplevel_wrangler_target_package_importable_name=None, 
        score_resident_wrangled_package_importable_name_infix=None, 
        session=None):
        SCFObject.__init__(self, session=session)
        if toplevel_wrangler_target_package_importable_name is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                toplevel_wrangler_target_package_importable_name)
        if score_resident_wrangled_package_importable_name_infix is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                score_resident_wrangled_package_importable_name_infix)
        self._toplevel_wrangler_target_package_importable_name = \
            toplevel_wrangler_target_package_importable_name
        self._score_resident_wrangled_package_importable_name_infix = \
            score_resident_wrangled_package_importable_name_infix
        self.conditionally_make_empty_package(self.toplevel_wrangler_target_package_importable_name)

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.toplevel_wrangler_target_package_importable_name == \
                other.toplevel_wrangler_target_package_importable_name:
                if self.score_resident_wrangled_package_importable_name_infix == \
                    other.score_resident_wrangled_package_importable_name_infix:
                    return True
        return False

    def __repr__(self):
        body = None
        if self.toplevel_wrangler_target_package_importable_name:
            body = self.toplevel_wrangler_target_package_importable_name.split('.')[-1]
        elif self.score_resident_wrangled_package_importable_name_infix:
            body = self.score_resident_wrangled_package_importable_name_infix.split('.')[-1]
        if body:
            return '{}({!r})'.format(self.class_name, body)
        else:
            return '{}()'.format(self.class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def current_containing_directory_name(self):
        return self.package_importable_name_to_directory_name(
            self.current_containing_package_importable_name)

    @property
    def current_containing_package_importable_name(self):
        if self.session.is_in_score:
            score_package_short_name = self.session.current_score_package_short_name
            return self.dot_join([
                score_package_short_name, self.score_resident_wrangled_package_importable_name_infix])
        else:
            return self.toplevel_wrangler_target_package_importable_name

    @property
    def score_resident_wrangled_package_importable_name_infix(self):
        return self._score_resident_wrangled_package_importable_name_infix

    @property
    def score_resident_wrangled_package_importable_names(self):
        result = []
        for toplevel_score_package_importable_name in self.score_resident_wrangler_target_package_importable_names:
            if self.score_resident_wrangled_package_importable_name_infix:
                toplevel_score_package_directory_name = self.package_importable_name_to_directory_name(
                    toplevel_score_package_importable_name)
                for name in os.listdir(toplevel_score_package_directory_name):
                    if name[0].isalpha():
                        result.append('{}.{}'.format(toplevel_score_package_importable_name, name))
            else:
                result.append(toplevel_score_package_importable_name)
        return result

    @property
    def score_resident_wrangled_package_directory_names(self):
        result = []
        for package_importable_name in self.score_resident_wrangled_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result

    @property
    def score_resident_wrangler_target_package_directory_names(self):
        result = []
        for package_importable_name in self.score_resident_wrangler_target_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result            

    @property
    def score_resident_wrangler_target_package_importable_names(self):
        result = []
        for score_package_short_name in self.score_package_short_names:
            parts = [score_package_short_name]
            if self.score_resident_wrangled_package_importable_name_infix:
                parts.append(self.score_resident_wrangled_package_importable_name_infix)
            toplevel_score_package_importable_name = self.dot_join(parts)
            result.append(toplevel_score_package_importable_name)
        return result

    @property
    def temporary_package_directory_name(self):
        return self.package_importable_name_to_directory_name(self.temporary_package_importable_name)

    @property
    def temporary_package_importable_name(self):
        return '__temporary_package'

    @property
    def toplevel_wrangled_package_directory_names(self):
        result = []
        for package_importable_name in self.toplevel_wrangled_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(package_importable_name))
        return result
        
    @property
    def toplevel_wrangled_package_importable_names(self):
        result = []
        if self.toplevel_wrangler_target_package_importable_name is not None:
            global_package_directory_name = self.package_importable_name_to_directory_name(
                self.toplevel_wrangler_target_package_importable_name)
            for name in os.listdir(global_package_directory_name):
                if name[0].isalpha():
                    result.append('{}.{}'.format(self.toplevel_wrangler_target_package_importable_name, name))
        return result

    @property
    def toplevel_wrangler_target_package_directory_name(self):
        return self.package_importable_name_to_directory_name(
            self.toplevel_wrangler_target_package_importable_name)

    @property
    def toplevel_wrangler_target_package_importable_name(self):
        return self._toplevel_wrangler_target_package_importable_name
    
    @property
    def wrangler_target_package_directory_names(self):
        result = []
        for wrangler_target_package_importable_name in self.wrangler_target_package_importable_names:
            result.append(self.package_importable_name_to_directory_name(wrangler_target_package_importable_name))
        return result

    @property
    def wrangler_target_package_importable_names(self):
        result = [] 
        if self.toplevel_wrangler_target_package_importable_name:
            result.append(self.toplevel_wrangler_target_package_importable_name)
        result.extend(self.score_resident_wrangler_target_package_importable_names)
        return result

    ### PUBLIC METHODS ###
    
    def fix_structure_of_wrangled_packages_to_display(self, prompt=True):
        results = []
        for package_proxy in self.list_wrangled_package_proxies_to_display():
            results.append(package_proxy.fix_package_structure(is_interactive=prompt))
            if prompt:
                package_proxy.profile_package_structure()
        return results

    def get_package_proxy(self, package_importable_name):
        return PackageProxy(package_importable_name, session=self.session)
        
    def list_wrangled_package_importable_names(self, head=None):
        if head is None: head = ''
        result, package_importable_names = [], []
        package_importable_names.extend(self.toplevel_wrangled_package_importable_names)
        package_importable_names.extend(self.score_resident_wrangled_package_importable_names)
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
            wrangled_package_proxy = self.get_package_proxy(package_importable_name)
            result.append(wrangled_package_proxy)
        return result

    def list_wrangled_package_proxies_to_display(self, head=None):
        return self.list_wrangled_package_proxies(head=head)

    def list_wrangled_package_short_names(self, head=None):
        result = []
        for x in self.list_wrangled_package_importable_names(head=head):
            result.append(x.split('.')[-1])
        return result

    def list_wrangled_package_short_names_to_display(self, head=None):
        result = []
        for package_proxy in self.list_wrangled_package_proxies_to_display(head=head):
            result.append(package_proxy.package_short_name)
        return result

    def list_wrangled_package_spaced_names(self, head=None):
        result = []
        for x in self.list_wrangled_package_short_names(head=head):
            result.append(x.replace('_', ' '))
        return result

    def make_package(self, package_short_name):
        assert iotools.is_underscore_delimited_lowercase_package_name(package_short_name)
        package_directory_name = os.path.join(self.current_containing_directory_name, package_short_name)
        os.mkdir(package_directory_name)
        score_package_proxy = self.get_package_proxy(package_short_name)
        score_package_proxy.fix_package_structure(is_interactive=False)

    def make_package_interactively(self):
        self.print_implemented_on_child_classes()

    def profile_visible_package_structures(self):
        for package_proxy in self.list_wrangled_package_proxies_to_display():
            package_proxy.profile_package_structure()

    def svn_add(self, prompt=True):
        for package_proxy in self.list_wrangled_package_proxies_to_display():
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
        for package_proxy in self.list_wrangled_package_proxies_to_display():
            package_proxy.svn_ci(commit_message=commit_message, prompt=False)
        self.proceed(prompt=prompt)

    def svn_st(self, prompt=True):
        for package_proxy in self.list_wrangled_package_proxies_to_display():
            package_proxy.svn_st(prompt=False)
        self.proceed(prompt=prompt)

    def svn_up(self, prompt=True):
        for package_proxy in self.list_wrangled_package_proxies_to_display():
            package_proxy.svn_up(prompt=False)
        self.proceed(prompt=prompt)

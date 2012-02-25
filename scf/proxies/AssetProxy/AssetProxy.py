from scf.core.SCFObject import SCFObject
import os
import subprocess


class AssetProxy(SCFObject):

    def __init__(self, path_name=None, session=None):
        assert isinstance(path_name, (str, type(None)))
        SCFObject.__init__(self, session=session)
        self._path_name = path_name

    ### CLASS ATTRIBUTES ###

    generic_class_name = 'asset'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def plural_generic_class_name(self):
        return self.pluralize_string(self.generic_class_name)

    @property
    def human_readable_name(self):
        return self.short_name

    @property
    def is_in_repository(self):
        if self.path_name is None:
            return False
        command = 'svn st {}'.format(self.path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        first_line = proc.stdout.readline()
        if first_line.startswith(('?', 'svn: warning:')):
            return False
        else:
            return True
        
    @property
    def path_name(self):
        return self._path_name

    @property
    def parent_directory_name(self):
        return os.path.dirname(self.path_name)

    @property
    def short_name(self):
        return self.path_name.split(os.path.sep)[-1]

    @property
    def short_name_without_extension(self):
        if '.' in self.short_name:
            return self.short_name[:self.short_name.rdindex('.')]
        else:
            return self.short_name

    @property
    def svn_add_command(self):
        return 'svn add {}'.format(self.path_name)

    ### PUBLIC METHODS ###

    def fix(self):
        self.print_implemented_on_child_classes()

    def rename(self, new_path_name, is_interactive=False):
        if self.is_in_repository:
            self.rename_versioned_asset(new_path_name, is_interactive=is_interactive)
        else:
            self.rename_nonversioned_asset(new_path_name, is_interactive=is_interactive)

    def rename_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_file_name_with_extension('new file name')
        getter.include_newlines = False
        result = getter.run()
        if self.backtrack():
            return
        new_path_name = os.path.join(self.parent_directory_name, result)
        self.display('new path name will be: "{}"\n'.format(new_path_name))
        if not self.confirm():
            return
        self.rename(new_path_name, is_interactive=True)

    # TODO: write test
    def rename_nonversioned_asset(self, new_path_name, is_interactive=False):
        command = 'mv {} {}'.format(self.path_name, new_path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        if is_interactive:
            lines = []
            lines.append('renamed {}.'.format(self.path_name))
            lines.append('')
            self.display(lines)
        self.proceed(prompt=is_interactive)

    # TODO: write test
    def rename_versioned_asset(self, new_path_name, is_interactive=False):
        command = 'svn --force mv {} {}'.format(self.path_name, new_path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        if is_interactive:
            lines = []
            lines.append('renamed {}.'.format(self.path_name))
            lines.append('')
            self.display(lines)
        self.proceed(prompt=is_interactive)

    def remove(self, is_interactive=False):
        if self.is_in_repository:
            result = self.remove_versioned_asset(is_interactive=is_interactive)
        else:
            result = self.remove_nonversioned_asset(is_interactive=is_interactive)
        return result

    def remove_nonversioned_asset(self, is_interactive=False):
        if is_interactive:
            line = '{} will be removed.\n'.format(self.path_name)
            self.display(line)
            getter = self.make_getter(where=self.where())
            getter.append_string("type 'remove' to proceed")
            response = getter.run()
            if self.backtrack():
                return
        if not is_interactive or response == 'remove':
            command = 'rm -rf {}'.format(self.path_name)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            proc.stdout.readline()
            if is_interactive:
                line = 'removed {}.\n'.format(self.path_name)
                self.display(line)
            return True
        return False

    def remove_versioned_asset(self, is_interactive=False):
        if is_interactive:
            line = '{} will be completely removed from the repository!\n'.format(self.path_name)
            self.display(line)
            getter = self.make_getter(where=self.where())
            getter.append_string("type 'remove' to proceed")
            response = getter.run()
            if self.backtrack():
                return
        if not is_interactive or response == 'remove':
            command = 'svn --force rm {}'.format(self.path_name)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.stdout.readline()
            if is_interactive:
                lines = []
                lines.append('removed {}.\n'.format(self.path_name))
                lines.append('(Subversion will cause empty package to remain visible until next commit.)')
                lines.append('')
                self.display(lines)
            return True
        return False

    def run(self, cache=False, clear=True, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.backtrack(source=self.backtracking_source):
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack(source=self.backtracking_source):
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def run_py_test(self, prompt=True):
        proc = subprocess.Popen('py.test {}'.format(self.path_name), shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.display(lines)
        line = 'tests run.'
        self.proceed(line, prompt=prompt)

    def svn_add(self, is_interactive=False):
        self.display(self.path_name)
        proc = subprocess.Popen(self.svn_add_command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(prompt=is_interactive)

    def svn_ci(self, commit_message=None, is_interactive=True):
        if commit_message is None:
            getter = self.make_getter(where=self.where())
            getter.append_string('commit message')
            commit_message = getter.run()
            if self.backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self.display(line)
            if not self.confirm():
                return
        lines = []
        lines.append(self.path_name)
        command = 'svn commit -m "{}" {}'.format(commit_message, self.path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines.extend([line.strip() for line in proc.stdout.readlines()])
        lines.append('')
        self.display(lines)
        self.proceed(prompt=is_interactive)

    def svn_st(self, is_interactive=True):
        if is_interactive:
            self.display(self.path_name)
        command = 'svn st -u {}'.format(self.path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(prompt=is_interactive)

    def svn_up(self, is_interactive=True):
        if is_interactive:
            self.display(self.path_name)
        command = 'svn up {}'.format(self.path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(prompt=is_interactive)

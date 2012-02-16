from baca.scf.core.SCFObject import SCFObject
import os
import subprocess


class AssetProxy(SCFObject):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def human_readable_name(self):
        return self.short_name
        
    @property
    def path_name(self):
        self.print_implemented_on_child_classes()

    @property
    def short_name(self):
        return self.path_name.split(os.path.sep)[-1]

    @property
    def svn_add_command(self):
        return 'svn add {}'.format(self.path_name)

    ### PUBLIC METHODS ###

    def fix(self):
        self.print_implemented_on_child_classes()

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

    def svn_add(self, prompt=False):
        self.display(self.path_name)
        proc = subprocess.Popen(self.svn_add_command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(prompt=prompt)

    def svn_ci(self, commit_message=None, prompt=True):
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
        lines.append('')
        lines.append(self.path_name)
        command = 'svn commit -m "{}" {}'.format(commit_message, self.path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines.extend([line.strip() for line in proc.stdout.readlines()])
        self.display(lines)
        self.proceed(prompt=prompt)

    def svn_st(self, prompt=True):
        self.display(self.path_name)
        command = 'svn st -u {}'.format(self.path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(prompt=prompt)

    def svn_up(self, prompt=True):
        self.display(self.path_name)
        command = 'svn up {}'.format(self.path_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(prompt=prompt)

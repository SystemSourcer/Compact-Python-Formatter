# Imports
import io
import re
import json
import tokenize
from pathlib import Path 
from datetime import datetime
# Functions
def main():
    copyfo = CompactPythonFormatter()
    copyfo.format_code()

# Objects
class CompactPythonFormatter:
    def __init__(self, config_path='./cpf_config.json', code_loc='./', set_conf=True):
        self.default_config_path = './cpf_config.json'
        self.default_config = {'structure_imports':True, 'unindent_imports':True, 'sort_imports':True, 'structure_functions':True, 'structure_objects':True, 'structure_globals':True, 'rm_vspace':True, 'indent_vspace':True, 'rm_hspace':True, 'equal_space':True,
                      'equal_brack_space':False, 'docstring':True, 'each_line_comment':True, 'compress_if_else':True,' max_line_len':None, 'backup':True}

        self.config_path = Path(config_path) # Ensure that it is a path object
        self.code_loc = Path(code_loc) # Ensure that it is a path object
        if set_conf: self.set_config()
        # Load config
        with self.config_path.open("r", encoding="utf-8") as config_file:
            config = json.load(config_file)

        for key, value in config.items():
            setattr(self, key, value)

        # Check and load code list
        if self.code_loc.is_file() and self.code_loc.suffix == '.py': self.code_path_list = [self.code_loc]
        elif self.code_loc.is_dir(): 
            self.code_path_list = list(self.code_loc.rglob('*.py'))
            if not self.code_path_list: ValueError("No python file in directory.")

        else: raise FileNotFoundError(f'"{self.code_loc}" is neither a file nor a directory.')

    def set_config(self):
        """
        Of course, the config file can also be created or edited manually.\n 
        However, please note that in this case, the values in the file will not be checked and errors may occur during execution.
        """
        print(f'\033[92mSet or update config in file \033[93m"{self.config_path}"\033[92m.\033[0m')
        if self.config_path.is_file(): 
            with self.config_path.open("r", encoding="utf-8") as config_file: 
                config = json.load(config_file)

            if 'edit' in config: del config['edit']
            if set(config) != set(self.default_config):
                print(f'\033[91mThe config file \033[93m"{self.config_path}"\033[91m does not have the right / up to date keys. \033[0m')
                print(f'\033[93mUsing default config \033[92m"{self.default_config}"\033[0m')
                config = self.default_config

        else:
            print(f'\033[91mThe config file \033[93m"{self.config_path}"\033[91m cloud not be found.\033[0m')
            print(f'\033[93mUsing default file path \033[92m"{self.default_config_path}"\033[0m')
            self.config_path = Path(self.default_config_path)
            config = self.default_config

        for key, value in config.items():
            while True:
                new_value = input(f'\033[94mEnter bool value for key \033[92m{key}\033[94m. Default / current value is \033[93m{value}\033[94m. To keep default / current just type nothing and press enter:\n\033[0m').strip().lower()
                if new_value == '': break
                elif new_value in ('true', 't', 'yes', 'y', 'ja', '1'): 
                    config[key] = True
                    break

                elif new_value in ('false', 'f', 'no', 'n', 'nein', '0'): 
                    config[key] = False
                    break

                else: print('\033[91mPleasse type "true", "t", "yes", "y", "ja", "1"; "false", "f", "no", "n", "nein", "0" or just press enter for the defualt / current value.\033[0m')

        config['edit'] = datetime.now().isoformat(timespec='seconds')
        with self.config_path.open("w", encoding="utf-8") as config_file: 
                json.dump(config,config_file,indent=4)

    def read_code(self,code_path):
        try:
            with open(code_path, "r", encoding="utf-8") as code_file:
                original_code = code_file.readlines()
                no_tab_code = [line.replace("\t", " ") for line in original_code]

            return no_tab_code

        except FileNotFoundError:
            print(f"Error: File '{code_path}' not found.")
            raise

        except IOError as e:
            print(f"Error reading file '{code_path}': {e}")
            raise

    def structure_code(self,code):
        import_line_list = ['# Imports\n']
        function_line_list = ['# Functions\n']
        object_line_list = ['# Objects\n']
        global_line_list = ["# Global\nif __name__ == '__main__':\n"]
        line_idx = - 1
        for idx, line in enumerate(code):
             if re.match(r"^\s*if\s+__name__\s*==\s*'__main__':", line): line_idx = idx

        if line_idx != - 1: code = [line if i < line_idx else line.lstrip() for i, line in enumerate(code)]
        # do imports
        import_idx_set = set()
        import_idx = 0
        while import_idx < len(code):
            line = code[import_idx]
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            if indent > 0 and not self.unindent_imports: 
                import_idx += 1
                continue

            match = re.search(r'\bimport\b', line)
            if match and '#' not in line[:match.start()]: 
                import_line_list.append(line.lstrip())
                import_idx_set.add(import_idx)

            import_idx += 1

        if self.sort_imports: import_line_list = sorted(import_line_list, key=lambda x: (len(x), x)) # First len if len is equal then alphabetic
        code_no_import = [line for idx, line in enumerate(code) if idx not in import_idx_set and line not in {'# Imports\n', '# Functions\n', '# Objects\n', '# Global\n', "if __name__ == '__main__':\n"}]
        # do functions
        function_idx_set = set()
        function_idx = 0
        while function_idx < len(code):
            line = code[function_idx]
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            if stripped.startswith('def ') and indent == 0:
                start = function_idx
                function_idx += 1
                while function_idx < len(code):
                    next_line = code[function_idx]
                    if next_line.strip() == '':
                        function_idx += 1
                        continue

                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent > 0:
                        function_idx += 1

                    else:
                        break

                end = function_idx
                function_line_list.extend(code[start:end])
                function_idx_set.update(range(start, end))

            else:
                function_idx += 1

        if self.unindent_imports: function_line_list = [line for line in function_line_list if line.lstrip() not in import_line_list] # here line instead of index is no problem because repeted imports are ok / good to remove
        code_no_import_func = [line for idx, line in enumerate(code) if idx not in set().union(import_idx_set, function_idx_set) and line not in {'# Imports\n', '# Functions\n', '# Objects\n', '# Global\n', "if __name__ == '__main__':\n"}]
        # do objects
        object_idx_set = set()
        object_idx = 0
        while object_idx < len(code):
            line = code[object_idx]
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            if stripped.startswith('class ') and indent == 0:
                start = object_idx
                object_idx += 1
                while object_idx < len(code):
                    next_line = code[object_idx]
                    if next_line.strip() == '':
                        object_idx += 1
                        continue

                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent > 0:
                        object_idx += 1

                    else:
                        break

                end = object_idx
                object_line_list.extend(code[start:end])
                object_idx_set.update(range(start, end))

            else:
                object_idx += 1

        if self.unindent_imports: object_line_list = [line for line in object_line_list if line.lstrip() not in import_line_list] # here line instead of index is no problem because repeted imports are ok / good to remove
        code_no_import_obj = [line for idx, line in enumerate(code) if idx not in set().union(import_idx_set, object_idx_set) and line not in {'# Imports\n', '# Functions\n', '# Objects\n', '# Global\n', "if __name__ == '__main__':\n", "if __name__=='__main__':\n"}]
        # do globals
        code_global = [line for idx, line in enumerate(code) if idx not in set().union(import_idx_set, function_idx_set, object_idx_set) and line not in {'# Imports\n', '# Functions\n', '# Objects\n', '# Global\n', "if __name__ == '__main__':\n", "if __name__=='__main__':\n"}] # = code_no_import_func_obj, all what remains here in code should be global...
        code_no_global = [line for idx, line in enumerate(code) if idx in set().union(import_idx_set, function_idx_set, object_idx_set)]
        code_no_import_global = [line for idx, line in enumerate(code) if idx in set().union(function_idx_set, object_idx_set)]
        global_line_list.extend([' '+' '+' '+' '+line.lstrip() for line in code_global]) 
        if self.structure_functions and self.structure_globals: new_code = import_line_list + function_line_list + object_line_list + global_line_list
        elif self.structure_functions and self.structure_objects and not self.structure_globals: new_code = import_line_list + function_line_list + object_line_list + code_global
        elif self.structure_functions and not self.structure_objects and not self.structure_globals: new_code = import_line_list + function_line_list + code_no_import_func
        elif not self.structure_functions and self.structure_objects and self.structure_globals: new_code = import_line_list + object_line_list + function_line_list + global_line_list
        elif not self.structure_functions and self.structure_objects and not self.structure_globals: new_code = import_line_list + object_line_list + code_no_import_obj
        elif self.structure_imports and not self.structure_functions and not self.structure_objects and self.structure_globals: new_code = import_line_list + code_no_import_global + global_line_list
        elif self.structure_imports and not self.structure_functions and not self.structure_objects and not self.structure_globals: new_code = import_line_list + code_no_import
        elif not self.structure_imports and not self.structure_functions and not self.structure_objects and self.structure_globals: new_code = code_no_global + global_line_list
        elif not self.structure_imports and not self.structure_functions and not self.structure_objects and not self.structure_globals:new_code = code
        return new_code

    def hspace_line(self,line):
        indent = len(line) - len(line.lstrip(' '))
        new_line = line[:indent] + re.sub(r' +', ' ', line[indent:])
        return new_line

    def space_code(self,code):
        if self.rm_vspace: code = [line for line in code if line.strip() != '']
        if self.indent_vspace: 
            idx_list = [idx for idx, line in enumerate(code[:-1]) if len(line) - len(line.lstrip()) > len(code[idx+1]) - len(code[idx+1].lstrip())]
            reverse_idx_list = sorted(idx_list,reverse=True)
            for idx in reverse_idx_list: code.insert(idx+1,'\n') 

        if self.rm_hspace: code = [self.hspace_line(line) for line in code]
        in_string = False
        brack_level = 0
        for idx, line in enumerate(code):
            i = 0
            while i < len(line):
                space = self.equal_space if brack_level == 0 else self.equal_brack_space
                c = line[i]
                c2 = line[i:i + 2]
                c3 = line[i:i + 3]
                if c3 in ('"""',"'''"): i += 3
                elif c2 in ('\"',"\'"): i += 2
                elif not in_string:
                    if c in ('"',"'"):
                        in_string = True
                        string_char = c
                        i += 1

                    elif c == '(':
                        brack_level += 1
                        i += 1

                    elif c == ')':
                        brack_level -= 1
                        i += 1

                    elif space:
                        if c3 in ('**=', '//=', '>>=', '<<='):
                            line = line[:i] + f' {c3} ' + line[i + 3:]
                            i += 5

                        elif c2 in ('+=', '-=', '*=', '/=', '%=', '==', '>=', '<=', '!='):
                            line = line[:i] + f' {c2} ' + line[i + 2:]
                            i += 4 

                        elif c in ('+', '-', '*', '/', '=', '%', '>', '<'):
                            line = line[:i] + f' {c} ' + line[i + 1:]
                            i += 3 

                        else: i += 1

                    else:
                        if c2 in (' +', '+ ', ' -', '- ', ' *', '* ', ' /', '/ ', ' =','= ', ' %', '% ', ' >', '> ', ' <', '< ', ' !'):
                            line = line[:i] + c2.strip(' ') + line[i + 2:]

                        else: i += 1 

                elif in_string:
                    if c == string_char: 
                        in_string = False
                        string_char = None
                        i += 1

                    else: i += 1

            code[idx] = self.hspace_line(line)

        return code

    def comment_code(self,code):
        pass

    def compress_code(self,code):
        pass

    def backup_code(self,code,code_path):
        if self.backup: 
            backup_path = code_path.with_suffix('.backup')
            with backup_path.open('w', encoding='utf-8') as backup_file:
                backup_file.writelines(code)

            print(f'\033[92m Original code is backuped.\033[0m')

        else: 
            print('\033[91m No bbackup will be saved.\033[0m')

    def write_code(self, code, code_path):
        print(f'\033[94mFormatted code of \033[92m{code_path}\033[94m will look like:\n\033[93m'+''.join(code)+'\033[0m') 
        if input('Type "yw" to write formatted code:\n') == 'yw': 
            with code_path.open('w', encoding='utf-8') as code_file:
                code_file.writelines(code)

            print('\033[92m Formatted code is written.\033[0m')

        else: 
            print('\033[91m Formatted code is not written.\033[0m')

    def format_code(self):
        print(f'All of the following code will be prcessed iterative:\n{self.code_path_list}')
        for code_path in self.code_path_list:
            code = self.read_code(code_path)
            self.backup_code(code, code_path)
            code = self.structure_code(code)
            code = self.space_code(code)
            self.write_code(code, code_path)

# Global
if __name__ == '__main__':
    main()
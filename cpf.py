from pathlib import Path
import json
from datetime import datetime
def main():
    copyfo = CompactPythonFormatter()
    copyfo.format_code()
    
class CompactPythonFormatter:
    def __init__(self, config_path='./cpf_config.json', code_loc = './'):
        self.config_path = Path(config_path) # Ensure that it is a path object
        self.code_loc = Path(code_loc) # Ensure that it is a path object
        # Load config
        if not self.config_path.is_file():
            print(f'\033[91mThe config file \033[93m"{self.config_path}"\033[91m cloud not be found.\033[0m')
            self.config_path = Path('./cpf_config.json')
            self.set_config()  
        with self.config_path.open("r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        for key, value in config.items():
            setattr(self, key, value)
        # Load list of file to format
        if self.code_loc.is_file() and code_loc.suffix == '.py': self.code_path_list=[code_loc]
        elif self.code_loc.is_dir(): 
            self.code_path_list = list(self.code_loc.rglob('*.py'))
            if not self.code_path_list: ValueError("No python file in directory.")
        else: raise FileNotFoundError(f'"{code_loc}" is neither a file nor a directory.')
        
    def set_config(self):
        """
        Of course, the config file can also be created or edited manually.\n 
        However, please note that in this case, the values in the file will not be checked and errors may occur during execution.
        """
        print(f'\033[92mSet or update config in file \033[93m"{self.config_path}"\033[92m.\033[0m')
        if self.config_path.is_file(): 
            with self.config_path.open("r", encoding="utf-8") as config_file: 
                config = json.load(config_file)
                if 'edit' in  config: del config['edit']
        else:
            config = {'sort_imports':True,
                      'structure':True,
                      'docstring':True,
                      'clear_all_space':True,
                      'indent_end_space':True,
                      'rm_double_space':True,
                      'no_equal_param_space':True,
                      'no_equal_def_space':True,
                      'each_line_comment':True,
                      'pretty_comment':True,
                      'singel_qmark':True,
                      'compress_if_else':True,
                      }
        for key, value in config.items():
            while True:
                new_value = input(f'\033[94mEnter bool value for key \033[92m{key}\033[94m. Default / current value is \033[93m{value}\033[94m. To keep default / current just type nothing and press enter:\n\033[0m').strip().lower()
                if new_value == '': break
                elif value in ('true', 't', 'yes', 'y', 'ja', '1'): config[key] = True
                elif value in ('false', 'f', 'no', 'n', 'nein', '0'): config[key] = False
                
                print('\033[91mPleasse type "true", "t", "yes", "y", "ja", "1"; "false", "f", "no", "n", "nein", "0" or just press enter for the defualt / current value.\033[0m')

        config['edit'] = datetime.now().isoformat(timespec='seconds')
        with self.config_path.open("w", encoding="utf-8") as config_file: 
                json.dump(config,config_file,indent=4)

    def read_code(self,code_path):
        try:
            with open(code_path, "r", encoding="utf-8") as code_file:
                content = code_file.readlines()
            return content
        except FileNotFoundError:
            print(f"Error: File '{code_path}' not found.")
            raise
        except IOError as e:
            print(f"Error reading file '{code_path}': {e}")
            raise

    def structure_code(self,code):
        pass

    def space_code(self,code):
        pass

    def comment_code(self,code):
        pass
    
    def string_code(self,code):
        pass

    def compress_code(self,code):
        pass

    def write_code(self, code_path, code):

        print('\033[94mFormatted code will look like:\n\033[93m'+''.join(code) + '\033[0m')   
        
        if input('Type "yw" to write formatted code:\n') == 'yw': 
            with code_path.open('w', encoding='utf-8') as code_file:
                code_file.writelines(code)
            print('\033[92m Formatted code is written.\033[0m')
        else: 
            print('\033[91m Formatted code is not written.\033[0m')
            

        
    def format_code(self):
        for code_path in self.code_path_list:
            code = self.read_code(code_path)



            self.write_code(code_path,code)


if __name__ == '__main__':
    main()
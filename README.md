# Compact-Python-Formatter
Compact Python Formatter (CPF) formats Python code in a highly compact and readable way, following a custom style guide instead of PEP8. CPF is ideal for users who prefer concise, clear code layouts—perfect for scripting, minified source, or personal preferences. It is not PEP8 but it is compact and clean :)


## Features

CPF is a Python code formatter that prioritizes compactness and readability using a custom style guide—offering an alternative to formatting standards like PEP8.


- Formats Python code with maximal compactness while ensuring clarity

- Can also sort imports aswell as add comments for the structure and docstrings

- Fast and easy to use as a CLI tool 

- Customizable via json file for personal or project-specific layouts

- Suitable for scripting, minified source, or personal code style preferences


## Installation 

Colne the repository or just download the cpf.py file.


## Usage

Import and inegrate it in your python code or ese it directly via CLI:
```bash
python cgp.py
``` 

## Example

To be written...

## Configuration

CPF can be customized using a configuration file (cpf-config.json).

Configurable options:
- "structure_imports": Should the global imports be grouped together at the beginning (true or false)
- "unindent_imports":  Sholud the not global imports be made global (true or false)
- "sort_imports": Sholud the imports be sorted (true or false)
- "structure_functions": Should the global functions be grouped together after the Imports. Sets structure_imports internally to true (true or false)
- "structure_objects": Should the global classes / obbjects be grouped together. Sets structure_imports internally to true (true or false)
- "structure_globals": Sholud all globbal lines which are nor import, comment structure, functions or objects be groupt togehter at the end under "if __name__ == '__main__':" (true or false)
- "rm_vspace": Sholud all empty lines be removed (true or false)
- "indent_vspace": Shuold an empy line be inserted after an indent ends (true or false)
- "rm_hspace": Sholud multible spaces be reduced (true or false)
- "equal_space": Shloud be spaces before and after opertators. (true or false)
- "equal_brack_space": Sholud be spaces befor and after operators inside brackets (true or false)
- "docstring": Should docstrings be created at the beginning of classes and functions? (true or false)
- "each_line_comment": Sholud # be added at the end of all lines which do not end inside bracklets (true or false)
- "max_line_len": Shloud line be breaked after a specific length (null or Integer value)
- "backup": Should a backup file be created before formatting? (true or false)

Additional options planned for the future:
- Compressing if else and loops as far as possible

## Why not PEP8?

PEP8 requires extensive whitespace, newlines, and indentation, which can significantly increase the number of lines and the overall size of the code.
The additional whitespace and spacing can make it harder to fit code on a single screen, especially for compact logic or scripts, reducing visibility of the overall program structure.
PEP8 is intentionally generic and cannot accommodate personal or project-specific preferences focused on compactness or alternative readable layouts.
CPF is designed for those who prefer extremely concise code layouts for personal, scripting, or minification needs, rather than classical PEP8 formatting.

## License

MIT License

See [LICENSE](LICENSE) for more information.

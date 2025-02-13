import py_compile
import os


syntax_checkers = {
    ".py": lambda file_path: py_compile.compile(file_path, doraise=True)#,
    #".php": lambda file_path: run_command(f"php -l {file_path}", os.path.dirname(file_path)),
    #".java": lambda file_path: run_command(f"javac -Xlint {file_path}", os.path.dirname(file_path)),
    #".c": lambda file_path: run_command(f"gcc -fsyntax-only {file_path}", os.path.dirname(file_path)),
    #".cpp": lambda file_path: run_command(f"g++ -fsyntax-only {file_path}", os.path.dirname(file_path)),
    #".js": lambda file_path: run_command(f"jshint {file_path}", os.path.dirname(file_path))'''
}

def check_syntax(directory):
        """Goes through all files in the directory and checks their syntax by trying to compile it or run language-specific syntax linters (as specified in syntax_checkers).

        Args:
            directory (str): The specified commit.


        Returns:
            Nothing. Raises an exception if a syntax error is found
        """

for root, dirs, files in os.walk(directory):

        for file in files:
            file_path = os.path.join(root, file)

            try:
                extension = os.path.splitext(file_path)[1].lower()
                checker = syntax_checkers.get(extension)

                if checker:
                    checker(file_path)

            except Exception as e:
                raise Exception(f"check_syntax: Syntax error in {file_path}: {e}")






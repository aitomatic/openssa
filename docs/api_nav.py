import os


DOCS_DIR = '.'
SRC_DIR = '../openssm'
API_DIR = './openssm'
NAV_PATH = '/tmp/api_nav.yml'
MKDOCS_INC_PATH = DOCS_DIR + '/mkdocs.yml.inc'
MKDOCS_PATH = DOCS_DIR + '/../mkdocs.yml'

INDENT_SPACES = 2
MODULE_PATH_PREFIX = 'openssm/'
EXCLUDES = ('deprecated', '__pycache__', '__init__.py')
EMPTY_MD = 'empty.md'


def main(nav_path, src_dir, api_dir, indent_spaces, mkdocs_inc_path, mkdocs_path):
    clean_api_directory(api_dir)
    generate_mkdocs_config(nav_path, src_dir, api_dir, indent_spaces)
    make_mkdocs_file(mkdocs_inc_path, nav_path, mkdocs_path)


def make_mkdocs_file(mkdocs_inc_path, nav_path, mkdocs_path):
    # Concatenate MKDOCS_INC_PATH with NAV_PATH and write to MKDOCS_PATH
    # print(f'mkdocs_inc_path: {mkdocs_inc_path}')
    with open(mkdocs_inc_path, 'r') as mkdocs_inc_file:
        mkdocs_inc_content = mkdocs_inc_file.read()

    with open(nav_path, 'r') as nav_file:
        nav_content = nav_file.read()

    # print(f'mkdocs_path: {mkdocs_path}')
    with open(mkdocs_path, 'w') as mkdocs_file:
        mkdocs_file.write(mkdocs_inc_content + '\n' + nav_content)


def clean_api_directory(api_dir):
    if os.path.exists(api_dir):
        os.system(f'rm -r {api_dir}')
    os.makedirs(api_dir, exist_ok=True)


def is_dir_empty(src_dir):
    for entry in os.scandir(src_dir):
        if entry.is_dir() and not entry.name.endswith('__pycache__'):
            return False

        if entry.is_file() and entry.name.endswith('.py') and not entry.name.endswith('__init__.py'):
            return False

    return True


def is_excluded(path):
    for name in EXCLUDES:
        if path.endswith(name):
            return True

    return False


def generate_mkdocs_config(nav_path, src_dir, api_dir, indent_spaces):
    with open(nav_path, 'w') as nav_file:
        nav_file.truncate()  # to be sure
        for root, dirs, files in os.walk(src_dir):
            indent = ' ' * (root.count(os.sep) * indent_spaces + indent_spaces)

            if is_excluded(root):
                continue

            if is_dir_empty(root):
                indent = ' ' * (root.count(os.sep) * indent_spaces + indent_spaces)
                module_name = os.path.basename(root)
                # Create a new empty .md file for this directory
                empty_md_dir = os.path.join(api_dir, root.replace(src_dir, '').lstrip('/'))
                os.makedirs(empty_md_dir, exist_ok=True)  # create necessary directories
                empty_md_path = os.path.join(empty_md_dir, 'EMPTY.md')
                with open(empty_md_path, 'w') as empty_md_file:
                    empty_md_file.write("This directory is (still) empty.\n")
                nav_file.write(f'{indent}- {module_name}: openssm/{empty_md_path.replace(api_dir+"/", "")}\n')


            else:
                indent = ' ' * (root.count(os.sep) * indent_spaces + indent_spaces)
                module_name = os.path.basename(root)
                nav_file.write(f'{indent}- {module_name}:\n')
                for file in files:
                    if file.endswith('.py') and not is_excluded(file):
                        generate_api_reference(root.replace(src_dir, '').lstrip('/'), file, api_dir)
                        module_path = os.path.join(root.replace(src_dir, '').lstrip('/'), file.replace('.py', ''))
                        nav_file.write(
                                f'{indent + " " * indent_spaces}- {file.replace(".py", "")}: '
                                f'openssm/{module_path.replace(".py", ".md")}.md\n')


def generate_api_reference(root, file, api_dir):
    module_path = os.path.join(root, file)
    module_name = MODULE_PATH_PREFIX.replace("/", ".") + module_path.replace("/", ".").replace(".py", "")

    md_file_dir = os.path.join(api_dir, os.path.dirname(module_path))
    md_file_name = f'{os.path.basename(module_path).replace(".py", ".md")}'
    md_file_path = os.path.join(md_file_dir, md_file_name)

    os.makedirs(md_file_dir, exist_ok=True)

    with open(md_file_path, 'w') as md_file:
        md_file.write(f'::: {module_name}\n')


if __name__ == "__main__":
    main(NAV_PATH, SRC_DIR, API_DIR, INDENT_SPACES, MKDOCS_INC_PATH, MKDOCS_PATH)


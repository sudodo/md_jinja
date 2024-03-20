import os
import yaml
from jinja2 import Template
import argparse
import re


def find_template_variables(template_content):
    # Regex to find Jinja2 placeholders (e.g., {{ var }})
    pattern = r'\{\{ *([a-zA-Z0-9_]+) *\}\}'
    return set(re.findall(pattern, template_content))

def include_external_files(template_content: str, template_path: str) -> str:
    """
    Search for special syntax {{{ /path/to/file }}} in the template content
    and replace it with the content of the specified file.

    Args:
        template_content (str): The content of the template being processed.
        template_path (str): The path to the template file being processed.

    Returns:
        str: The template content with included files content.
    """
    template_dir = os.path.dirname(template_path)
    pattern = r'\{\{\{ *(.*?) *\}\}\}'  # Regex to find {{{ path/to/file }}}

    def replace_with_file_content(match):
        file_path = match.group(1)
        # Compute the absolute path if the file_path is relative
        absolute_file_path = os.path.join(template_dir, file_path)
        try:
            with open(absolute_file_path, 'r') as file:
                file_content = file.read()
                # Recursively include external files in the included file content
                file_content = include_external_files(file_content, absolute_file_path)
                return file_content
        except FileNotFoundError:
            raise FileNotFoundError(f"Included file not found: {absolute_file_path}")

    return re.sub(pattern, replace_with_file_content, template_content)

def render_template(template_path, variables):
    """
    Render a Jinja2 template with the given variables.

    This function reads a template file from the specified path, processes it for
    external file inclusions, checks for undefined variables, and finally renders
    the template with the provided variables. It supports the inclusion of external
    files within the template using a special syntax {{{ path/to/file }}}. The paths
    can be relative to the template's directory or absolute. If a variable used in
    the template is not provided in the `variables` dictionary, a warning is printed.

    Args:
        template_path (str): The path to the Jinja2 template file. This path can be
            either absolute or relative to the current working directory.
        variables (dict): A dictionary of variables to be used for rendering the
            template. The keys should match the variable names used within the
            template.

    Returns:
        str: The rendered template as a string.

    Raises:
        FileNotFoundError: If the template file or any included file specified in the
            template does not exist.

    Example:
        Given a template file located at './templates/my_template.md' with the following content:

        ```md
        # {{ title }}
        Welcome to our site.
        {{ body }}
        Thank you for visiting.
        ```

        And using the following Python code to render this template:

        ```python
        variables = {'title': 'My Title', 'body': 'This is the body.'}
        rendered_content = render_template('./templates/my_template.md', variables)
        print(rendered_content)
        ```

        The output will be:

        ```md
        # My Title
        Welcome to our site.
        This is the body.
        Thank you for visiting.
        ```
    Note:
    - The function will print a warning to the standard output if there are
    variables in the template that are not provided in the `variables` dict.
    - The special syntax for including external files ({{{ path/to/file }}}) allows
    for flexible template composition. Ensure that included paths are correct
    relative to the template's directory or are valid absolute paths.
    """
    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Process file inclusions
    template_content = include_external_files(template_content, template_path)

    # Find variables used in the template
    template_vars = find_template_variables(template_content)

    # Warn if any template variable is not defined in YAML variables
    undefined_vars = template_vars - variables.keys()
    if undefined_vars:
        print(f"Warning: Undefined variables in {template_path}: {', '.join(undefined_vars)}")

    template = Template(template_content)
    return template.render(variables)

def process_directory(input_dir, output_dir, variables):
    """
    Process all Markdown files in a given directory, including its subdirectories,
    and render them using the provided variables. The rendered files are saved in
    a corresponding structure in the output directory.

    Args:
        input_dir (str): The path to the directory containing Markdown template files.
        output_dir (str): The path to the directory where rendered files will be saved.
        variables (dict): A dictionary containing variables for rendering the templates.

    This function walks through the input directory, processes each Markdown file
    found, and saves the rendered content in the output directory while preserving
    the directory structure.
    """
    # TODO: This method is not tested. Instead, I added inline comments to explain what it does. Build a test case based on these comments.
    for root, dirs, files in os.walk(input_dir):
        # Determine the relative path from the input directory to the current directory
        # This relative path is used to maintain the same directory structure in the output
        rel_path = os.path.relpath(root, input_dir)

        # Construct the corresponding output path
        output_root = os.path.join(output_dir, rel_path)

        # Ensure the output directory exists, creating it if necessary
        os.makedirs(output_root, exist_ok=True)

        # Process each Markdown file in the current directory
        for file in files:
            if file.endswith('.md') or file.endswith('.yaml') or file.endswith('.yml'):
                # Construct the full paths for the input and output files
                template_path = os.path.join(root, file)
                output_path = os.path.join(output_root, file)

                # Render the template with the provided variables
                rendered_content = render_template(template_path, variables)

                # Write the rendered content to the corresponding file in the output directory
                with open(output_path, 'w') as output_file:
                    output_file.write(rendered_content)

def load_variables(variable_dirs):
    variables = {}
    for var_dir in variable_dirs:
        if var_dir:  # Check to avoid empty strings
            for root, _, files in os.walk(var_dir):
                for file in files:
                    if file.endswith('.yaml') or file.endswith('.yml'):
                        with open(os.path.join(root, file), 'r') as yaml_file:
                            variables.update(yaml.safe_load(yaml_file))
    return variables

def is_directory(path):
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Provided path is not a directory: {path}")

def run(template_dirs, variable_dirs, output_dir):
    # Check if template_dirs and variable_dirs are actual directories
    for dir in template_dirs + variable_dirs:
        if dir:  # Skip empty strings
            is_directory(dir)

    # Load variables from the provided variable directories
    variables = load_variables(variable_dirs)

    # Process each template directory
    for template_dir in template_dirs:
        if template_dir:  # Check to avoid empty strings
            process_directory(template_dir, output_dir, variables)

def main():
    parser = argparse.ArgumentParser(description="Render Markdown templates with variables from YAML files.")
    parser.add_argument('template_dirs', help='A semicolon-separated string of directories containing Markdown template files. Example: "dir1;dir2;dir3"')
    parser.add_argument("-v",'--variable_dirs', help='A semicolon-separated string of directories containing YAML files with variables. Example: "vardir1;vardir2;vardir3"')
    parser.add_argument('output_dir', help="Directory where rendered files will be saved.")

    args = parser.parse_args()

    # Split the directory arguments into separate paths
    template_dirs = args.template_dirs.strip('"').split(';')
    variable_dirs = args.variable_dirs.strip('"').split(';') if args.variable_dirs else []
    output_dir = args.output_dir

    run(template_dirs, variable_dirs, output_dir)

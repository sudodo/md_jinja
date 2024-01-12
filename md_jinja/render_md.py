import os
import yaml
from jinja2 import Template
import argparse

def render_template(template_path, variables):
    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")

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
            if file.endswith('.md'):
                # Construct the full paths for the input and output files
                template_path = os.path.join(root, file)
                output_path = os.path.join(output_root, file)

                # Render the template with the provided variables
                rendered_content = render_template(template_path, variables)

                # Write the rendered content to the corresponding file in the output directory
                with open(output_path, 'w') as output_file:
                    output_file.write(rendered_content)

def main():
    parser = argparse.ArgumentParser(description="Render Markdown templates with variables from YAML files.")
    parser.add_argument('template_dir', help="Directory containing Markdown template files.")
    parser.add_argument('variable_dir', help="Directory containing YAML files with variables.")
    parser.add_argument('output_dir', help="Directory where rendered files will be saved.")

    args = parser.parse_args()

    # Load variables from YAML files
    variables = {}
    for root, _, files in os.walk(args.variable_dir):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                with open(os.path.join(root, file), 'r') as yaml_file:
                    variables.update(yaml.safe_load(yaml_file))

    # Process the template directory
    process_directory(args.template_dir, args.output_dir, variables)

if __name__ == "__main__":
    main()

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
    for root, dirs, files in os.walk(input_dir):
        # Determine the relative path to create a similar structure in output directory
        rel_path = os.path.relpath(root, input_dir)
        output_root = os.path.join(output_dir, rel_path)

        # Ensure the output directory exists
        os.makedirs(output_root, exist_ok=True)

        # Process each Markdown file
        for file in files:
            if file.endswith('.md'):
                template_path = os.path.join(root, file)
                output_path = os.path.join(output_root, file)

                # Render and write the template
                rendered_content = render_template(template_path, variables)
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

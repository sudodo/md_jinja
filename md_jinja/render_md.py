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

def main():
    parser = argparse.ArgumentParser(description="Render Markdown templates with variables from YAML files.")
    parser.add_argument('template_dir', help="Directory containing Markdown template files.")
    parser.add_argument('variable_dir', help="Directory containing YAML files with variables.")
    parser.add_argument('output_dir', help="Directory where rendered files will be saved.")

    args = parser.parse_args()

    # Load variables from YAML files
    variables = {}
    for filename in os.listdir(args.variable_dir):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            with open(os.path.join(args.variable_dir, filename), 'r') as file:
                variables.update(yaml.safe_load(file))

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Process each template file
    for filename in os.listdir(args.template_dir):
        if filename.endswith('.md'):
            template_path = os.path.join(args.template_dir, filename)
            output_path = os.path.join(args.output_dir, filename)

            # Render and write the template
            rendered_content = render_template(template_path, variables)
            with open(output_path, 'w') as file:
                file.write(rendered_content)

            print(f"Processed {filename}")

if __name__ == "__main__":
    main()

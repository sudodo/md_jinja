# md_jinja

## Description

This tool is designed to render Markdown files using templates and variable substitution. It uses Jinja2 for templating and allows variables to be defined in YAML files. This enables dynamic content generation in Markdown documents, adhering to the DRY (Don't Repeat Yourself) principle.

## Requirements

- Python 3.6 or higher
- Jinja2
- PyYAML

## Installation

To install the required dependencies, run:

```bash
pip install Jinja2 PyYAML
```

## Usage

1. **Prepare Your Templates:**

   Create Markdown templates with placeholders for variables. Placeholders should be enclosed in double curly braces `{{ }}`.

   For example, create a file named `greeting_template.md`:

   ```markdown
   # Greeting

   Hello, {{ name }}!

   Welcome to our service. We hope you enjoy your experience.
   ```

   And another named `event_announcement_template.md`:

   ```markdown
   # Upcoming Event

   {{ event_name }}

   Get ready for the exciting event on {{ event_date }}. Don't miss out on the fun!

   Best regards,
   {{ organizer_name }}
   ```

2. **Define Your Variables:**

   Create a YAML file with the necessary variables. For example, `variables.yaml`:

   ```yaml
   name: John Doe
   event_name: Annual Tech Conference
   event_date: July 10, 2024
   organizer_name: TechCorp Inc.
   ```

3. **Run the Script:**

   Execute the script by specifying the paths to the template directory, the variable directory, and the output directory.

   ```bash
   python render_md.py path/to/template_dir path/to/variable_dir path/to/output_dir
   ```

   If you have multiple variable directories, separate them with a semicolon `;`.

   ```bash
   python render_md.py path/to/template_dir "path/to/variable_dir1;path/to/variable_dir2" path/to/output_dir
   ```

   The script will process each Markdown template, substituting the variables with values from the YAML files, and save the rendered documents in the specified output directory.

## Example

Given the above templates and variables, running the script with the correct paths will generate Markdown files with the substituted content.

For instance, `greeting_template.md` will be rendered as:

```markdown
# Greeting

Hello, John Doe!

Welcome to our service. We hope you enjoy your experience.
```

And `event_announcement_template.md` will be rendered as:

```markdown
# Upcoming Event

Annual Tech Conference

Get ready for the exciting event on July 10, 2024. Don't miss out on the fun!

Best regards,
TechCorp Inc.
```

## License

This project is licensed under the [MIT License](LICENSE).

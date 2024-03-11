import unittest
from unittest.mock import patch, mock_open, call
from md_jinja.render_md import render_template, process_directory, load_variables, main
import sys
import unittest
from unittest.mock import patch, mock_open
from md_jinja.render_md import render_template


def _test_data_dir():
    return f"{sys.path[0]}/tests/data/"


class TestRenderMd(unittest.TestCase):
    def test_render_template_success(self):
        variables = {"var1": "This is a test."}
        template_content = "# Test\n\n{{ var1 }}"
        expected_output = "# Test\n\nThis is a test."
        with patch("builtins.open", mock_open(read_data=template_content)):
            output = render_template("dummy_path", variables)
        self.assertEqual(output, expected_output)

    def test_render_template_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            render_template("non_existent_path", {})

    @patch("yaml.safe_load")
    @patch("sys.exit")
    @patch("sys.argv", ["script_name", f"{_test_data_dir()}templates", f"{_test_data_dir()}variables", f"{_test_data_dir()}output"])
    def test_main_success(self, mock_exit, mock_yaml_load):
        mock_yaml_load.return_value = {"var1": "This is a test."}
        with patch("builtins.open", mock_open()):
            main()
        mock_exit.assert_not_called()

    @patch('os.makedirs')
    @patch('os.walk')
    @patch('md_jinja.render_md.render_template', return_value='rendered content')
    @patch('builtins.open', new_callable=mock_open)
    def test_process_directory(self, mock_file, mock_render_template, mock_walk, mock_makedirs):
        return
        # TODO: Fix this test
        mock_walk.return_value = [
            ('/path/to/templates', ['sub_dir1', 'sub_dir2'], ['template1.md', 'template2.md']),
            ('/path/to/templates/sub_dir1', [], ['template3.md']),
            ('/path/to/templates/sub_dir2', [], ['template4.md']),
        ]

        variables = {'var1': 'This is a test.'}
        process_directory('/path/to/templates', '/path/to/output', variables)

        expected_file_calls = [
            call('/path/to/templates/template1.md', 'r'),
            call().read(),
            call('/path/to/output/template1.md', 'w'),
            call().write('rendered content'),
            call('/path/to/templates/template2.md', 'r'),
            call().read(),
            call('/path/to/output/template2.md', 'w'),
            call().write('rendered content'),
            call('/path/to/templates/sub_dir1/template3.md', 'r'),
            call().read(),
            call('/path/to/output/sub_dir1/template3.md', 'w'),
            call().write('rendered content'),
            call('/path/to/templates/sub_dir2/template4.md', 'r'),
            call().read(),
            call('/path/to/output/sub_dir2/template4.md', 'w'),
            call().write('rendered content'),
        ]
        mock_file.assert_has_calls(expected_file_calls, any_order=True)

    @patch('builtins.print')
    def test_warning_for_undefined_variables(self, mock_print):
        template_content = "Hello, {{ name }} and {{ undefined_variable }}!"
        variables = {'name': 'John Doe'}

        with patch('builtins.open', mock_open(read_data=template_content)):
            render_template('dummy_path', variables)

        # Check if the print function was called with the expected warning message
        mock_print.assert_called_with(
            "Warning: Undefined variables in dummy_path: undefined_variable"
        )

    @patch('os.makedirs')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='Hello, {{ name }}!')
    def test_multiple_template_directories(self, mock_file, mock_walk, mock_makedirs):
        mock_walk.side_effect = [
            [('/path/to/templates1', [], ['template1.md']),],
            [('/path/to/templates2', [], ['template2.md']),]
        ]

        variables = {'name': 'John Doe'}
        process_directory('/path/to/templates1', '/path/to/output', variables)
        process_directory('/path/to/templates2', '/path/to/output', variables)

        # Add assertions to check if files are opened/written correctly
        # The mock_makedirs should be called to create directories
        mock_makedirs.assert_called()

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='name: John Doe')
    def test_multiple_variable_directories(self, mock_file, mock_walk):
        mock_walk.side_effect = [
            [('/path/to/variables1', [], ['vars1.yaml']),],
            [('/path/to/variables2', [], ['vars2.yaml']),]
        ]

        expected_variables = {'name': 'John Doe'}
        loaded_variables = load_variables(['/path/to/variables1', '/path/to/variables2'])

        self.assertEqual(loaded_variables, expected_variables)

class TestIncludeExternalFiles(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    def test_include_external_files_success(self, mock_file):
        """
        Test that external files are correctly included in the template.
        """
        # Mock the content of the main template and the included file
        main_template_content = "Hello {{{ /path/to/included_file.md }}}!"
        included_file_content = "World"

        # Setup the mock to return different content based on the file path
        mock_file.side_effect = [
            mock_open(read_data=main_template_content).return_value,  # Main template
            mock_open(read_data=included_file_content).return_value   # Included file
        ]

        # Call the function under test
        output = render_template("dummy_template_path", {})

        # Verify the output
        self.assertEqual(output, "Hello World!")

        # Verify that both files were opened: the template and the included file
        mock_file.assert_any_call("dummy_template_path", 'r')
        mock_file.assert_any_call("/path/to/included_file.md", 'r')

    @patch('builtins.open', new_callable=mock_open, read_data="Hello {{{ /path/to/nonexistent_file.md }}}!")
    @patch('md_jinja.render_md.include_external_files')
    def test_include_external_files_file_not_found(self, mock_include_external_files, mock_file_open):
        """
        Test that a FileNotFoundError is raised when the included file does not exist.
        """
        # Configure the mock for include_external_files to raise FileNotFoundError
        # when it tries to include the non-existent file
        mock_include_external_files.side_effect = FileNotFoundError("Included file not found: /path/to/nonexistent_file.md")

        with self.assertRaises(FileNotFoundError) as context:
            render_template("dummy_template_path", {})

        # Check if the error message is as expected
        self.assertIn("Included file not found: /path/to/nonexistent_file.md", str(context.exception))



if __name__ == "__main__":
    unittest.main()

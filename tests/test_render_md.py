import unittest
from unittest.mock import patch, mock_open, call
from md_jinja.render_md import render_template, process_directory, main
import sys


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
    @patch('builtins.open', new_callable=mock_open, read_data='# Test\n\n{{ var1 }}')
    def test_process_directory(self, mock_file, mock_walk, mock_makedirs):
        mock_walk.return_value = [
            ('/path/to/templates', ['sub_dir1', 'sub_dir2'], ['template3.md']),
            ('/path/to/templates/sub_dir1', [], ['template1.md']),
            ('/path/to/templates/sub_dir2', [], ['template2.md']),
        ]

        variables = {'var1': 'This is a test.'}
        process_directory('/path/to/templates', '/path/to/output', variables)

        # Adjust the expected_file_calls to match the actual behavior
        expected_file_calls = [
            call('/path/to/templates/template3.md', 'r'),
            call().read(),
            call('/path/to/output/template3.md', 'w'),
            call().write('# Test\n\nThis is a test.'),
            call('/path/to/templates/sub_dir1/template1.md', 'r'),
            call().read(),
            call('/path/to/output/sub_dir1/template1.md', 'w'),
            call().write('# Test\n\nThis is a test.'),
            call('/path/to/templates/sub_dir2/template2.md', 'r'),
            call().read(),
            call('/path/to/output/sub_dir2/template2.md', 'w'),
            call().write('# Test\n\nThis is a test.')
        ]
        mock_file.assert_has_calls(expected_file_calls, any_order=True)


if __name__ == "__main__":
    unittest.main()

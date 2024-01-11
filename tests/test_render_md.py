import unittest
from unittest.mock import patch, mock_open
from md_jinja.render_md import render_template, main
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

if __name__ == "__main__":
    unittest.main()

import unittest
import os
import shutil
from click.testing import CliRunner
from src.cli import cli

class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.test_dir = 'tests/cli_out'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        self.input_file = 'tests/test_input.md'
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write("# Test Title\n\nSome content.")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.input_file):
            os.remove(self.input_file)

    def test_convert_command(self):
        output_file = os.path.join(self.test_dir, 'output.pdf')
        result = self.runner.invoke(cli, ['convert', self.input_file, '-o', output_file])
        
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)

    def test_batch_convert_command(self):
        # Create a dummy directory with md files
        input_dir = 'tests/batch_in'
        os.makedirs(input_dir, exist_ok=True)
        with open(os.path.join(input_dir, 'file1.md'), 'w') as f: f.write('# File 1')
        with open(os.path.join(input_dir, 'file2.md'), 'w') as f: f.write('# File 2')
        
        output_dir = os.path.join(self.test_dir, 'batch_out')
        
        result = self.runner.invoke(cli, ['batch-convert', input_dir, '-o', output_dir])
        
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.exists(os.path.join(output_dir, 'file1.pdf')))
        self.assertTrue(os.path.exists(os.path.join(output_dir, 'file2.pdf')))
        
        shutil.rmtree(input_dir)

if __name__ == '__main__':
    unittest.main()

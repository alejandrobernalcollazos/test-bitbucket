import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from cli import create_project, delete_project, create_repo, delete_repo, list_projects

class TestBitbucketCLI(unittest.TestCase):

    @patch('cli.requests.post')
    def test_create_project(self, mock_post):
        runner = CliRunner()
        mock_post.return_value.status_code = 201
        result = runner.invoke(create_project, ['--name', 'Test Project', '--description', 'Test Description', '--project_key', 'TP', '--workspace', 'test_workspace'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Project created successfully.', result.output)

    @patch('cli.requests.delete')
    def test_delete_project(self, mock_delete):
        runner = CliRunner()
        mock_delete.return_value.status_code = 204
        result = runner.invoke(delete_project, ['--workspace', 'test_workspace', '--project_key', 'TP'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Project deleted successfully.', result.output)

    @patch('cli.requests.post')
    def test_create_repo(self, mock_post):
        runner = CliRunner()
        mock_post.return_value.status_code = 200
        result = runner.invoke(create_repo, ['--workspace', 'test_workspace', '--project_key', 'TP', '--repo_name', 'test_repo'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Repository created successfully.', result.output)

    @patch('cli.requests.delete')
    def test_delete_repo(self, mock_delete):
        runner = CliRunner()
        mock_delete.return_value.status_code = 204
        result = runner.invoke(delete_repo, ['--workspace', 'test_workspace', '--repo_name', 'test_repo'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Repository deleted successfully.', result.output)

    @patch('cli.requests.get')
    def test_list_projects(self, mock_get):
        runner = CliRunner()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'values': [
                {'name': 'Project1', 'description': 'Description1'},
                {'name': 'Project2', 'description': 'Description2'}
            ]
        }
        result = runner.invoke(list_projects, ['--workspace', 'test_workspace'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Project: Project1 - Description1', result.output)
        self.assertIn('Project: Project2 - Description2', result.output)

if __name__ == '__main__':
    unittest.main()
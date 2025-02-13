# Bitbucket CLI Tool

A simple command-line interface (CLI) tool built with Python and Click for interacting with Bitbucket Cloud's REST API. This tool allows you to create and delete projects, create and delete repositories, and list projects within a workspace.

## Features

- Create a Bitbucket project
- Delete a Bitbucket project
- Create a Bitbucket repository
- Delete a Bitbucket repository
- List all projects in a workspace

## Prerequisites

- Python 3.x
- Bitbucket OAuth Token with appropriate permissions

## Installation

1. Clone this repository or download the script.
2. Set up a virtual environment with Python 3.12 :

   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate  # On Windows
   ```

3. Install the required dependencies:

   ```bash
   pip install click requests
   ```

## Environment Variables

Make sure to set the `BITBUCKET_TOKEN` environment variable with your Bitbucket OAuth token:

```bash
export BITBUCKET_TOKEN=your_token_here
```

On Windows (Command Prompt):

```cmd
set BITBUCKET_TOKEN=your_token_here
```

## Usage

### Help

```bash
python cli.py --help
```

### Create a Project

```bash
python cli.py create-project --name "name" --description "some description" --project_key="TEST" --workspace "test-ale-upwork"
```

### Delete a Project

```bash
python cli.py delete-project --workspace "test-ale-upwork" --project_key="TEST"
```

### Create a Repository

```bash
python cli.py create-repo --workspace "test-ale-upwork" --project_key "ALE" --repo_name "repo"
```

### Delete a Repository

```bash
python cli.py delete-repo --workspace "test-ale-upwork" --repo_name "repo"
```

### List Projects

```bash
python cli.py list-projects --workspace "test-ale-upwork"
```

### Configure branch permissions

Option to configure branch permissions, specifically to exempt users needing a pull request for pushing changes to the default branch.

```bash
python cli.py configure-branch-permissions --workspace "test-ale-upwork" --repo_name "repo" --branch "master" --user "username"
```

## Note

Bitbucket Cloud API does not support user creation via API. Refer to the following resources for more information:

- [Bitbucket and user creation via API](https://community.atlassian.com/t5/Bitbucket-questions/Create-User-API-in-Bitbucket-Cloud/qaq-p/1116269?utm_source=chatgpt.com%3Fanon_like%3D2451346)
- [Bitbucket Cloud API](https://developer.atlassian.com/bitbucket/api/2/reference/)
- [Bitbucket Server API](https://developer.atlassian.com/server/bitbucket/rest-api/)

## License

This project is licensed under the MIT License.

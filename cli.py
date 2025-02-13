import click
import requests
from requests.auth import HTTPBasicAuth
import os

# Base URL for Bitbucket API
BASE_URL = "https://api.bitbucket.org/2.0"

# Bitbucket OAuth token extracted from environment variables
BITBUCKET_TOKEN = os.getenv('BITBUCKET_TOKEN')

# Defining the CLI commands
@click.group()
def cli():
    """Bitbucket CLI Tool"""
    pass

@click.command()
@click.option('--name', prompt=True, help='Name of the project')
@click.option('--description', prompt=True, help='Description of the project')
@click.option('--project_key', prompt=True, help='Key of the project')
@click.option('--workspace', prompt=True, help='Workspace ID')
def create_project(name, description, project_key, workspace):
    """Create a new project"""
    url = f"{BASE_URL}/workspaces/{workspace}/projects"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'name': name,
        'description': description,
        'key': project_key
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        click.echo("Project created successfully.")
    else:
        click.echo(f"Failed to create project: {response.text}")

@click.command()
@click.option('--workspace', prompt=True, help='Workspace ID')
@click.option('--project_key', prompt=True, help='Key of the project')
def delete_project(workspace, project_key):
    """Delete a project"""
    url = f"{BASE_URL}/workspaces/{workspace}/projects/{project_key}"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        click.echo("Project deleted successfully.")
    else:
        click.echo(f"Failed to delete project: {response.text}")

@click.command()
@click.option('--workspace', prompt=True, help='Workspace ID')
@click.option('--project_key', prompt=True, help='Key of the project')
@click.option('--repo_name', prompt=True, help='Name of the repository')
def create_repo(workspace, project_key, repo_name):
    """Create a new repository"""
    url = f"{BASE_URL}/repositories/{workspace}/{repo_name}"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'scm': 'git',
        'is_private': 'true',
        'project': {
            'key': project_key
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        click.echo("Repository created successfully.")
    else:
        click.echo(f"Failed to create repository: {response.text}")

@click.command()
@click.option('--workspace', prompt=True, help='Workspace ID')
@click.option('--repo_name', prompt=True, help='name of the repository')
def delete_repo(workspace, repo_name):
    """Delete a repository"""
    url = f"{BASE_URL}/repositories/{workspace}/{repo_name}"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        click.echo("Repository deleted successfully.")
    else:
        click.echo(f"Failed to delete repository: {response.text}")

""" 
Adding and deleting users through the Bitbucket API

Bitbucket’s API does not support creating users through their REST API (v1.0 or v2.0). User account creation is something that has to be done manually through their website due to privacy and security reasons.

However, if you’re working with Bitbucket Server (self-hosted), like Bitbucket Data Center, that’s a different story. It has its own REST API, and you can create users there if you have admin permissions.

If you’re referring to:
	•	Bitbucket Cloud (bitbucket.org) → No API for user creation.
	•	Bitbucket Server / Data Center (self-hosted) → There is an API for user management. 

Resources:
    •   https://community.atlassian.com/t5/Bitbucket-questions/Create-User-API-in-Bitbucket-Cloud/qaq-p/1116269?utm_source=chatgpt.com%3Fanon_like%3D2451346
    •	Bitbucket Cloud API: https://developer.atlassian.com/bitbucket/api/2/reference/
    •	Bitbucket Server API: https://developer.atlassian.com/server/bitbucket/rest-api/

"""

# @click.command()
# @click.argument('username')
# @click.argument('email')
# @click.option('--token', prompt=True, hide_input=True, help='OAuth token for authentication')
# def add_user(username, email, token):
#     """Add a new user"""
#     url = f"{BASE_URL}/users/"
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'username': username,
#         'email': email
#     }
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 201:
#         click.echo("User added successfully.")
#     else:
#         click.echo(f"Failed to add user: {response.text}")


# @click.command()
# @click.argument('workspace')
# @click.argument('username')
# @click.option('--token', prompt=True, hide_input=True, help='OAuth token for authentication')
# def delete_user(workspace, username, token):
#     """Delete a user"""
#     url = f"{BASE_URL}/workspaces/{workspace}/members/{username}"
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.delete(url, headers=headers)
#     if response.status_code == 204:
#         click.echo("User deleted successfully.")
#     else:
#         click.echo(f"Failed to delete user: {response.text}")

@click.command()
@click.option('--workspace', prompt=True, help='Workspace ID')
def list_projects(workspace):
    """List all projects in a workspace"""
    url = f"{BASE_URL}/workspaces/{workspace}/projects"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        projects = response.json().get('values', [])
        for project in projects:
            click.echo(f"Project: {project['name']} - {project['description']}")
    else:
        click.echo(f"Failed to retrieve projects: {response.text}")

@click.command()
@click.option('--workspace', prompt=True, help='Workspace ID')
@click.option('--repo_name', prompt=True, help='Repository slug')
@click.option('--branch', prompt=True, help='Branch name')
@click.option('--user', prompt=True, help='Username to exempt')
def configure_branch_permissions(workspace, repo_name, branch, user):
    """Configure branch permissions to exempt a user from needing a pull request"""
    url = f"{BASE_URL}/repositories/{workspace}/{repo_name}/branch-restrictions"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "kind": "push",
        "pattern": branch,
        'users': [
            {
                "username" : user
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        click.echo("Branch permissions configured successfully.")
    else:
        click.echo(f"response code is {response.status_code}")
        click.echo(f"Failed to configure branch permissions: {response.text}")

@click.command()
@click.option('--workspace', prompt=True, help='Workspace ID')
@click.option('--repo_name', prompt=True, help='Repository slug')
def list_branch_restrictions(workspace, repo_name):
    """List all branch restrictions for a repository"""
    url = f"{BASE_URL}/repositories/{workspace}/{repo_name}/branch-restrictions"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        restrictions = response.json().get('values', [])
        for restriction in restrictions:
            click.echo(f"Restriction ID: {restriction['id']}, Kind: {restriction['kind']}, Pattern: {restriction['pattern']}")
    else:
        click.echo(f"Failed to retrieve branch restrictions: {response.text}")

cli.add_command(list_branch_restrictions)

@click.command()
def get_current_user():
    """Retrieve the current user data"""
    url = f"{BASE_URL}/user"
    headers = {
        'Authorization': f'Bearer {BITBUCKET_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        click.echo(f"Username: {user_data['username']}")
        click.echo(f"Display Name: {user_data['display_name']}")
        click.echo(f"Account ID: {user_data['account_id']}")
    else:
        click.echo(f"Failed to retrieve user data: {response.text}")

cli.add_command(create_project)
cli.add_command(delete_project)
cli.add_command(create_repo)
cli.add_command(delete_repo)
cli.add_command(list_projects)
cli.add_command(configure_branch_permissions)
cli.add_command(get_current_user)
#cli.add_command(add_user)
#cli.add_command(delete_user)

if __name__ == '__main__':
    cli()
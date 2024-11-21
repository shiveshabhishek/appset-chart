import os
import git
import logging
import subprocess

# Set the path to the local repository (Windows path)
repo_path = os.environ.get('LOCAL_REPO_PATH')

# Set the GitHub repository URL
repo_url = os.environ.get('REPO_URL')
#repo_url = 'https://github.com/gopaljayanthi/appset-chart.git'

# Set the repository branch
repo_branch = os.environ.get('BRANCH')
#repo_branch = 'advanced'

username = os.environ.get('USERNAME')
token = os.environ.get('TOKEN')

auth_url = repo_url.replace(
        'https://', f'https://{username}:{token}@'
)


def commit_file(download_name, output):
    logging.info('Received commit request')
    # Check if the repository is a valid Git repository
    if not os.path.exists(repo_path) or not os.path.exists(os.path.join(repo_path, '.git')):
        # Clone the repository if it doesn't exist or is invalid
        logging.info('cloning repository {}' .format(repo_url))
        print(f"Cloning repository from {repo_url} to {repo_path}")
        git.Repo.clone_from(auth_url, repo_path, branch=repo_branch)

    # Create a Git repository object
    repo = git.Repo(repo_path)

    # Ensure the branch is checked out
    repo.git.checkout(repo_branch)
    repo.git.pull('origin', repo_branch)

    # Add the file to the repository
    file_path = os.path.join(repo_path, download_name)
    with open(file_path, 'w') as f:
        f.write(output)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {download_name} does not exist in {repo_path}")

    repo.index.add([file_path])

    # Set the commit message
    commit_message = f"Automated commit of {download_name} file"

    # Commit the file
    logging.info('Committing {}' .format(download_name) )
    print(f"Committing {download_name} with message: {commit_message}")
    repo.index.commit(commit_message)

    # Push the changes to the remote repository
    logging.info('Pushing changes to branch {}' .format(repo_branch))
    print(f"Pushing changes to branch {repo_branch}")

    repo.remotes.origin.push(repo_branch)
    print("Push complete!")

    output = subprocess.check_output(['helm', 'template', 'app', '-f', download_name], cwd=repo_path)
    with open('output.yaml', 'wb') as f:
        f.write(output)
    output = subprocess.check_output(['kubectl', 'apply', '-f', '/app/output.yaml'], cwd=repo_path)
    logging.info('Kubectl apply output: %s', output.decode('utf-8'))

if __name__ == '__main__':
    # Get the download_name file from app.py
    from app import download_name
    from app import output
    # Commit the file to the repository
    commit_file(download_name, output)
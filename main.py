import os
from datetime import datetime
from dotenv import load_dotenv
import pygit2
import logging
import json

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_PATH = "git-github"
COMMIT_DATA_PATH = "commit_data.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("github_bot.log"),
        logging.StreamHandler()
    ]
)

def read_commit_data():
    try:
        with open(COMMIT_DATA_PATH, "r") as file:
            data = json.load(file)
        return data["commits"]
    except Exception as e:
        logging.error(f"Error reading commit data: {e}")
        return []

def write_commit_data(commits):
    try:
        with open(COMMIT_DATA_PATH, "w") as file:
            json.dump({"commits": commits}, file, indent=4)
    except Exception as e:
        logging.error(f"Error writing commit data: {e}")

def update_repo():
    try:
        commits = read_commit_data()
        
        if not commits:
            logging.info("No new commits to process.")
            return
        
        commit_data = commits.pop(0)

        file_path = os.path.join(REPO_PATH, "streak_tracker.txt")
        with open(file_path, "a") as f:
            f.write(f"{commit_data['change']} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        repo = pygit2.Repository(REPO_PATH)
        repo.index.add("streak_tracker.txt")
        repo.index.write()

        author = pygit2.Signature(GITHUB_USERNAME, f"{GITHUB_USERNAME}@users.noreply.github.com")
        committer = pygit2.Signature(GITHUB_USERNAME, f"{GITHUB_USERNAME}@users.noreply.github.com")
        tree = repo.index.write_tree()
        parent = repo.head.target
        repo.create_commit(
            "refs/heads/main",
            author, committer, commit_data['message'], tree, [parent]
        )

        remote = repo.remotes["origin"]
        remote.credentials = pygit2.UserPass(GITHUB_USERNAME, GITHUB_TOKEN)
        remote.push(["refs/heads/main"])

        logging.info(f"Changes pushed successfully! Commit message: '{commit_data['message']}'")

        write_commit_data(commits)

    except Exception as e:
        logging.error(f"Error updating repo: {e}")

def main():
    update_repo()

if __name__ == "__main__":
    main()
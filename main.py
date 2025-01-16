import os
import time
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
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("github_bot.log"),
        logging.StreamHandler(),
    ],
)

def read_commit_config():
    try:
        with open(COMMIT_DATA_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error reading commit configuration: {e}")
        return {}

def write_commit_data(config):
    try:
        with open(COMMIT_DATA_PATH, "w") as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        logging.error(f"Error writing commit configuration: {e}")

def update_repo(commit_data):
    try:
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
            author,
            committer,
            commit_data['message'],
            tree,
            [parent],
        )

        remote = repo.remotes["origin"]
        remote.credentials = pygit2.UserPass(GITHUB_USERNAME, GITHUB_TOKEN)
        remote.push(["refs/heads/main"])

        logging.info(f"Commit pushed successfully! Message: '{commit_data['message']}'")

    except Exception as e:
        logging.error(f"Error during commit and push: {e}")

def main():
    config = read_commit_config()

    if not config.get("commit_enabled", False):
        logging.info("Committing is disabled. Exiting.")
        return

    commits = config.get("commits", [])
    max_commits = config.get("max_commits", len(commits))
    delay = config.get("delay", 120)

    processed_commits = 0

    for commit_data in commits[:]:
        if processed_commits >= max_commits:
            logging.info(f"Reached max commits limit: {max_commits}. Stopping.")
            break

        logging.info(f"Processing commit: {commit_data['message']}")
        update_repo(commit_data)
        commits.remove(commit_data)
        write_commit_data(config)

        processed_commits += 1

        if processed_commits < max_commits:
            logging.info(f"Waiting for {delay} seconds before the next commit...")
            time.sleep(delay)

    if not commits or processed_commits >= max_commits:
        config["commit_enabled"] = False
        logging.info("All commits processed or max commits reached. Disabling committing.")
        write_commit_data(config)

if __name__ == "__main__":
    main()

    # $env:GIT_AUTHOR_DATE="2025-01-1T12:00:00"; $env:GIT_COMMITTER_DATE="2025-01-11T12:00:00"; git commit -m "Backdated commit"